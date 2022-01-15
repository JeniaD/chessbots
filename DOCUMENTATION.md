# Documentation v. 0.1.0
## `chessbots.bot`
This file contains `BaseBot` and `ExampleBot` classes.
`BaseBot` class is used to write your own bot on top of it, so you will be able to work with it using this package. To use it, simply write:
```Python
import chessbots.bot
```
you can also add "`as ...`" at the end if you want to.

So, the `BaseBot` class looks like this:
```Python
class BaseBot():
	def __init__(self):
		self.name = "Undefined"
	
	def StartNewGame(self, board, side):
		self.board = board
		self.side = side

	def Move(self):
		self.board.push(random.choice(self.board.legal_moves))
```
This is how it looks in the __0.1.0__ version.

It is all the functions bot should have. 

> Note: In the future, maybe `self.name` will be changed to `self.__name`.

So lets explore every function.
#### `StartNewGame(self, board, side)`
This function is supposed to initialize bot for the new game.

#### `Move(self)`
This function is called to make a move, for now, it doesn't take any paramenters. 
> Note: In the future versions this should be fixed, because this causes security problem with fair play.

So what this function should do is `self.board.push`.
So this function should be overwrited by user.

#### So here is the example:
```Python
class ExampleBot(BaseBot):
	def __init__(self, board, side, deep=3):
		self.name = "Example bot"
		self.deep = deep

        # You can add here different strategies and tactics

	def Minimax(self, board, side, root=False, deep=3):
		... # A lot of code here
        return bestMove

	def Move(self):
		self.board.push(self.Minimax(self.board, \
                        self.side, root=True, deep=self.deep))
```
So here is the idea: bot can be created as you like, but it should have `name` variable, `StartNewGame` and `Move` functions

After that, you can launch a game versus other bots! You're free to use my bot, which is `chessbots.bot.ExampleBot`.