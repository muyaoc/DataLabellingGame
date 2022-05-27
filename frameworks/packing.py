"""
The first version of the Packing Game framework.
It can be utilised when the server is set up.
"""

from interface import *


class Packer(Player):
    def __init__(self, game, pid) -> None:
        super().__init__(game, pid)

        self.rects = []  # coordinates [x1,y1,x2,y2]
        self.current_image = None
    
    def listen(self):
        if not self.game.images:
            return

        root, file = self.game.images.pop()
        file_path = os.path.join(root, file)

        self.current_image = cv2.imread(file_path)

        cv2.namedWindow(file)
        cv2.setMouseCallback(file, self.clickDrag)

        while True:
            cv2.imshow(file, self.current_image)
            key = cv2.waitKey(1) & 0xFF

            # TODO: exit and save
            if key == ord("s"):
                self.saveCordinates(file_path, self.rects)

            if key == ord("q"):
                cv2.destroyAllWindows()
                break

    # Listening for the mouse events
    def clickDrag(self, event, x, y, flags, param):
        # draw bounding boxes
        # allows multiple bounding boxes in the same raw image
        # coordinates,top left and bottom right

        if event == cv2.EVENT_LBUTTONDOWN:
            self.rects = [x, y]

        elif event == cv2.EVENT_LBUTTONUP:
            self.rects.extend((x, y))
            xy1 = (self.rects[0], self.rects[1])
            xy2 = (self.rects[2],self.rects[3])
            cv2.rectangle(self.current_image, xy1, xy2, (255, 0, 255), 1)

    def saveCordinates(self, file, rects):
        pass

    def make_segment(self, raw):
        pass
    # raw data is divided to different segments
    # for seg in segments:
    #     self.data.append(seg)
