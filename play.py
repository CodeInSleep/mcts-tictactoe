from utils import checkBoardStatus, Board

initState = ("0 1 2 "
						 "0 1 2 "
						 "0 1 0")

b = Board(initState, 1)
print(checkBoardStatus(b, 1))

