from tracemalloc import start
import chess
import random

from chess import pgn
import time

# standartMinimax = []
# alphaBetaPruning = []

class BaseBot():
	def __init__(self):
		self.name = "Undefined"
	
	def StartNewGame(self, board, side):
		self.board = board
		self.side = side

	def Move(self):
		self.board.push(random.choice(self.board.legal_moves))

class ExampleBot(BaseBot):
	def __init__(self, deep=3):
		self.name = "Example bot"
		self.deep = deep
		self.center = [chess.D4, chess.D5, chess.E5, chess.E4]

	#WARNING: may crush if no moves left
	def Minimax(self, board, side, root=False, deep=3, analize=False):
		if board.outcome():
			if board.outcome().result() == "1/2-1/2": return 0
			return 10000 if chess.WHITE == board.outcome().winner else -10000

		if not deep:
			b = str(board)
			status = 0
			for p in b:
				if p == 'Q': status += 90
				elif p == 'q': status -= 90
				elif p == 'B': status += 30
				elif p == 'b': status -= 30
				elif p == 'N': status += 30
				elif p == 'n': status -= 30
				elif p == 'R': status += 50
				elif p == 'r': status -= 50
				elif p == 'P': status += 10
				elif p == 'p': status -= 10

			# Check for double pawns
			ranks = str(b).split()

			ranks = list(ranks[i:i+8] for i in range(0, len(ranks), 8))

			for file in range(0, 8):
				blackPawns = 0
				whitePawns = 0
				for rank in range(0, 8):
					target = ranks[rank][file]
					if target == 'P': whitePawns += 1
					elif target == 'p': blackPawns += 1

				if whitePawns:
					status -= (whitePawns - 1) * 3

				if blackPawns:
					status += (blackPawns - 1) * 3

			try:
				b4 = board.copy()
				b4.pop()
				bonus1 = b4.legal_moves.count() / 23 # WARNING: was 10
				bonus2 = board.legal_moves.count() / 23
				if board.turn == chess.WHITE:
					status += bonus2
					status -= bonus1
				else:
					status -= bonus2
					status += bonus1
			except Exception as e:
				print("Error:", e)
				pass
			
			return status #round(status, 2) # Speed down?

		if root:
			moves = {}
			for move in board.legal_moves:
				possibillity = board.copy()
				possibillity.push(move)
				moves[move] = self.Minimax(possibillity, chess.BLACK if side==chess.WHITE else chess.WHITE, deep=deep-1) #[1]

				#WARNING: test code
				try:
					# Punishment for repeating moves
					possibillity.pop()
					m = possibillity.pop()
					if move == m:
						moves[move] += -2 if side == chess.WHITE else 2 # WARNING: changed from -1, 1
					
					# Difference in bounty between defferent castlings?
					if move == chess.Move.from_uci('e1g1') or move == chess.Move.from_uci('e1c1'): moves[move] += 2
					elif move == chess.Move.from_uci('e8g8') or move == chess.Move.from_uci('e8c8'): moves[move] -= 2
				except:
					...
				
			if not analize:
				bestScore = sorted(list(moves.values()), reverse=True)[0] if side == chess.WHITE else sorted(list(moves.values()))[0] #WARNING: was sorted(list(moves.values()))[0] if side == chess.WHITE else sorted(list(moves.values()), reverse=True)[0]
				bestMoves = dict([(i, moves[i]) for i in moves if moves[i] == bestScore])
				return bestMoves
			else:
				return moves
		else:
			bestMove = -10000 if side == chess.WHITE else 10000
			if side == chess.WHITE:
				for move in board.legal_moves:
					possibillity = board.copy()
					possibillity.push(move)
					res = self.Minimax(possibillity, chess.BLACK if side==chess.WHITE else chess.WHITE, deep=deep-1)
					if bestMove < res: bestMove = res
			else:
				for move in board.legal_moves:
					possibillity = board.copy()
					possibillity.push(move)
					res = self.Minimax(possibillity, chess.BLACK if side==chess.WHITE else chess.WHITE, deep=deep-1)
					if bestMove > res: bestMove = res

			return bestMove

	def Move(self):
		startTime = time.time()
		bestMoves = self.Minimax(self.board, self.side, root=True, deep=self.deep)
		t = round(time.time() - startTime, 3)
		# global standartMinimax
		# standartMinimax += [t]
		# print("SM time:", t, "with possible moves:", len(list(self.board.legal_moves)))
		self.board.push(random.choice(list(bestMoves.keys())))

