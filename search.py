from board import board

#midgame search
sum = [0]

def PVS(brd, alpha, beta, depth, targetDepth):
    if depth == targetDepth:
        # print(brd.p2d())
        # print()
        sum[0] += 1

        return 0
    
    for p in brd.pieces[brd.player]:
        p.findMoves(brd.state)
        for move in (p.moves[0] | p.moves[1]):
            fromPos = p.index
            
            brd.playMove(p, move)
            score = -PVS(brd, -beta, -alpha, depth+1, targetDepth)
            brd.unplayMove(p, move, fromPos)

            #print(p, p.moves)
            
            
            # if score >= beta:
            #     return score
            # elif score > alpha:
            #     alpha = score
    
    return alpha

brd = board()
print(PVS(brd, -999, 999, 0, 5))
print(sum)

# brd.playMove(p, move)
# brd.clearUpdate(fromPos)
# brd.placeUpdate(move)
# p.findMoves(brd.state)
# score = -PVS(brd, -beta, -alpha, depth+1, targetDepth)
# brd.unplayMove(p, move, fromPos)
# brd.clearUpdate(move)
# brd.placeUpdate(fromPos)
# p.findMoves(brd.state)
