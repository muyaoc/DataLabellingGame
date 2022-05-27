"""
The first version of the Guessing Game framework.
It can be utilised when the server is set up.
"""

from interface import *


class Guesser(Player):
    def __init__(self, game, pid) -> None:
        super().__init__(game, pid)
        self.selected_label = None
        self.current_seg = None

        self.labelled_data = self.game.labelled
        self.current_seg = self.labelled_data.keys()[0]
        self.unmatch = []
    
    def listen(self):
        pass

    def select_label(self, label):
        self.selected_label = label
    
    def enter_diff_label(self, label):
        self.selected_label = label

    def guess(self):
        seg = self.current_seg
        label = self.selected_label
        if label != self.game.labelled[seg]:
            self.game.annotate_seg(seg, label)

        if label != self.game.labelled[seg]:
           self.unmatch.append(seg)
           self.game.labelled.remove(seg)
    
    def update_seg(self, seg):
        self.current_seg = seg
