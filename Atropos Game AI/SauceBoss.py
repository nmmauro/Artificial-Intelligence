"""
Khai Phan, Michael Deng, Nick Mauro
Programming Assignment 3
Due: 4/27/17
"""

import sys
import numpy as np
import re

def next_move(inputString):
	"""
	Main Function -- Initializes board and calls upon other boards
	Returns chosen play
	@type lastPlay: list/array
	Note: lastPlay and moves[i] have same format, which makes it easy for recursion
		sys.stdout.write(str(move)) will return "[c, x, y, z]"
	"""
	
	idx = inputString.find("LastPlay:")
	board = inputString[:idx]
	board = board.replace('[', '').split(']')[:-1]	# [:-1] removes the extra end line					
	lastPlay = inputString[idx + 9:]
	if (lastPlay != "null"):
		lastPlay = convert_lastPlay(lastPlay)

	# 'Global' Variable for this turn
	BOARDSIZE = len(board) - 2
	DEPTH = BOARDSIZE + 2

	# Generate the Board (3D array)
	board = model_board(board, BOARDSIZE + 1)	# BOARDSIZE + 1 = height of the board

	# lastPlay & board is now parsed
	if (lastPlay == "null" or (len(list_moves(lastPlay, board)) == 0)):
		# Make Wise Free Play Here
		msg = do_ab(-10000, 10000, "null", 0, DEPTH * 2, board)
		sys.stdout.write("(" + str(msg[0]) + "," + str(msg[1]) + "," + str(msg[2]) + "," + str(msg[3]) + ")")
	else:
		# calculate all possible moves
		msg = do_ab(-10000, 10000, lastPlay, 0, DEPTH, board)
		# sys.stdout.write(str(game_ends(msg, board)) + '\n')
		sys.stdout.write("(" + str(msg[0]) + "," + str(msg[1]) + "," + str(msg[2]) + "," + str(msg[3]) + ")")
	
	return

def list_moves(lastPlay, board):
	"""
	Define a function that lists all available next moves based on current board
	Returns all possible moves -> index the move as moves[i], color is moves[i][0]
	"""

	move_1 = [lastPlay[1] + 1] + [lastPlay[2] - 1] + [lastPlay[3]]	# upper left
	move_2 = [lastPlay[1]] + [lastPlay[2] - 1] + [lastPlay[3] + 1]	# left
	move_3 = [lastPlay[1] + 1] + [lastPlay[2]] + [lastPlay[3] - 1]	# upper right
	move_4 = [lastPlay[1]] + [lastPlay[2] + 1] + [lastPlay[3] - 1]	# right
	move_5 = [lastPlay[1] - 1] + [lastPlay[2]] + [lastPlay[3] + 1]	# lower left
	move_6 = [lastPlay[1] - 1] + [lastPlay[2] + 1] + [lastPlay[3]]	# lower right

	moves = []

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

	lastPlay = lastPlay.replace('(', '')
	lastPlay = lastPlay.replace(')', '')
	lastPlay = lastPlay.split(',')

	newLastPlay = []
	newLastPlay.append(int(lastPlay[0]))
	newLastPlay.append(int(lastPlay[1]))
	newLastPlay.append(int(lastPlay[2]))
	newLastPlay.append(int(lastPlay[3]))

	return newLastPlay

def model_board(board, boardHeight):
	"""
	This function takes in the board as a list of lists & models it in x,y,z coordinates
	Returns x, y, z grid coordinates with c 
	"""

	# Init 3D array to -1
	newBoard = np.full((boardHeight + 1, boardHeight + 1, boardHeight + 1), -1, dtype=int)

	startIdx = 1
	height = boardHeight

	for row in board:
		# Set x, y, and z to appropriate indices
		if (height == 0):
			y = 1
			z = startIdx - 1
		else:
			z = startIdx
			y = 0
		x = height

		for color in row:
			# Set board color and then calculate new x, y
			newBoard[x][y][z] = color
			z -= 1
			y += 1

		# Update height and start index
		height -= 1 
		startIdx += 1

	return newBoard

