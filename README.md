# Chessbots
It is simple chess API for bots, which is based on 
[chess](https://github.com/niklasf/python-chess) 
library. It provides small functionality, although it is enough
to build your own bot from scratch.

Here is an example:
```python
>>> import chessbots
>>> import chessbots.bot
>>> import chessbots.engine
>>> chessbots.bot.BaseBot() # The class which contans basic functions for your bot
>>> chessbots.bot.ExampleBot() # Built-in bot based on minimax algorithm
>>> chessbots.engine.LaunchGame(bot1, bot2) # Function which allows bots to play games against each other
```