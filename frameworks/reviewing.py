"""
The first version of the Reviewing Game framework.
It can be utilised when the server is set up.
"""

from interface import *


class Reviewer(Player):
    def __init__(self, game, pid) -> None:
        super().__init__(game, pid)

    def listen(self):
        pass
    
    def check(self, state, data):
        if state:
            self.game.accept.append(data)
        else:
            self.game.reject.append(data)
