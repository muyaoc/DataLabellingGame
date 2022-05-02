"""
Main file to execute the game.

Author: Cindy
"""

from minigames.interface import *


if __name__ == '__main__':
    game = Game()
    # game.create_csv()
    # game.add_player(0, "Host")
    # game.add_player(0, "Producer")
    # game.get_images("dataset")
    game.add_player(0, "Guesser")
    game.run()
