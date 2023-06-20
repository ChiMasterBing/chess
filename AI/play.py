#MAIN DRIVER
import AI.search as search
from AI.board import board
import AI.tables as t

def flipCase(c):
    if c == '.': return c
    elif c >= 'a': return c.upper()
    return c.lower()


def getMove(state, player):
    state = ''.join(flipCase(c) for c in state)[::-1]
    state = (''.join([''.join(state[rs*8:rs*8+8][::-1]) for rs in range(8)]))

    print(f"Received Board as {player}\n{state}")

    brd = board(state, player)

    move = search.PVS(brd, -999, 999, 0, 5)

    if not move:
        print(f"[AI] Checkmate Detected")
        exit()

    print(f"[AI] Selected Move {move[0]} {t.letter[move[1]%8]}{8-move[1]//8}")

    #format move according to GUI specification
    return f"{str(move[0])[2:]}{t.letter[move[1]%8]}{8-move[1]//8}"

dflt = 'RNBQKBNRPPPPPPPP................................pppppppprnbqkbnr'

#print(getMove(dflt, 1))