import sys
import numpy as np
import random

# def next_move(inputString):
#     """
#     Main Function -- Initializes board and calls upon other boards
#     Returns chosen play
#     @type lastPlay: list/array
#     Note: lastPlay and moves[i] have same format, which makes it easy for recursion
#     sys.stdout.write(str(move)) will return "[c, x, y, z]"
#     """
#
#     idx = inputString.find("LastPlay:")
#     board = inputString[:idx]
#     board = board.replace('[', '').split(']')[:-1]# [:-1] removes the extra end line
#     lastPlay = inputString[idx + 9:]
#     if (lastPlay != "null"):
#         lastPlay = convert_lastPlay(lastPlay)
#
#     # 'Global' Variable for this turn
#     BOARDSIZE = len(board) - 2
#
#     # Generate the Board (3D array)
#     board = model_board(board, BOARDSIZE + 1)# BOARDSIZE + 1 = height of the board
#
#     # lastPlay & board is now parsed
#     if (lastPlay == "null"):
#         random_move(board)
#         # Make Wise First Play Here
#         sys.stderr.write("TODO: MAKE THIS WORK\n");
#
#     else:
#         # calculate all possible moves
#         moves = list_moves(lastPlay, board)
#
#     return

def list_moves(lastPlay, board):
	"""
	Define a function that lists all available next moves based on current board
	Returns all possible moves -> index the move as moves[i], color is moves[i][0]
	"""

	move_1 = [lastPlay[1]] + [lastPlay[2] - 1] + [lastPlay[3] + 1]	# upper left
	move_2 = [lastPlay[1] + 1] + [lastPlay[2] - 1] + [lastPlay[3]]	# left
	move_3 = [lastPlay[1] - 1] + [lastPlay[2]] + [lastPlay[3] + 1]	# upper right
	move_4 = [lastPlay[1] - 1] + [lastPlay[2] + 1] + [lastPlay[3]]	# right
	move_5 = [lastPlay[1] + 1] + [lastPlay[2]] + [lastPlay[3] - 1]	# lower left
	move_6 = [lastPlay[1]] + [lastPlay[2] + 1] + [lastPlay[3] - 1]	# lower right

	moves = []
	counter = 0

	if (board[move_1[0]][move_1[1]][move_1[2]] == 0):
		for i in range(1, 4):
			newMove = [[i] + move_1]
			moves += newMove
	if (board[move_2[0]][move_2[1]][move_2[2]] == 0):
		for i in range(1, 4):
			newMove = [[i] + move_2]
			moves += newMove
	if (board[move_3[0]][move_3[1]][move_3[2]] == 0):
		for i in range(1, 4):
			newMove = [[i] + move_3]
			moves += newMove
	if (board[move_4[0]][move_4[1]][move_4[2]] == 0):
		for i in range(1, 4):
			newMove = [[i] + move_4]
			moves += newMove
	if (board[move_5[0]][move_5[1]][move_5[2]] == 0):
		for i in range(1, 4):
			newMove = [[i] + move_5]
			moves += newMove
	if (board[move_6[0]][move_6[1]][move_6[2]] == 0):
		for i in range(1, 4):
			newMove = [[i] + move_6]
			moves += newMove

	return moves

def convert_lastPlay(lastPlay):
	"""
	This function converts last play into an int list to be indexed
	Returns the new lastPlay
	"""
	newLastPlay = []
	newLastPlay.append(int(lastPlay[1]))
	newLastPlay.append(int(lastPlay[3]))
	newLastPlay.append(int(lastPlay[5]))
	newLastPlay.append(int(lastPlay[7]))

	return newLastPlay

def model_board(board, boardHeight):
    """
    This function takes in the board as a list of lists & models it in x,y,z coordinates
    Returns x, y, z grid coordinates with c 
    """
    # Init 3D array to -1
    newBoard = np.full((boardHeight + 1, boardHeight + 1, boardHeight + 1), 0, dtype=int)
    
    startIdx = 1
    height = boardHeight

    for row in board:
    	# Set x, y, and z to appropriate indices
    	if (height == 0):
    		y = 1
    		x = startIdx - 1
    	else:
    		x = startIdx
    		y = 0
    	z = height

    	for color in row:
    		# Set board color and then calculate new x, y
    		newBoard[y][z][x] = color
    		x -= 1
    		y += 1

    	# Update height and start index
    	height -= 1 
    	startIdx += 1
    sys.stderr.write(str(newBoard));
    return newBoard

