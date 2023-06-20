import tables as t

class piece:
    type = None
    symbol = None
    index = None
    team = None #white = 1, black = 0
    hash = None
    moves = set()
    def __init__(self, type, i):
        self.type, self.index, self.symbol = type.upper(), i, type
        self.team = 1 if type >= 'a' else 0
        self.hash = t.names[self.type] + self.index * 10
    def __hash__(self):
        return self.hash

    def __str__(self):
        return f"{self.type}:{t.letter[self.index%8]}{self.index//8}"
    
    def __eq__(self, obj):
        return hash(self) == hash(obj)

    def move(self, move): #DOES NOT UPDATE ITS MOVES
        #assert move in self.moves[0] or move in self.moves[1], move
        self.index = move
        #print("set index as", self.index)

    def unmove(self, fromPos):
        self.index = fromPos

    def findMoves(self, board):
        captures = set()
        quiet = set()
        if self.type == 'N':
            for pos in t.knightMoves[self.index]:
                if board[pos] != '.':
                    t_team = (board[pos] >= 'a')
                    if t_team ^ self.team:
                        captures.add(pos)
                else:
                    quiet.add(pos)
        if self.type in ['Q', 'R']:
            for strp in t.strips[self.index][:4]:
                for pos in strp:
                    if board[pos] != '.':
                        t_team = (board[pos] >= 'a')
                        if t_team ^ self.team: #not the same team
                            captures.add(pos)
                        break
                    quiet.add(pos)
        if self.type in ['Q', 'B']:
            for strp in t.strips[self.index][4:]:
                for pos in strp:
                    if board[pos] != '.':
                        t_team = (board[pos] >= 'a')
                        if t_team ^ self.team: #not the same team
                            captures.add(pos)
                        break
                    quiet.add(pos)
        if self.type == 'K':
            for strp in t.strips[self.index]:
                for pos in strp:
                    if board[pos] != '.':
                        t_team = (board[pos] >= 'a')
                        if t_team ^ self.team: #not the same team
                            captures.add(pos)
                        break
                    quiet.add(pos)
                    break #break after first
        if self.type == 'P':
            for pos in t.pawnMoves[self.team][self.index]:
                if board[pos] != '.': break
                quiet.add(pos)
            
            for pos in t.pawnCaptures[self.team][self.index]:
                if board[pos] != '.':
                    t_team = (board[pos] >= 'a')
                    if self.team ^ t_team:
                        captures.add(pos)
        self.moves = (captures, quiet)
        return self.moves

