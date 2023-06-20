from AI.board import board
import AI.tables as t

#midgame search
sum = [0]

def PVS(brd, alpha, beta, depth, targetDepth):
    if depth == targetDepth:  
        score = brd.evaluate()
        sum[0] += 1
        return score
    
    bestMove = None
        
    iterate = [p for p in brd.pieces[brd.player]]
    for p in iterate:
        pM = p.findMoves(brd.state)
        for move in pM[0]: #captures
            fromPos = p.index
            
            captured = brd.pbypos[move]
            
            if captured.type == 'K': return 100
            
            brd.pieces[p.team ^ 1].remove(captured)
            brd.playMove(p, move)

            score = -PVS(brd, -beta, -alpha, depth+1, targetDepth)
            brd.unplayMove(p, move, fromPos, captured)
            
            if score >= beta:
                return score
            elif score > alpha:
                bestMove = (p, move)
                alpha = score

        for move in pM[1]:
            fromPos = p.index
            
            brd.playMove(p, move)
            score = -PVS(brd, -beta, -alpha, depth+1, targetDepth)
            brd.unplayMove(p, move, fromPos)

            if score >= beta:
                return score
            elif score > alpha:
                bestMove = (p, move)
                alpha = score
    
    if depth == 0:
        print(alpha)
    return alpha if depth != 0 else bestMove



if __name__== "__main__":
    #ss = 'RNBQKBNRPPPP.PPP............P........p..........ppppp.pprnbqkbnr'
    #ss = 'RNB.KBNRPPPP.PPP............P......p.ppQ........ppp.p..prnbqkbnr'
    #ss = 'RNB.K.NRPPPPBPPP............p..........Q......p.ppppp..prnbqkbnr'
    #ss = 'RNB.K.NRPPPPBPPP............p..........p........ppppp..prnbqkbnr'
    #ss = 'R.B.K.NRPPPPBPPP..N.........p.......Q........npbppppp..prnbqk..r'
    #ss = 'RNBQKBNRPPPP.PPP...................P..........p.ppp.pp.prnbqkbnr'
    brd = board()
    brd.player = 1
    print(brd.p2d())
    while True:
        brd = board(brd.state)
        print("player:", brd.player)
        tpl = PVS(brd, -999, 999, 0, 6)
        
        if not tpl:
            print("Checkmate"); exit()

        print(tpl[0], f"{t.letter[tpl[1]%8]}{8-tpl[1]//8}", tpl[1])
        print(sum)

        brd.playMove(tpl[0], tpl[1])
        print(brd.p2d())
        exit()
        #print(brd.state)

        move = input().split(" ")
        i1 = t.letter.index(move[0][0]) + 8*(8-int(move[0][1]))
        i2 = t.letter.index(move[1][0]) + 8*(8-int(move[1][1]))

        for p in brd.pieces[brd.player]:
            if p.index == i1:
                brd.playMove(p, i2)
                break
        
        print(brd.p2d())
        print(brd.state)
        