class AlphaBeta(BaseBot):
	def __init__(self, deep=3):
		self.name = "Alpha Beta bot"
		self.deep = deep
		self.center = [chess.D4, chess.D5, chess.E5, chess.E4]

	#WARNING: may crush if no moves left
	def Minimax(self, board, side, root=False, deep=3, alpha=-10000, beta=10000):
		if board.outcome():
			if board.outcome().result() == "1/2-1/2": return 0
			return 10000 if chess.WHITE == board.outcome().winner else -10000 #WARNING: what if outcome different

		if not deep:
			b = str(board)
			status = 0
			for p in b:
				if p == 'Q': status += 90
				elif p == 'q': status -= 90
				elif p == 'B': status += 30
				elif p == 'b': status -= 30
				elif p == 'N': status += 30
				elif p == 'n': status -= 30
				elif p == 'R': status += 50
				elif p == 'r': status -= 50
				elif p == 'P': status += 10
				elif p == 'p': status -= 10

			# Check for double pawns
			ranks = str(b).split()

			ranks = list(ranks[i:i+8] for i in range(0, len(ranks), 8))

			for file in range(0, 8):
				blackPawns = 0
				whitePawns = 0
				for rank in range(0, 8):
					target = ranks[rank][file]
					if target == 'P': whitePawns += 1
					elif target == 'p': blackPawns += 1

				if whitePawns:
					status -= (whitePawns - 1) * 3

				if blackPawns:
					status += (blackPawns - 1) * 3

			try:
				b4 = board.copy()
				b4.pop()
				bonus1 = b4.legal_moves.count() / 23 # WARNING: was 10
				bonus2 = board.legal_moves.count() / 23
				if board.turn == chess.WHITE:
					status += bonus2
					status -= bonus1
				else:
					status -= bonus2
					status += bonus1
			except Exception as e:
				print("Error:", e)
				pass
			
			return status #round(status, 2) # Speed down?

		if root:
			moves = {}
			for move in board.legal_moves:
				possibillity = board.copy()
				possibillity.push(move)
				moves[move] = self.Minimax(possibillity, chess.BLACK if side==chess.WHITE else chess.WHITE, deep=deep-1) #[1]

				#WARNING: test code
				try:
					# Punishment for repeating moves
					possibillity.pop()
					m = possibillity.pop()
					if move == m:
						moves[move] += -2 if side == chess.WHITE else 2 # WARNING: changed from -1, 1
					
					# Difference in bounty between defferent castlings?
					if move == chess.Move.from_uci('e1g1') or move == chess.Move.from_uci('e1c1'): moves[move] += 2
					elif move == chess.Move.from_uci('e8g8') or move == chess.Move.from_uci('e8c8'): moves[move] -= 2
				except:
					...
				
			return moves
		else:
			if side == chess.WHITE:
				maxEval = -10000
				for move in board.legal_moves:
					possibillity = board.copy()
					possibillity.push(move)
					eval = self.Minimax(possibillity, chess.BLACK, False, deep-1, alpha, beta)

					maxEval = max(maxEval, eval)
					alpha = max(alpha, eval)
					if beta <= alpha: break
				return maxEval
			else:
				minEval = 10000
				for move in board.legal_moves:
					possibillity = board.copy()
					possibillity.push(move)
					eval = self.Minimax(possibillity, chess.WHITE, False, deep-1, alpha, beta)

					minEval = min(minEval, eval)
					beta = min(beta, eval)
					if beta <= alpha: break
				return minEval

	def Move(self):
		startTime = time.time()
		moves = self.Minimax(self.board, self.side, root=True, deep=self.deep)
		t = round(time.time() - startTime, 3)
		# global alphaBetaPruning
		# alphaBetaPruning += [t]
		print("AB time:", t, "with possible moves:", len(list(self.board.legal_moves)))
		moves = {k: v for k, v in sorted(moves.items(), key=lambda item: item[1])} if self.side == chess.BLACK else \
					{k: v for k, v in sorted(moves.items(), key=lambda item: item[1], reverse=True)}
		# print("AB Moves:", '; '.join([str(x) for x in list(bestMoves.keys())])) # print("Best moves detected:", len(bestMoves.items()), bestMoves) # print(list(bestMoves.values()))
		# self.board.push(random.choice(list(bestMoves.keys())))
		best = list(moves.values())[0]
		
		bestMoves = []
		for move in list(moves.keys()):
			if moves[move] == best:
				bestMoves += [move]
			else:
				break
		
		if len(bestMoves):
			# print("Moves:", bestMoves)
			self.board.push(random.choice(bestMoves))
		else:
			raise BaseException("No possible moves found") # WARNING: Wrong exception

if __name__ == "__main__":
	AGAINSTBOT = False
	# BOTSIDE = chess.BLACK

	if AGAINSTBOT:
		board = chess.Board()
		bot = ExampleBot(3)
		bot.StartNewGame(board, chess.BLACK)
		game = chess.pgn.Game()
		game.setup(board)
		node = game

		try:
			while not board.outcome():
				# bot.Move()
				# node = node.add_variation(board.peek())
				# print("Bot move:", board.peek())
				while True:
					try:
						board.push_san(input('> '))
						break
					except:
						...
				node = node.add_variation(board.peek())

				bot.Move()
				node = node.add_variation(board.peek())
				print("Bot move:", board.peek())

				# print(board)
		except Exception as e:
			print("Error:", e)

		# print(game)
		exit(0)

	white = ExampleBot() #board, chess.WHITE)
	black = AlphaBeta(4) #AlphaBetaBot() #ExampleBot(3) #board, chess.BLACK)

	# white.StartNewGame(board, chess.WHITE)
	# black.StartNewGame(board, chess.BLACK)

	from engine import StartClassicGame

	headers = {"Event": "Test game", "Site": "chessbots", "Date": "Day Dev", "Round": "undefined round"}
	game = StartClassicGame((white, black), headers)
	print(game[0])
	print("Error:", game[2])
	# print(standartMinimax, alphaBetaPruning)

	# game = chess.pgn.Game()
	# game.setup(board)
	# node = game

	# import os

	# try:
	# 	while not board.outcome():
	# 		white.Move()
	# 		node = node.add_variation(board.peek())
	# 		black.Move()
	# 		node = node.add_variation(board.peek())

	# 		os.system("cls")
	# 		print(board)
	# except Exception as e:
	# 	print(e)

	# print(game)