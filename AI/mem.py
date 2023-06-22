#Lookuptables, big memory
print("Initialized - Mem")

moveDP = {}

def storeMove(symbol, pos, brd_hash, moves):
    moveDP[(symbol, pos, brd_hash)] = moves

def grabMove(symbol, pos, brd_hash):
    if (symbol, pos, brd_hash) in moveDP:
        return moveDP[(symbol, pos, brd_hash)]
    return None


