from AI.piece import piece
import AI.tables as t
#use rudimentry methods - could be optimized for bitboards later
class board:
    state = 'RNBQKBNRPPPPPPPP................................pppppppprnbqkbnr'
    pieces = [set(), set()]
    pbypos = [None for _ in range(64)]
    player = 1 #white starts
    evaluation = 0
    mg, eg, gP = [0, 0], [0, 0], 0

    #initialize the board, default position given
    def __init__(self, s = state, p = 1):
        self.pieces = [set(), set()]
        self.state = [*s]
        self.player = p
        self.setPieces()
        self.hard_evaluate()
    
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

        #incrementally update evaluations
        if self.state[move] != '.':
            self.mg[piece.team ^ 1] -= t.mg_table[piece.team ^ 1][self.state[move].upper()][move]
            self.eg[piece.team ^ 1] -= t.eg_table[piece.team ^ 1][self.state[move].upper()][move]
            self.gP -= t.gamephaseInc[self.state[move].upper()]
        self.mg[piece.team] += t.mg_table[piece.team][piece.type][move]
        self.mg[piece.team] -= t.mg_table[piece.team][piece.type][piece.index]
        self.eg[piece.team] += t.eg_table[piece.team][piece.type][move]
        self.eg[piece.team] -= t.eg_table[piece.team][piece.type][piece.index]

        if self.state[move] != '.':
            captured = self.pbypos[move]
            self.pieces[captured.team].remove(captured)
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

        # #incrementally update evaluations
        # if self.state[move] != '.':
        #     self.mg[captured.team] += t.mg_table[captured.team][captured.type][move]
        #     self.eg[captured.team] += t.eg_table[captured.team][captured.type][move]
        #     self.gP += t.gamephaseInc[captured.type]
        # self.mg[piece.team] -= t.mg_table[piece.team][piece.type][move]
        # self.mg[piece.team] += t.mg_table[piece.team][piece.type][piece.index]
        # self.eg[piece.team] -= t.eg_table[piece.team][piece.type][move]
        # self.eg[piece.team] += t.eg_table[piece.team][piece.type][piece.index]

        if captured: self.pieces[captured.team].add(captured)
        self.state[fromPos] = piece.symbol
        self.pbypos[move] = captured if captured else None
        piece.unmove(fromPos)
        self.pbypos[piece.index] = piece
        self.player ^= 1
        
    
    def evaluate(self):
        mgScore = self.mg[1] - self.mg[0] 
        egScore = self.eg[1] - self.eg[0]
        g = max(self.gP, 24)
        e = 24-g
        score = (mgScore * g + egScore * e)/2400
        self.evaluation = score if self.player == 1 else -score
        return self.evaluation

    def hard_evaluate(self):
        g = 0
        mgW, mgB, egW, egB = 0, 0, 0, 0
        for p in self.pieces[0]:
            mgB += t.mg_table[0][p.type][p.index]
            egB += t.eg_table[0][p.type][p.index] 
            g += t.gamephaseInc[p.type]

        for p in self.pieces[1]:
            mgW += t.mg_table[1][p.type][p.index] 
            egW += t.eg_table[1][p.type][p.index] 
            g += t.gamephaseInc[p.type]

        self.mg = [mgB, mgW]
        self.eg = [egB, egW]
        self.gP = g

        mgScore = mgW - mgB 
        egScore = egW - egB

        g = max(g, 24)
        e = 24 - g

        score = (mgScore * g + egScore * e)/2400
        if self.player == 0:
            self.evaluation = -score
            return -score
        self.evaluation = score
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
