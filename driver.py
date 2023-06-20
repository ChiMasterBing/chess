import ChessGUI.ChessGUI_Example as GUI
#import AI.play as bot

print("Finished Loading Imports")

DEFAULT_BOARD = 'RNBQKBNRPPPPPPPP................................pppppppprnbqkbnr'
PLAYERS = ['USER', 'AI']

victor, moves, boards = GUI.run_game(PLAYERS)
# print()
# print("All moves in order:", moves)
exit()