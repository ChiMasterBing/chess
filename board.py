from piece import piece
import tables as t
#use rudimentry methods - could be optimized for bitboards later
class board:
    state = 'RNBQKBNRPPPPPPPP................................pppppppprnbqkbnr'
    pieces = [set(), set()]
    pbypos = [None for _ in range(64)]
    player = 1 #white starts
    #initialize the board, default position given
    def __init__(self, s = state, p = 1):
        self.pieces = [set(), set()]
        self.state = s
        self.player = p
        self.setPieces()
    
    def setPieces(self): #fills the pieces set
        for i, p in enumerate(self.state):
            if p != '.':
                tmp = piece(p, i)
                tmp.findMoves(self.state)
                self.pieces[tmp.team].add(tmp)
                self.pbypos[tmp.index] = tmp

    def playMove(self, piece, move): #play a move
        assert(piece in self.pieces[piece.team])
        #assert move in piece.moves[0] or move in piece.moves[1], f"{move} {piece} {piece.moves}"
        brd = [*self.state]
        brd[piece.index] = '.'
        brd[move] = piece.symbol
        
        self.pbypos[piece.index] = None
        piece.move(move)
        self.pbypos[piece.index] = piece

        self.state = ''.join(brd)
        self.player ^= 1
    
    def unplayMove(self, piece, move, fromPos):
        assert piece in self.pieces[piece.team], piece
        assert(move == piece.index)
        brd = [*self.state]
        brd[piece.index] = '.'
        brd[fromPos] = piece.symbol
        
        self.pbypos[piece.index] = None
        piece.unmove(fromPos)
        self.pbypos[piece.index] = piece
        
        self.state = ''.join(brd)
        self.player ^= 1
    
    def placeUpdate(self, move): #incrementally update moves for new state
        #TODO: delayed team updates
        #print(piece, piece.index, move)
        #assert(piece in self.pieces[piece.team])
        #assert(move == piece.index)
        for p in (self.pieces[0] | self.pieces[1]):
            if move in p.moves[0] or move in p.moves[1]:
                p.findMoves(self.state)

    def clearUpdate(self, pos):
        for nxt in t.knightMoves[pos]:
            if self.pbypos[nxt] != None and self.pbypos[nxt].type == 'N':
                self.pbypos[nxt].findMoves(self.state)
        #TODO: speed here
        for strip in t.strips[pos]:
            for nxt in strip:
                if self.pbypos[nxt] != None and self.pbypos[nxt].type != 'N':
                    self.pbypos[nxt].findMoves(self.state)
                    break
        

    def __str__(self): #2d board representation
        out = [*self.state]
        for p in (self.pieces[0] | self.pieces[1]):
            a, b = p.findMoves(self.state)
            for mv in b:
                if p.team == 1:
                    if out[mv] == '@' or out[mv] == '&':
                        out[mv] = '&'
                    else: 
                        out[mv] = '*'
                else:
                    if out[mv] == '*' or out[mv] == '&':
                        out[mv] = '&'
                    else: 
                        out[mv] = '@'
            for mv in a:
                if p.team == 1:
                    out[mv] = 'X'
                else:
                    out[mv] = 'x'
        out = ''.join(out)
        return('\n'.join([out[rs*8:rs*8+8]for rs in range(8)]))
    
    def p2d(self):
        return('\n'.join([self.state[rs*8:rs*8+8]for rs in range(8)]))
    


#if __name__ == "__main__":
