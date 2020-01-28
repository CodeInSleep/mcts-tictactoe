"""
Classes:
- State
- Node
- Board

pseudocode:
At each turn:
	Variables
	=== 
	current player's move
	current state of the 

	Routine (run in a certain time threshold)
	===
	1. Selection Phase
		select the child node C of the root node that has the
		highest UCT score
	2. Expansion Phase
		Enumerate all the possible moves from the node C
	3. Pick a random children from the expansion phase
		and run simulation (random play) starting form that
		child's state
	4. Back Prop Phase
		only the winner is creidted with the win by adding 1
		to winNo, and 0.5 for ties.
		playNo is incremented fromt one simulation trial.		 
"""

import random

BOARD_SIZE = 3

def checkBoardStatus(board, playerNo):
	# checks if the board state is over, returns
	# 	-1: not over
	# 	0: tie
	# 	1: player 1 wins
	# 	2: player 2 wins
	
	# check if there is a winning row/column/diagonal
	solutions = []
	for i in range(BOARD_SIZE):
		colSol = [[i, j] for j in range(BOARD_SIZE)]
		rowSol = [[j, i] for j in range(BOARD_SIZE)]
		solutions.append(colSol)
		solutions.append(rowSol)

	solutions.append([[i, i] for i in range(BOARD_SIZE)])
	solutions.append([[BOARD_SIZE-1-i, i] for i in range(BOARD_SIZE)])

	won = False
	for sol in solutions:
		# if all symbols in solution coordinates are the same then
		# the player with the symbol has won
		allMatch = True	
		for coord in sol:
			if board.state.boardConfig[coord[0]][coord[1]] != playerNo:
				allMatch = False
		if allMatch:
			won = True
			break
	
	# if no one won, the game continues if there is more to play
	# else it is a tie.
	if won:
		return playerNo

	return 0 if board.state.terminated else -1

class State:
	def __init__(self, boardConfig):
		if isinstance(boardConfig, str):
			# parse string into state (string describes state of board
			# from left to right, from up to down
			boardConfig = [int(c) for c in boardConfig.split(' ')]
		elif isinstance(boardConfig, list):
			if all(isinstance(x, list) for x in boardConfig):
				# flatten 2D board config
				boardConfig = [ele for x in boardConfig for ele in x]

		assert len(boardConfig) == BOARD_SIZE*BOARD_SIZE
	
		self.boardConfig = [[boardConfig[i*BOARD_SIZE+j] 
			for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]
		
		# check if the board state is the end
		terminated = True
		for i in boardConfig:
			# check for empty spots
			if boardConfig[i] == 0:
				terminated = False
		# TODO: move to State object of the board when State is implemented
		self.terminated = terminated

		# statistics for upper confidence bound algorithm function
		self.winCounts = 0
		self.totalCount = 0

class Coords:
	def __init__(self, r, c):
		self.r = r
		self.c = c

class Board:
	def __init__(self, currState, playerTurn):
		self.playerTurn = playerTurn
		self.state = State(currState)				
	
class Node:
	def __init__(self, currState, playerTurn, parent=None):
		self.parent = parent
		self.children = []
		self.board = Board(currState, playerTurn)

	def randPlay(self, num=1):
		# check that position is playable
		if self.board.state.terminated:
			return 
		
		availPos = []
		for r in range(BOARD_SIZE):
			for c in range(BOARD_SIZE):
				if self.board.state[r][c] == 0:
					availPos.append(Coords(r, c))
		# randomly play a position
		num = min([num, len(availPos)])	
		randIdxs = random.sample(range(len(avail)), num)
		
		outcomes = []
		for idx in randIdxs:
			randPlay = availPos[idx]
		
			newState = [x[:] for x in self.board.state]
			newState[randPlay.r][randPlay.c] = self.playerTurn

			outcomes.append(Node(newState, self.nextPlayer(self.playerTurn), parent=self))
	
		return outcomes
		
	def nextPlayer(self, currPlayer):
		return 3 - currPlayer

# randomly playout from board's current state
def rollout(leafNode):
	while not leafNode.state.terminated:
		leafNode = leafNode.randPlay()
