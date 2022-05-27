"""
The first version of the Labelling Game framework.
It can be utilised when the server is set up.
"""

from interface import *


class Labeller(Player):
    def __init__(self, game, pid) -> None:
        super().__init__(game, pid)
        self.selected_label = None
        self.selected_seg = None

    def listen(self):
        pass    

    def select_label(self, label):
        self.selected_label = label
    
    def select_seg(self, seg):
        self.selected_seg = seg
    
    def annotate_seg(self):
        if not self.selected_label:
            print("No valid label is selected")
        elif not self.selected_seg:
            print("No segment is selected")
        else:
            self.game.annotate_seg(self.selected_seg, self.selected_label)
            self.selected_label = None
    
    def skip_label(self):
        if not self.selected_seg:
            print("No segment is selected")
        else:
            self.game.add_unlablled_seg(self.selected_seg)
