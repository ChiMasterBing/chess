import random
k_moves = [-11, -10, -9, -1, 1, 9, 10, 11]
b_moves = [-11,-9,9,11]
r_moves = [-10,-1,1,10]
n_moves = [-21, -19, -12, -8, 8, 12, 19, 21]

default = "RNBQKBNRPPPPPPPP................................pppppppprnbqkbnr"
letters = "abcdefgh"
numbers = "12345678"
test = "RNBQKBNRPpPPPPPP................................pppppPpprnbqkbnr"
peeces = "RNBQ"
peeeces = "rnbq"

def print_board(board):
    size = int(len(board)**0.5)
    print("+ a b c d e f g h +")
    for i in range(size):
        i = size - i - 1
        s = ""
        for j in range(size):
            h = board[i*size+j]
            if(h=="k"):
                h="♚"
            elif(h=="n"):
                h ="♞"
            elif(h=="r"):
                h ="♜"
            elif(h=="q"):
                h="♛"
            elif(h=="b"):
                h="♝"
            elif(h=="p"):
                h="♟︎"
            elif(h=="K"):
                h="♔"
            elif(h=="N"):
                h ="♘"
            elif(h=="R"):
                h ="♖"
            elif(h=="Q"):
                h="♕"
            elif(h=="B"):
                h="♗"
            elif(h=="P"):
                h="♙"
            s+=h+" "
        print(str(i+1) + " " + s + " " + str(i+1))
    print("+ a b c d e f g h +")
    print()

def token_convert(token):
    return int(token == "W")*2-1

def get_token(piece):
    if(piece == "."):
        return 0
    elif(piece == "?"):
        return 2
    return int(piece.upper() == piece)*2-1

