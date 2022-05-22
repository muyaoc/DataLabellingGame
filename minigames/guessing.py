from interface import *


class Guesser(Player):
    def __init__(self, game, pid) -> None:
        super().__init__(game, pid)
        self.selected_label = None
        self.current_seg = None

        # self.labelled_data = self.game.labelled
        # self.current_seg = self.labelled_data.keys()[0]
        # self.unmatch = []
    
    def listen(self):
        path = 'tasks/test.csv'
        labels_list = list(self.game.labels)
        df = pd.read_csv(path)
        label_df = df[df['Label'].notnull()].iloc[1: , :]
        if label_df.empty:
            return

        for index, row in label_df.iterrows():
            print("Guess the label from the following options:")

            # random algorithm
            labels = [row['Label']]
            label_copy = labels_list.copy()
            label_copy.remove(row['Label'])
            labels += random.sample(label_copy, 2)
            random.shuffle(labels)

            for i in range(len(labels)):
                print(str(i) + ": " + labels[i])

            image_path = row['ImageName']
            image = cv2.imread(image_path)
            cv2.namedWindow(image_path)

            xy1 = (row['X1'],row['Y1'])
            xy2 = (row['X2'],row['Y2'])
            cv2.rectangle(image, xy1, xy2, (255, 0, 255), 1)

            while(True):
                cv2.imshow(image_path, image)

                key = cv2.waitKey(1) & 0xFF

                # TODO: exit and save
                if key >= 48 and key <= 57:  # key'0'-key'9'
                    number = key - 48
                    if (number <= len(labels) - 1):
                        if labels[number] == row['Label']:
                            print("Label is guessed correctly")
                        else:
                            print("Label is guessed incorrectly")
                            # TODO: add the incorrect index to []

                        cv2.destroyAllWindows()
                        break

    def select_label(self, label):
        self.selected_label = label
    
    # def enter_diff_label(self, label):
    #     self.selected_label = label

    def guess(self):
        seg = self.current_seg
        label = self.selected_label
        if label != self.game.labelled[seg]:
            self.game.annotate_seg(seg, label)

        # if label != self.game.labelled[seg]:
        #    self.unmatch.append(seg)
        #    self.game.labelled.remove(seg)
    
    def update_seg(self, seg):
        self.current_seg = seg
