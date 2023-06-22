#MAIN DRIVER
import AI.search as search
from AI.board import board
import AI.tables as t
import time

def flipCase(c):
    if c == '.': return c
    elif c >= 'a': return c.upper()
    return c.lower()


def getMove(state, player):
    state = ''.join(flipCase(c) for c in state)[::-1]
    state = (''.join([''.join(state[rs*8:rs*8+8][::-1]) for rs in range(8)]))

    print(f"Received Board as {player}\n{state}")

    st = time.process_time()
    brd = board(state, player) #move this outside
    for i in range(2, 10):
        
        print("Running depth", i)
        move = search.PVS(brd, -999, 999, 0, i)
        
        #brd.reform()

        if not move:
            print(f"[AI] Checkmate Detected")
            exit()

        if i == 5 or time.process_time() - st > 1:
            print(f"Depth {i} in time {time.process_time() - st}")
            break

    print(f"[AI] Move Raw: {move}")
    print(f"[AI] Selected Move: {move[0]} {t.letter[move[1]%8]}{8-move[1]//8}")
    #format move according to GUI specification
    
    return f"{str(move[0])[2:]}{t.letter[move[1]%8]}{8-move[1]//8}"

if __name__ == '__main__':
    dflt = 'RNBQKBNRPPPPPPPP................................pppppppprnbqkbnr'
    print(getMove(dflt, 1))