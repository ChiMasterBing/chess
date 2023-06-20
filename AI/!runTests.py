from AI.board import board

def testFindMoves():
    f = open("tests/findMoves.txt").readlines()
    for i in range(0, len(f), 4):
        name, start, end, pieceCount = f[i].strip(), f[i+1].strip(), f[i+2].strip(), int(f[i+3])
        brd = board(start)
        out = str(brd).replace('\n', '')
        assert len(brd.state) == 64, "board size error"
        assert len(brd.pieces[0]) + len(brd.pieces[1]) == pieceCount, "piece count error"
        assert out == end, f"\noriginal: {start}\noutput:   {out}\ncorrect:  {end}"
        print(f"FindMoves - {name} - Nominal")

def testPlayMoves():
    brd = board()
    choice = None
    for p in brd.pieces[0]:
        if p.type == 'N':
            choice = p

    print(choice, choice.moves)
    brd.playMove(choice, 21)
    print(brd)


    
testFindMoves()   
testPlayMoves()