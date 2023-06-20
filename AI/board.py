from AI.piece import piece
import AI.tables as t
#use rudimentry methods - could be optimized for bitboards later
class board:
    state = 'RNBQKBNRPPPPPPPP................................pppppppprnbqkbnr'
    pieces = [set(), set()]
    pbypos = [None for _ in range(64)]
    player = 1 #white starts
    #initialize the board, default position given
    def __init__(self, s = state, p = 1):
        self.pieces = [set(), set()]
        self.state = [*s]
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
        # assert piece in self.pieces[piece.team]
        # assert move != piece.index
        #assert move in piece.moves[0] or move in piece.moves[1], f"{move} {piece} {piece.moves}"

        self.state[piece.index] = '.'
        self.state[move] = piece.symbol
        self.pbypos[piece.index] = None
        piece.move(move)
        self.pbypos[piece.index] = piece
        self.player ^= 1
    
    def unplayMove(self, piece, move, fromPos, captured = None):
        # assert piece in self.pieces[piece.team], piece
        # assert move == piece.index
        # assert self.state[fromPos] == '.', "\n" + self.p2d() + "\n" + f"{piece} {move} {fromPos}"
        
        self.state[move] = captured.symbol if captured else '.'
        if captured: self.pieces[captured.team].add(captured)
        self.state[fromPos] = piece.symbol
        self.pbypos[move] = captured if captured else None
        piece.unmove(fromPos)
        self.pbypos[piece.index] = piece
        self.player ^= 1
        
    def evaluate(self):
        score = 0
        for p in self.pieces[self.player]:
            if p.type == 'K':
                score += 100
            elif p.type == 'Q':
                score += 9
            elif p.type == 'R':
                score += 5
            elif p.type == 'B' or p.type == 'N':
                score += 3
            elif p.type == 'P':
                score += 1

        for p in self.pieces[self.player^1]:
            if p.type == 'K':
                score -= 100
            elif p.type == 'Q':
                score -= 9
            elif p.type == 'R':
                score -= 5
            elif p.type == 'B' or p.type == 'N':
                score -= 3
            elif p.type == 'P':
                score -= 1
        return score

    def __str__(self): #2d board representation
        out = self.state.copy()
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
        return('\n'.join([''.join(self.state[rs*8:rs*8+8]) for rs in range(8)]))
    


#if __name__ == "__main__":
