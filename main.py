"""
Main file to execute the game.

Author: Cindy
"""

from minigames.interface import *


if __name__ == '__main__':
    game = Game()
    print("Do you want to create a new task? (y/n)")
    ans = input()
    if ans.lower() == "y" or ans.lower() == "yes":
        # game.create_csv()
        game.add_player(0, "Host")
    else:
        print("Please enter the task id you want to join.")

        print("Please enter your role:")
        print("1: Packer    2: Labeller    3: Guesser    4: Reviewer (Host)")
        role = input()
        if role.lower() == "1" or role == "Packer":
            game.add_player(0, "Packer")
            game.get_images("dataset")
        elif role.lower() == "2" or role == "Labeller":
            game.add_player(0, "Labeller")
        elif role.lower() == "3" or role == "Guesser":
            game.add_player(0, "Guesser")
        elif role.lower() == "4" or role == "Reviewer":
            game.add_player(0, "Reviewer")

    game.run()
