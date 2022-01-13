import copy
import chess
import random

# Launching a chess game between 2 bots
# Parameters: board(chess.Board), 
# 				players(tuple of 2 players of custom class),
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