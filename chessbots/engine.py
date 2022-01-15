import copy
import chess
import chess.pgn
import random

# May raise error if headers is not full
def StartClassicGame(players, headers): # players, event):
	board = chess.Board()
	game = chess.pgn.Game()

	white, black = players
	if random.randint(0, 1): white, black = black, white

	white.StartNewGame(board, chess.WHITE)
	black.StartNewGame(board, chess.BLACK)

	# game.headers = headers

	game.headers["Event"] = str(headers["Event"])
	game.headers["White"] = str(white.name)
	game.headers["Black"] = str(black.name)
	game.headers["Site"] = str(headers["Site"])
	game.headers["Date"] = str("Date")
	game.headers["Round"] = str(headers["Round"])

	game.setup(board)
	node = game
	error = None

	moveIndex = 1
	while not board.outcome():
		try:
			white.Move()
			node = node.add_variation(board.peek())
			if board.outcome(): break
			black.Move()
			node = node.add_variation(board.peek())
		except Exception as e:
			error = e
			break

		moveIndex += 1

	return game, board, error, moveIndex

# Launching a chess game between 2 bots
# Parameters: board(chess.Board), 
# 				players(tuple of 2 classes)(tuple of 2 players of custom class in the previous version),
# 				eventName(str),
# 				site(str),
# 				date(str),
# 				roundNumber(str)
# Returns: tuple(game(chess.pgn.Game), board(chess.Board), error(Exception), moveIndex(int))
def LaunchGame(board, players, eventName, site, date, roundNumber=1):
	board = copy.deepcopy(board)
	game = chess.pgn.Game()

	white, black = players
	if random.randint(0, 1): white, black = black, white

	white = white()

	game.headers["Event"] = str(eventName)
	game.headers["White"] = str(white.botName)
	game.headers["Black"] = str(black.botName)
	game.headers["Site"] = str(site)
	game.headers["Date"] = str(date)
	game.headers["Round"] = str(roundNumber)

	game.setup(board)
	node = game
	error = None

	moveIndex = 1
	while not board.outcome():
		try:
			white.Move()
			node = node.add_variation(board.peek())
			if board.outcome(): break
			black.Move()
			node = node.add_variation(board.peek())
		except Exception as e:
			error = e
			break

		moveIndex += 1

	return game, board, error, moveIndex