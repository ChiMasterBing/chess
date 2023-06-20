import tkinter as tk
from chess_imports import possible_moves, make_move
pastMoves = set()
pieceMoving = ""

def update_board(board, allPieces, canvas, root, theMovesPossible):
    global moveMade
    moveMade = tk.IntVar()
    for piece in allPieces:
        piece.destroy()
    theMovesPossible = make_possible_moves(theMovesPossible)
    return configure_board(board, canvas, root,  theMovesPossible, moveMade)

def configure_board(board, canvas, root, everyMove, moveMade):
    blackPawn = tk.PhotoImage(file = "blackPawn.png")
    blackKing = tk.PhotoImage(file = "blackKing.png")
    blackQueen = tk.PhotoImage(file = "blackQueen.png")
    blackKnight = tk.PhotoImage(file = "blackKnight.png")
    blackBishop = tk.PhotoImage(file = "blackBishop.png")
    blackRook = tk.PhotoImage(file = "blackRook.png")
    whitePawn = tk.PhotoImage(file = "whitePawn.png")
    whiteKing = tk.PhotoImage(file = "whiteKing.png")
    whiteQueen = tk.PhotoImage(file = "whiteQueen.png")
    whiteKnight = tk.PhotoImage(file = "whiteKnight.png")
    whiteBishop = tk.PhotoImage(file = "whiteBishop.png")
    whiteRook = tk.PhotoImage(file = "whiteRook.png")
    allPieces = set()
    for i in range(0, 64, 8):
        for j in range(8):
            piece = board[i + j]
            if piece != ".":
                coordToCheck = getCoords(i + j)
                if (coordToCheck in everyMove):
                    button = tk.Button(root, command=lambda coordToCheck=coordToCheck: make_button_moves(canvas, root, coordToCheck, everyMove[coordToCheck], moveMade))
                else:
                    button = tk.Button(root)
                if piece == "p":
                    button.image = blackPawn
                    button.config(image = blackPawn)
                if piece == "k":
                    button.image = blackKing
                    button.config(image = blackKing)
                if piece == "q":
                    button.image = blackQueen
                    button.config(image = blackQueen)
                if piece == "n":
                    button.image = blackKnight
                    button.config(image = blackKnight)
                if piece == "r":
                    button.image = blackRook
                    button.config(image = blackRook)
                if piece == "b":
                    button.image = blackBishop
                    button.config(image = blackBishop)
                if piece == "P":
                    button.image = whitePawn
                    button.config(image = whitePawn)
                if piece == "K":
                    button.image = whiteKing
                    button.config(image = whiteKing)
                if piece == "Q":
                    button.image = whiteQueen
                    button.config(image = whiteQueen)
                if piece == "N":
                    button.image = whiteKnight
                    button.config(image = whiteKnight)
                if piece == "R":
                    button.image = whiteRook
                    button.config(image = whiteRook)
                if piece == "B":
                    button.image = whiteBishop
                    button.config(image = whiteBishop)
                button.place(relx=j*.125, rely=.875 - i/64, height=50, width=50)
                allPieces.add(button)
    return allPieces

def make_button_moves(canvas, root, ogSquare, allMovesForPiece, moveMade):
    global pastMoves, pieceMoving
    deletePastMoves()
    if pieceMoving != ogSquare:
        for move in allMovesForPiece:
            theMove = getIndex(move)
            wholeMove = ogSquare + move
            button = tk.Button(root, command=lambda wholeMove=wholeMove: the_move_made(moveMade, wholeMove))
            button.place(relx=(theMove%8)*.125, rely=.875 - (theMove//8)*.125, height=50, width=50)
            pastMoves.add(button)
        pieceMoving = ogSquare
    else:
        pieceMoving = ""
    canvas.pack()

def get_player_move(board, canvas, root):
    global toReturn
    global moveMade
    root.wait_variable(moveMade)
    deletePastMoves()
    return toReturn

def deletePastMoves():
    global pastMoves
    for theMoveThingy in pastMoves:
        theMoveThingy.destroy()
    pastMoves = set()

def the_move_made(moveMade, wholeMove):
    global toReturn
    toReturn = wholeMove
    moveMade.set(wholeMove)
#blackPawn = blackPawn.subsample(blackPawn.width() // 50, blackPawn.height() // 50)
#subsample shrinks the thing. Very good, very good
def getIndex(index):
    positions = "abcdefgh"
    return positions.index(index[0]) + 8*(int(index[1]) - 1)

def getCoords(index):
    rowIndex = "abcdefgh"
    return rowIndex[index % 8] + str(index // 8 + 1)

def make_possible_moves(allMoves):
    eachPiecesMoves = dict()
    for moves in allMoves:
        if moves[:2] not in eachPiecesMoves:
            eachPiecesMoves[moves[:2]] = set()
        eachPiecesMoves[moves[:2]].add(moves[2:])
    return eachPiecesMoves

def which_button(button_press):
    make_possible_moves("asdf")
    pastIndex = getIndex(int(button_press))