import chess
import random
from chess import pgn

class BaseBot():
	def __init__(self, name, board, side):
		self.name = name
		self.board = board
		self.side = side

	def Move(self):
		self.board.push(random.choice(self.board.legal_moves))

class ExampleBot(BaseBot):
	def __init__(self, board, side, deep=3):
		super().__init__("Example bot", board, side)

		self.deep = deep

	#WARNING: may crush if no moves left
	def Minimax(self, board, side, root=False, deep=3):
		if board.outcome():
			if board.outcome().result() == "1/2-1/2": return 0
			return 10000 if chess.WHITE == board.outcome().winner else -10000

		if not deep:
			b = str(board)
			# Save calculations from the previous iterations via function parameter? X
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

			# Better to break the len()
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
					# print("Minus", (whitePawns - 1) * 3)

				if blackPawns:
					status += (blackPawns - 1) * 3
					# print("Plus", (blackPawns - 1) * 3)

			# Mobillity
			try:
				b4 = board.copy().pop()
				bonus1 = b4.legal_moves.count() / 10
				bonus2 = board.legal_moves.count() / 10
				if board.turn == chess.WHITE:
					status += bonus2
					status -= bonus1
				else:
					status -= bonus2
					status += bonus1
			except:
				pass

			return status

		if root:
			moves = {}
			for move in board.legal_moves:
				possibillity = board.copy()
				possibillity.push(move)
				moves[move] = self.Minimax(possibillity, chess.BLACK if side==chess.WHITE else chess.WHITE, deep=deep-1) #[1]

			bestScore = sorted(list(moves.values()), reverse=True)[0] if side == chess.WHITE else sorted(list(moves.values()))[0] #WARNING: was sorted(list(moves.values()))[0] if side == chess.WHITE else sorted(list(moves.values()), reverse=True)[0]
			bestMoves = dict([(i, moves[i]) for i in moves if moves[i] == bestScore])
			return bestMoves
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
		bestMoves = self.Minimax(self.board, self.side, root=True, deep=self.deep)
		self.board.push(random.choice(list(bestMoves.keys())))

if __name__ == "__main__":
	board = chess.Board()
	white = ExampleBot(board, chess.WHITE)
	black = ExampleBot(board, chess.BLACK)

	game = chess.pgn.Game()
	game.setup(board)
	node = game

	import os

	try:
		while not board.outcome():
			white.Move()
			node = node.add_variation(board.peek())
			black.Move()
			node = node.add_variation(board.peek())

			os.system("cls")
			print(board)
	except Exception as e:
		print(e)

	print(game)