def game_ends(move, board):
    """
    This function checks if a move will end a game
    Note: this will also check if any in the sum of 6 is 0, because it is, then two 3's have
    	been added, which means it's not the end of the game. It also checks if 2 are the same:
    	2 + 2 + 2 is an option -> so we check that any two are not equal as well.
    Returns true or false depending on if it ends the game
    """
    sys.stderr.write(str(move)+"\n");
    # Left, UpLeft
    if (move[0] + board[move[1]+1][move[2]-1][move[3]] + board[move[1]][move[2]-1][move[3]+1] == 6):
    	if(board[move[1]+1][move[2]-1][move[3]] != 0 and board[move[1]][move[2]-1][move[3]+1] != 0 and (board[move[1]+1][move[2]-1][move[3]] != board[move[1]][move[2]-1][move[3]+1])):
    		return True
    # UpLeft, UpRight
    if (move[0] + board[move[1]][move[2]-1][move[3]+1] + board[move[1]-1][move[2]][move[3]+1] == 6):
    	if(board[move[1]][move[2]-1][move[3]+1] != 0 and board[move[1]-1][move[2]][move[3]+1] != 0 and (board[move[1]][move[2]-1][move[3]+1] != board[move[1]-1][move[2]][move[3]+1])):
    		return True
    # UpRight, Right
    if (move[0] + board[move[1]-1][move[2]][move[3]+1] + board[move[1]-1][move[2]+1][move[3]] == 6):
    	if(board[move[1]-1][move[2]][move[3]+1] != 0 and board[move[1]-1][move[2]+1][move[3]] != 0 and (board[move[1]-1][move[2]][move[3]+1] != board[move[1]-1][move[2]+1][move[3]])):
    		return True
    # Right, LowRight
    if (move[0] + board[move[1]-1][move[2]+1][move[3]] + board[move[1]][move[2]+1][move[3]-1] == 6):
    	if(board[move[1]-1][move[2]+1][move[3]] != 0 and board[move[1]][move[2]+1][move[3]-1] != 0 and (board[move[1]-1][move[2]+1][move[3]] != board[move[1]][move[2]+1][move[3]-1])):
    		return True
    # LowRight, LowLeft
    if (move[1] == 1):
        if (move[0] + board[move[1]][move[2]+1][move[3]-1] + board[move[1]+1][move[2]][move[3]-1] == 6):
        	if(board[move[1]][move[2]+1][move[3]-1] != 0 and board[move[1]+1][move[2]][move[3]-1] != 0 and (board[move[1]][move[2]+1][move[3]-1] != board[move[1]+1][move[2]][move[3]-1])):
        		return True
    else:    
        if (move[0] + board[move[1]][move[2]+1][move[3]-1] + board[move[1]+1][move[2]][move[3]-1] == 6):
        	if(board[move[1]][move[2]+1][move[3]-1] != 0 and board[move[1]+1][move[2]][move[3]-1] != 0 and (board[move[1]][move[2]+1][move[3]-1] != board[move[1]+1][move[2]][move[3]-1])):
        		return True
    # LowLeft, Left
    if (move[0] + board[move[1]+1][move[2]][move[3]-1] + board[move[1]+1][move[2]-1][move[3]] == 6):
    	if(board[move[1]+1][move[2]][move[3]-1] != 0 and board[move[1]+1][move[2]-1][move[3]] != 0 and (board[move[1]+1][move[2]][move[3]-1] != board[move[1]+1][move[2]-1][move[3]])):
    		return True
    return False

def static_eval(move, board, depth):
	"""
	Function which calculates static point for a move
	Currently, this is only based on depth and whether it ends the game
	Returns an integer
	"""

	if (game_ends(move, board)):
		# Return (50 - depth) for the score
		return (50 - depth)
	else:
		# Return 0 because nothing happens
		return 0

def update_board(move, board):
	"""
	Helper function to update the board
	Returns the new board
	@type move is [c, x, y, z]
	@type board is 3D array
	"""

	boardCopy = board
	boardCopy[move[1]][move[2]][move[3]] = move[0]

	return boardCopy

def random_move(board):
    move = [0] * 4
    move[0] = random.randint(1,3)
    move[1] = random.randint(1,BOARDSIZE)
    move[2] = random.randint(1,BOARDSIZE+1-move[1])
    move[3] = BOARDSIZE + 2 - move[1] - move[2]

    while (game_ends(move,board)):
        move[0] = random.randint(1,3)
        move[1] = random.randint(1,BOARDSIZE)
        move[2] = random.randint(1,BOARDSIZE+1-move[1])
        move[3] = BOARDSIZE + 2 - move[1] - move[2]

    sys.stdout.write("("+str(move[0])+","+str(move[1])+","+str(move[2])+","+str(move[3])+")");

    return

def do_ab(alpha, beta, lastMove, depth, maxDepth, board):
	"""
	Perform Alpha-Beta procedure (with minimax as well)
	Use game_ends() function at maxDepth to return a static value
	returns score and updates alpha/beta
	"""

	# Call Recursively until maxDepth
	# maxDepth + 1 is the layer of children of the last depth
	if (depth != maxDepth + 1):
		# Create Moves List and Call Recursively
		moves = list_moves(lastMove, board)
		for move in moves:
			score = do_ab(alpha, beta, move, depth + 1, maxDepth, update_board(move, board))
			# Maximizing Level (Try & Maximize Alpha)
			if (depth % 2 == 0):
				if (score > alpha): alpha = score
			# Minimizing Level (Try & Minimize Beta)
			else:
				if (score < beta): beta = score

	# Static Eval for maxDepth's children
	else:
		return static_eval(move, board, depth)


"""
Main Program Here
Calls next_move(sys.argv[1])
"""

# next_move(sys.argv[1])
inputString = sys.argv[1]
idx = inputString.find("LastPlay:")
board = inputString[:idx]
board = board.replace('[', '').split(']')[:-1]# [:-1] removes the extra end line
lastPlay = inputString[idx + 9:]
if (lastPlay != "null"):
    lastPlay = convert_lastPlay(lastPlay)

# 'Global' Variable for this turn
BOARDSIZE = len(board) - 2

# Generate the Board (3D array)
board = model_board(board, BOARDSIZE + 1)# BOARDSIZE + 1 = height of the board
# lastPlay & board is now parsed
# if (lastPlay == "null"):
#     random_move(board)
# # Make Wise First Play Here
# # return sys.stdout.write("TODO: MAKE THIS WORK\n")
#
# else:
# # calculate all possible moves
#     moves = list_moves(lastPlay, board)
