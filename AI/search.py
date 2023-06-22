from AI.board import board
import AI.tables as t

#midgame search
global sum
sum = 0

global IDDFS, PVDP
IDDFS, PVDP = {}, {}

def hashCutoffAB(brd, alpha, beta):
    if (brd.brd_hash, brd.player) in PVDP:
        flag, val  = PVDP[(brd.brd_hash, brd.player)]
        if flag == 1: #precise
            return (-2, alpha, beta)
        elif flag == 2: 
            alpha = max(alpha, val)
        elif flag == 3:
            beta = min(beta, val)
        if alpha >= beta:
            return (val, alpha, beta)
    return (-2, alpha, beta)

def scoutMoves(brd):
    lst = []
    stored = None
    if (brd.brd_hash, brd.player) in IDDFS:
        stored = IDDFS[(brd.brd_hash, brd.player)]

    for p in brd.pieces[brd.player]:
        if stored and hash(p) == hash(stored[0]):
            lst.insert(0, p)
        else:
            lst.append(p)
    
    return lst


def PVS(brd, alpha, beta, depth, targetDepth):
    global sum, IDDFS, PVDP
    
    #val, alpha, beta = hashCutoffAB(brd, alpha, beta)
    # if val != -2:
    #     return val
    if (brd.brd_hash, brd.player, alpha, beta) in PVDP:
        return PVDP[(brd.brd_hash, brd.player, alpha, beta)]

    if depth == targetDepth:  
        score = brd.evaluate()
        sum += 1
        return score
    
    iterate = scoutMoves(brd)
    bestMove = None
    brd_hash = brd.brd_hash
    mg, eg, gP = brd.mg.copy(), brd.eg.copy(), brd.gP
    first = True

    for p in iterate:
        fromPos = p.index
        pM = p.findMoves(brd.state, brd.brd_hash)

        for move in pM[0]: #captures
            captured = brd.pbypos[move]
            if captured.type == 'K': return 100
            
            brd.playMove(p, move)
            
            if not first:
                score = -PVS(brd, -alpha-1, -alpha, depth+1, targetDepth)
                if alpha < score < beta:
                    cur = -PVS(brd, -beta, -cur, depth+1, targetDepth)
                first = False
            else:
                score = -PVS(brd, -beta, -alpha, depth+1, targetDepth)
            
            brd.mg, brd.eg, brd.gP = mg.copy(), eg.copy(), gP
            brd.brd_hash = brd_hash
            brd.unplayMove(p, move, fromPos, captured)
            
            if score >= beta:
                #PVDP[(brd.brd_hash, brd.player)] = (2, score)
                PVDP[(brd.brd_hash, brd.player, alpha, beta)] = score
                IDDFS[(brd.brd_hash, brd.player)] = (p, move)
                return score
            elif score > alpha:
                bestMove = (p, move)
                alpha = score

        for move in pM[1]:
            brd.playMove(p, move)

            if not first:
                score = -PVS(brd, -alpha-1, -alpha, depth+1, targetDepth)
                if alpha < score < beta:
                    cur = -PVS(brd, -beta, -cur, depth+1, targetDepth)
                first = False
            else:
                score = -PVS(brd, -beta, -alpha, depth+1, targetDepth)

            brd.mg, brd.eg, brd.gP = mg.copy(), eg.copy(), gP
            brd.brd_hash = brd_hash
            brd.unplayMove(p, move, fromPos)

            if score >= beta:
                #PVDP[(brd.brd_hash, brd.player)] = (2, score)
                PVDP[(brd.brd_hash, brd.player, alpha, beta)] = score
                IDDFS[(brd.brd_hash, brd.player)] = (p, move)
                return score
            elif score > alpha:
                bestMove = (p, move)
                alpha = score
        

    PVDP[(brd.brd_hash, brd.player, alpha, beta)] = score #(flag, score)
    IDDFS[(brd.brd_hash, brd.player)] = bestMove

    if depth == 0:
        print("Nodes", sum)
        print("Score", alpha)
        sum = 0
        IDDFS, PVDP = {}, {}

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
        