def index_to_coords(index):
    return letters[index%8] + numbers[index//8]

def convert_10i_to_8i(i):
    return 8*(i//10-1)+i%10-1

def convert_8i_to_10i(index):
    return 10*(index//8+1)+index%8+1

def convert_board(board):
    new_board = "??????????"
    for i in range(8):
        new_board+="?"
        for j in range(8):
            new_board+=board[i*8+j]
        new_board+="?"
    new_board+="??????????"
    return new_board

def convert_back(board):
    new_board = ""
    for i in range(8):
        for j in range(8):
            new_board += board[10*(i+1)+j+1]
    return new_board

def make_moves(board, board8, token, index, extra):
    coord = index_to_coords(index)
    i10 = convert_8i_to_10i(index)
    moves = []
    piece = board[i10]
    if(token == get_token(piece)):
        upiece = piece.upper()
        if(upiece == "K"):
            if(not(isCheck(board, token))):
                if(token == 1):
                    if(extra[2] and board[i10+1] == "." and board[i10+2] == "." and not isCheck(convert_board(make_move(board8, extra, "e1f1")[0]), token)):
                        moves.append("e1g1")
                    if(extra[1] and board[i10-1] == "." and board[i10-2] == "." and board[i10-3] == "." and not isCheck(convert_board(make_move(board8, extra, "e1d1")[0]), token)):
                        moves.append("e1c1")
                elif(token == -1):
                    if(extra[4] and board[i10+1] == "." and board[i10+2] == "." and not isCheck(convert_board(make_move(board8, extra, "e8f8")[0]), token)):
                        moves.append("e8g8")
                    if(extra[3] and board[i10-1] == "." and board[i10-2] == "." and board[i10-3] == "." and not isCheck(convert_board(make_move(board8, extra, "e8d8")[0]), token)):
                        moves.append("e8c8")

            for move in k_moves:
                n_i = i10 + move
                if(n_i>=0 and n_i<100):
                    npiece = board[n_i]
                    ntoken = get_token(npiece)
                    if(npiece == "." or ntoken == token*-1):
                        moves.append(coord + index_to_coords(convert_10i_to_8i(n_i)))
        elif(upiece == "N"):
            for move in n_moves:
                n_i = i10 + move
                if(n_i>=0 and n_i<100):
                    npiece = board[n_i]
                    ntoken = get_token(npiece)
                    if(not(ntoken == 2 or ntoken == token)):
                        moves.append(coord + index_to_coords(convert_10i_to_8i(n_i)))
        elif(upiece == "P"):
            if(token == 1):
                ntoken = get_token(board[i10+10])
                if(board[i10+10]=="."):
                    if(index//8==6):
                        for b in peeces:
                            moves.append(coord + index_to_coords(convert_10i_to_8i(i10+10))+b)
                    else:
                        moves.append(coord + index_to_coords(convert_10i_to_8i(i10+10)))
                        if(index//8==1):
                            if(board[i10+20]=="."):
                                moves.append(coord + index_to_coords(convert_10i_to_8i(i10+20)))
                if(index//8==4 and extra):
                    thing = letters.index(extra[0]) - index%8
                    if(abs(thing)==1):
                        moves.append(coord + index_to_coords(convert_10i_to_8i(i10+10+thing)))
                ntoken = get_token(board[i10+11])
                if(ntoken == token*-1):
                    if(index//8==6):
                        for b in peeces:
                            moves.append(coord + index_to_coords(convert_10i_to_8i(i10+11))+b)
                    else:
                        moves.append(coord + index_to_coords(convert_10i_to_8i(i10+11)))
                ntoken = get_token(board[i10+9])
                if(ntoken == token*-1):
                    if(index//8==6):
                        for b in peeces:
                            moves.append(coord + index_to_coords(convert_10i_to_8i(i10+9))+b)
                    else:
                        moves.append(coord + index_to_coords(convert_10i_to_8i(i10+9)))
            else:
                ntoken = get_token(board[i10-10])
                if(board[i10-10]=="."):
                    if(index//8==1):
                        for b in peeeces:
                            moves.append(coord + index_to_coords(convert_10i_to_8i(i10-10))+b)
                    else:
                        moves.append(coord + index_to_coords(convert_10i_to_8i(i10-10)))
                        if(index//8==6):
                            if(board[i10-20]=="."):
                                moves.append(coord + index_to_coords(convert_10i_to_8i(i10-20)))
                if(index//8==3 and extra):
                    thing = letters.index(extra[0]) - index%8
                    if(abs(thing)==1):
                        moves.append(coord + index_to_coords(convert_10i_to_8i(i10-10+thing)))
                ntoken = get_token(board[i10-11])
                if(ntoken == token*-1):
                    if(index//8==1):
                        for b in peeeces:
                            moves.append(coord + index_to_coords(convert_10i_to_8i(i10-11))+b)
                    else:
                        moves.append(coord + index_to_coords(convert_10i_to_8i(i10-11)))
                ntoken = get_token(board[i10-9])
                if(ntoken == token*-1):
                    if(index//8==1):
                        for b in peeeces:
                            moves.append(coord + index_to_coords(convert_10i_to_8i(i10-9))+b)
                    else:
                        moves.append(coord + index_to_coords(convert_10i_to_8i(i10-9)))
        elif(upiece == "B"):
            for move in b_moves:
                nindex = i10+move
                npiece = board[nindex]
                while(npiece=="."):
                    moves.append(coord + index_to_coords(convert_10i_to_8i(nindex)))
                    nindex += move
                    npiece = board[nindex]
                if(get_token(npiece) == token*-1):
                    moves.append(coord + index_to_coords(convert_10i_to_8i(nindex)))
        elif(upiece == "Q"):
            for move in k_moves:
                nindex = i10+move
                npiece = board[nindex]
                while(npiece=="."):
                    moves.append(coord + index_to_coords(convert_10i_to_8i(nindex)))
                    nindex += move
                    npiece = board[nindex]
                if(get_token(npiece) == token*-1):
                    moves.append(coord + index_to_coords(convert_10i_to_8i(nindex)))
        elif(upiece == "R"):
            for move in r_moves:
                nindex = i10+move
                npiece = board[nindex]
                while(npiece=="."):
                    moves.append(coord + index_to_coords(convert_10i_to_8i(nindex)))
                    nindex += move
                    npiece = board[nindex]
                if(get_token(npiece) == token*-1):
                    moves.append(coord + index_to_coords(convert_10i_to_8i(nindex)))
    moves = [move for move in moves if(not isCheck(convert_board(make_move(board8, extra, move)[0]), token))]
    return moves
    #moves.append(index_to_coords(index) + index_to_coords())

def kingNotInCheck(board, pieces, otherPieces, king):
    return not(isCheck(board, ("kK".index(king))*2-1))

def isCheck(board, token):
    if(len(board)!=100):
        board = convert_board(board)
    if(token == 1):
        king = "K"
    else:
        king = "k"
    i10 = board.index(king)
    for move in r_moves:
            nindex = i10+move
            npiece = board[nindex]
            while(npiece=="."):
                nindex += move
                npiece = board[nindex]
            if(get_token(npiece) == token*-1 and npiece.lower() in "rq"):
                return True
    for move in b_moves:
            nindex = i10+move
            npiece = board[nindex]
            while(npiece=="."):
                nindex += move
                npiece = board[nindex]
            if(get_token(npiece) == token*-1 and npiece.lower() in "bq"):
                return True
    for move in n_moves:
            nindex = i10+move
            if(nindex>=0 and nindex<100):
                npiece = board[nindex]
                if(get_token(npiece) == token*-1 and npiece.lower() == "n"):
                    return True
    for move in k_moves:
            nindex = i10+move
            if(nindex>=0 and nindex<100):
                npiece = board[nindex]
                if(get_token(npiece) == token*-1 and npiece.lower() == "k"):
                    return True
    for i in [-1, 1]:
            nindex = i10+10*token+i
            npiece = board[nindex]
            if(get_token(npiece) == token*-1 and npiece.lower() == "p"):
                return True
    return False

def possible_moves(board, extra, token):
    new_board = convert_board(board)
    all_moves = []
    n_token = token_convert(token)
    for i in range(64):
        moves = make_moves(new_board, board, n_token, i, extra)
        for m in moves:
            all_moves.append(m)
    return all_moves

def make_move(board, extra, coords):
    if(coords == "e1g1"):
        extra = ("", False, False, extra[3], extra[4])
        return board[:4] + ".RK." + board[8:], extra
    elif(coords == "e1c1"):
        extra = ("", False, False, extra[3], extra[4])
        return "..KR." + board[5:], extra
    elif(coords == "e8g8"):
        extra = ("", extra[1], extra[2], False, False)
        return board[:60] + ".rk.", extra
    elif(coords == "e8c8"):
        extra = ("", extra[1], extra[2], False, False)
        return board[:56] + "..kr." + board[61:], extra
    index1 = letters.index(coords[0]) + (int(coords[1])-1)*8
    index2 = letters.index(coords[2]) + (int(coords[3])-1)*8
    piece = board[index1]
    if(piece == "K"):
        extra = ("", False, False, extra[3], extra[4])
    elif(piece == "k"):
        extra = ("", extra[1], extra[2], False, False)
    elif(piece == "R"):
        if(index1 == 7):
            extra = ("", extra[1], False, extra[3], extra[4])
        elif(index1 == 0):
            extra = ("", False, extra[2], extra[3], extra[4])
    elif(piece == "r"):
        if(index1 == 63):
            extra = ("", extra[1], extra[2], extra[3], False)
        elif(index1 == 56):
            extra = ("", extra[1], extra[2], False, extra[4])
    elif(piece.lower() == "p"):
        if(abs(index1-index2)==16):
            extra = (coords[0], extra[1], extra[2], extra[3], extra[4])
        elif(abs(abs(index1-index2)-8)==1):
            extra = ("", extra[1], extra[2], extra[3], extra[4])
            if(board[index2]=="."):
                if(piece == "P"):
                    board =  board[:index2-8] + "." + board[index2-7:]
                else:
                    board =  board[:index2+8] + "." + board[index2+9:]
                if(index1<index2):
                    return board[:index1] + "." + board[index1+1:index2] + piece + board[index2+1:], extra
                return board[:index2] + piece + board[index2+1:index1] + "." + board[index1+1:], extra
                
        else:
            extra = ("", extra[1], extra[2], extra[3], extra[4])
    if(len(coords)==5):
        piece = coords[4]
    if(index1<index2):
        return board[:index1] + "." + board[index1+1:index2] + piece + board[index2+1:], extra
    return board[:index2] + piece + board[index2+1:index1] + "." + board[index1+1:], extra

def game_over(board):
    if("k" not in board or "K" not in board):
        return True
    return False

