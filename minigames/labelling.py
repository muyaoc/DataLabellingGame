from interface import *


class Labeller(Player):
    def __init__(self, game, pid) -> None:
        super().__init__(game, pid)
        # self.game = game
        self.selected_label = None
        self.selected_seg = None

    def listen(self):
        path = 'tasks/test.csv'
        labels_list = list(self.game.labels)
        df = pd.read_csv(path)
        unlabel_df = df[df['Label'].isnull()]
        if unlabel_df.empty:
            return

        for index, row in unlabel_df.iterrows():
            print("Labels:")
            for i in range(len(labels_list)):
                print(str(i) + ": " + labels_list[i])

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
                    if (number <= len(labels_list) - 1):
                        print(image_path + " was labelled as " + labels_list[number])

                        df['Label'][index] = labels_list[number]
                        cv2.destroyAllWindows()
                        break

        df.to_csv(path, index=False)  # save all the labels back to the csv file        

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
