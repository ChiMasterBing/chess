from ChessGUI.BoardGUI import configure_board, update_board, get_player_move
from ChessGUI.chess_imports import possible_moves, make_move, print_board, kingNotInCheck
import tkinter as tk
import AI.play as bot
root = tk.Tk()

board = "RNBQKBNRPPPPPPPP................................pppppppprnbqkbnr"
players = ["USER", "USER"]

canvas = tk.Canvas(root, bg='white')

colors = ["white", "light blue"]
current = 0
for i in range(8):
    for j in range(8):
        s = canvas.create_rectangle(i*50, j*50, i*50+50, j*50+50, fill=colors[current])
        current = (current + 1)%2
    current = (current + 1)%2

canvas.pack(fill=tk.BOTH, expand=True)
allPieces = configure_board(board, canvas, root, dict(), None)

root.resizable(width=0,height=0)
root.geometry('400x400')
canvas.pack()

def game_over(board, extra, current_player):
    if len(possible_moves(board, extra, current_player)) == 0:
        return True
    return False

def winner(board, extra, current_player):
    if current_player == "W":
        pieces = "PQNBRK"
        otherPieces = pieces.lower()
    else:
        pieces = "pqnbrk"
        otherPieces = pieces.upper()
    if kingNotInCheck(board, pieces, otherPieces, pieces[5]):
        return -1
    if len(possible_moves(board, extra, current_player)) == 0:
        return "BW".index(current_player)
    return -1


def run_game(players):
    global allPieces
    board = "RNBQKBNRPPPPPPPP................................pppppppprnbqkbnr"
    pastStates = dict()
    lastPawnMove = 0
    extra = (".", True, True, True, True)
    turn = 0
    move_tracker = []  # This will track a list of moves...
    board_state_tracker = []
    while True:
        options = possible_moves(board, extra, "WB"[turn])
        allPieces = update_board(board, allPieces, canvas, root, options)
        root.update()
        if board not in pastStates:
            pastStates[board] = 0
        pastStates[board] += 1
        if pastStates[board] == 3:
            print("Game ends in a draw due to repetition!")
            return -1, move_tracker, board_state_tracker
        if lastPawnMove == 50:
            print("Game ends in a draw due to lack of activity!")
            print("(NO PAWN HAS MOVED IN THE LAST 50 MOVES)")
            return -1, move_tracker, board_state_tracker
        if game_over(board, extra, "WB"[turn]):
            win = winner(board, extra, "WB"[turn])
            if win == -1:
                print("Game ends in a draw due to stalemate!", win)
            else:
                print(players[win], "playing as", ["White", "Black"][win], "wins the game!")
            return win, move_tracker, board_state_tracker
        print("Next player:", players[turn], "playing as", "WB"[turn])
        print("Available moves are:", options)
        #---------------------------------------------
        
        
        if players[turn] == 'USER':
            move = get_player_move(board, canvas, root)
        elif players[turn] == 'AI':
            move = bot.getMove(board, turn ^ 1)
        else:
            print("Invalid Move"); exit()
        
        

        #---------------------------------------------
        if len(move) == 5:
            if "WB"[turn] == "W":
                move = move[:4] + "Q"
            else:
                move = move[:4] + "q"
        lastPawnMove += 1
        if board["abcdefgh".index(move[0]) + 8*(int(move[1]) - 1)].upper() == "P":
            lastPawnMove = 0
        board, extra = make_move(board, extra, move)
        print(extra)
        turn = 1-turn
        move_tracker.append(move)
        board_state_tracker.append(board)

# victor, moves, boards = run_game(players)
# print()
# print("All moves in order:", moves)
# root.mainloop()