def game_ends(move, board):
	"""
	This function checks if a move will end a game
	Note: this will also check if any in the sum of 6 is 0, because it is, then two 3's have
		been added, which means it's not the end of the game. It also checks if 2 are the same:
		2 + 2 + 2 is an option -> so we check that any two are not equal as well.
	Returns true or false depending on if it ends the game
	"""
	# Left, UpLeft
	if (move[0] + board[move[1]][move[2]-1][move[3]+1] + board[move[1]+1][move[2]-1][move[3]] == 6):
		if(board[move[1]][move[2]-1][move[3]+1] != 0 and board[move[1]+1][move[2]-1][move[3]] != 0
			and (board[move[1]][move[2]-1][move[3]+1] != board[move[1]+1][move[2]-1][move[3]])):
			return True
	# Left, LowLeft
	if (move[0] + board[move[1]][move[2]-1][move[3]+1] + board[move[1]-1][move[2]][move[3]+1] == 6):
		if(board[move[1]][move[2]-1][move[3]+1] != 0 and board[move[1]-1][move[2]][move[3]+1] != 0
			and (board[move[1]][move[2]-1][move[3]+1] != board[move[1]-1][move[2]][move[3]+1])):
			return True
	# LowLeft, LowRight
	if (move[0] + board[move[1]-1][move[2]][move[3]+1] + board[move[1]-1][move[2]+1][move[3]] == 6):
		if(board[move[1]-1][move[2]][move[3]+1] != 0 and board[move[1]-1][move[2]+1][move[3]] != 0
			and (board[move[1]-1][move[2]][move[3]+1] != board[move[1]-1][move[2]+1][move[3]])):
			return True
	# LowRight, Right
	if (move[0] + board[move[1]-1][move[2]+1][move[3]] + board[move[1]][move[2]+1][move[3]-1] == 6):
		if(board[move[1]-1][move[2]+1][move[3]] != 0 and board[move[1]][move[2]+1][move[3]-1] != 0
			and (board[move[1]-1][move[2]+1][move[3]] != board[move[1]][move[2]+1][move[3]-1])):
			return True
	# Right, UpRight
	if (move[0] + board[move[1]][move[2]+1][move[3]-1] + board[move[1]+1][move[2]][move[3]-1] == 6):
		if(board[move[1]][move[2]+1][move[3]-1] != 0 and board[move[1]+1][move[2]][move[3]-1] != 0
			and (board[move[1]][move[2]+1][move[3]-1] != board[move[1]+1][move[2]][move[3]-1])):
			return True
	# UpRight, UpLeft
	if (move[0] + board[move[1]+1][move[2]][move[3]-1] + board[move[1]+1][move[2]-1][move[3]] == 6):
		if(board[move[1]+1][move[2]][move[3]-1] != 0 and board[move[1]+1][move[2]-1][move[3]] != 0
			and (board[move[1]+1][move[2]][move[3]-1] != board[move[1]+1][move[2]-1][move[3]])):
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
		return (-1 * (50 - depth))
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

def do_ab(alpha, beta, lastMove, depth, maxDepth, board):
	"""
	Perform Alpha-Beta procedure (with minimax as well)
	Use game_ends() function at maxDepth to return a static value
	returns score and updates alpha/beta
	"""

	# Always create a list of available moves based on the board
	# Create it based on previous play, or if none, based on available spots
	if (lastMove == "null"):
		moves = gen_all_plays(board, len(board) - 1)
	else:
		moves = list_moves(lastMove, board)	

	# If depth = 0, this is the root (the next move)
	# We want to make a bestMove return value for this and then
	# recursively call do_ab() on all of the moves
	# Once do_ab() returns, we can return the bestMove
	if (depth == 0):
		bestMove = moves[0]	# init to first child
		for move in moves:
			# Calculate the score and then update alpha for this depth (we only care about alpha)
			if(not game_ends(move, board)):
				score = do_ab(alpha, beta, move, depth + 1, maxDepth, update_board(move, board))
				if (score >= alpha):
					alpha = score
					bestMove = move
		return bestMove

	# Else, let's do Alpha-Beta
	if ((depth != 0) and (depth != (maxDepth + 1))):
		# Maximize this alpha and then return to the previous beta
		if (depth % 2 == 0):
			for move in moves:
				# recursively go down the tree and update alpha/beta
				score = do_ab(alpha, beta, move, depth + 1, maxDepth, update_board(move, board))
				if (score > alpha):
					alpha = score
				if (alpha >= beta):
					return alpha
			return alpha

		# Minimize this beta and then return to the previous alpha
		else:
			for move in moves:
				# recursively go down the tree and update alpha/beta
				score = do_ab(alpha, beta, move, depth + 1, maxDepth, update_board(move, board))
				if (score < beta):
					beta = score
				if (alpha >= beta):
					return beta
			return beta
	# if depth = maxDepth + 1, these are the lowest depth's children
	elif (depth == maxDepth + 1):
		return static_eval(lastMove, board, depth)

def gen_all_plays(board, boardLen):
	"""
	Function returns a play which is not completely random
	"""

	moves = []

	for x in range(1, boardLen):
		for y in range(1, boardLen):
			for z in range(1, boardLen):
				if (board[x][y][z] == 0):
					for c in range(1, 4):
						moves += [[c] + [x] + [y] + [z]]

	return moves

"""
Main Program Here
Calls next_move(sys.argv[1])
"""

next_move(sys.argv[1])