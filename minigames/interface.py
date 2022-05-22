import os
import shutil
import cv2
from csv import writer
import pandas as pd
import numpy as np
import random


class Game():
    def __init__(self) -> None:
        self.tid = "test"
        # self.current_player = None
        self.players = {}  # {player_id: role}

        self.segments = []  # a list of segments (without labels)
        # self.labels = set()
        self.labels = {'a', 'b', 'c', 'd', 'e'}
        self.labelled = {}  # {seg: [label(s)]}
        self.unlabelled = []  # a list of unlabelled segments

        self.accept = []
        self.reject = []

        self.images = set()  # images paths 

    def upload_rawdata(self):
        pass

    def get_images(self):
        # get all the images' paths
        tid = self.tid
        dir = 'tasks/' + tid + '/' + 'dataset/'
        if (not os.path.exists('tasks/' + tid + '/')):
            print("The task id does not exist.")
            return
        for root, _, files in os.walk(dir):
            for file in files:
                if file.endswith('.png') or file.endswith('.jpeg') or file.endswith('.jpg'):
                    self.images.add((root, file))

    def run(self):
        # while True:
        for player in self.players.values():
            player.listen()

    def add_player(self, pid, role):
        if (role == "Host"):
            self.players[pid] = Host(self, pid)
        if (role == "Packer"):
            self.players[pid] = Packer(self, pid)
        if (role == "Labeller"):
            self.players[pid] = Labeller(self, pid)
        if (role == "Guesser"):
            self.players[pid] = Guesser(self, pid)
        if (role == "Reviewer"):
            self.players[pid] = Reviewer(self, pid)

    def create_label(self, label):
        self.labels.add(label)
        # self.labels.append(label)

    def annotate_seg(self, seg, label):
        if not seg in self.labelled:
            self.labelled[seg] = [label]
        else:
            self.labelled[seg].append(label)
    
    def add_unlablled_seg(self, seg):
        self.unlabelled.append(seg)

    def print_players(self):
        for player in self.players:
            print(f"{player.id} is a {type(player)}")
    
    def output_labelled_data(self):
        if self.reject:
            print("Some data need to be relabelled")
        else:
            # output the data
            pass


class Player():
    def __init__(self, game, pid) -> None:
        self.game = game
        self.pid = pid
    
    # def listen():
    #     pass

class Host(Player):
    def __init__(self, game, pid) -> None:
        super().__init__(game, pid)

    def listen(self):
        # get input from the keyboard
        print("Please set a unique task id")
        tid = input()
        self.create_task(tid)

        while True:
            label = input()
            if label == '\q':
                break
            self.create_label(label)

    def create_task(self, tid):
        # unique task id
        # inidividual folder named by the id
        if (os.path.exists('tasks/' + tid + '/')):
            print('Task ID already exists. Please enter a different one.')
            print("Or you can choose to stop creating task (;;q)")
            ans = input()
            if ans == ";;q":
                return
            else:
                self.create_task(ans)

        else:
            os.makedirs('tasks/' + tid + '/')
            print("Please upload the dataset you want to be labelled")
            print("Enter the source path:")
            # path = input()
            path = 'test_dataset'
            print(path)
            self.upload_datasets(tid, path)
        
        self.game.tid = tid

        with open('tasks/' + tid + '/' + tid + '.csv', 'w') as file:
            attr = ['ImageName', 'X1', 'Y1', 'X2', 'Y2', 'Label']
            wri = writer(file)
            wri.writerow(attr)

    def upload_datasets(self, tid, src):
        trg = 'tasks/' + tid + '/' + 'dataset/'
        shutil.copytree(src, trg)

    def create_label(self, label):
        # remove similar labels and fix typo
        label = label.strip()  # remove leading and trailing whitespaces
        label = label.lower()
        self.game.create_label(label)


class Packer(Player):
    def __init__(self, game, pid) -> None:
        super().__init__(game, pid)

        self.rects = []  # coordinates [x1,y1,x2,y2]
        self.current_image = None
    
    def listen(self):
        if not self.game.images:
            return

        for (root, file) in self.game.images:
            file_path = os.path.join(root, file)
            self.current_image = cv2.imread(file_path)

            cv2.namedWindow(file)
            cv2.setMouseCallback(file, self.clickDrag)

            while True:
                cv2.imshow(file, self.current_image)
                key = cv2.waitKey(1) & 0xFF

                # save and unsave
                # TODO: reset bounding boxes
                if key == ord("s"):
                    self.saveCordinates(file_path, self.rects)

                if key == ord("q"):
                    cv2.destroyAllWindows()
                    break

                if key == ord("n"):
                    # cv2.destroyWindow(file_path)
                    self.saveCordinates(file_path, self.rects)
                    cv2.destroyAllWindows()
                    break

    # Listening for the mouse events
    def clickDrag(self, event, x, y, flags, param):
        # draw bounding boxes
        # allows multiple bounding boxes in the same raw image
        # coordinates,top left and bottom right

        if event == cv2.EVENT_LBUTTONDOWN:
            # self.rects = [(x, y)]
            self.rects = [x, y]

        elif event == cv2.EVENT_LBUTTONUP:
            # self.rects.append((x, y))
            self.rects.extend((x, y))
            # cv2.rectangle(self.current_image, self.rects[0], self.rects[1], (255, 0, 255), 1)
            xy1 = (self.rects[0], self.rects[1])
            xy2 = (self.rects[2],self.rects[3])
            cv2.rectangle(self.current_image, xy1, xy2, (255, 0, 255), 1)

    def saveCordinates(self, file, rects):
        #  output as csv file
        dirs = os.path.dirname(file)
        tid = os.path.split(os.path.split(dirs)[0])[1]
        # tid = self.game.tid

        path = 'tasks/' + tid + '/' + tid + '.csv'

        with open(path, 'a') as f_object:
            writer_object = writer(f_object)
            # writer_object.writerow([img, rects[0][0], rects[0][1], rects[1][0], rects[1][0]])  # image name, rects
            info = [file]
            info.extend(rects)
            writer_object.writerow(info)

            f_object.close()
    
    def make_segment(self, raw):
        pass
    # raw data is divided to different segments
    # for seg in segments:
    #     self.data.append(seg)


class Labeller(Player):
    def __init__(self, game, pid) -> None:
        super().__init__(game, pid)
        # self.game = game
        self.selected_label = None
        self.selected_seg = None

    def listen(self):
        tid = self.game.tid
        path = 'tasks/' + tid + '/' + tid + '.csv'
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


class Guesser(Player):
    def __init__(self, game, pid) -> None:
        super().__init__(game, pid)
        self.selected_label = None
        self.current_seg = None

        # self.labelled_data = self.game.labelled
        # self.current_seg = self.labelled_data.keys()[0]
        # self.unmatch = []
    
    def listen(self):
        tid = self.game.tid
        path = 'tasks/' + tid + '/' + tid + '.csv'
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


class Reviewer(Player):
    def __init__(self, game, pid) -> None:
        super().__init__(game, pid)

    def listen(self):
        tid = self.game.tid
        path = 'tasks/' + tid + '/' + tid + '.csv'
        df = pd.read_csv(path)
        label_df = df[df['Label'].notnull()].iloc[1: , :]
        # unlabel_df = df[df['Label'].isnull()]
        if not label_df.equals(df.iloc[1: , :]):
            print("Some segments need to be labelled first")
            return

        for index, row in label_df.iterrows():
            label = row['Label']
            print("The label for this segment is: " + label)
            print("Do you accept(1) or reject(0) the labelling?")

            image_path = row['ImageName']
            image = cv2.imread(image_path)
            cv2.namedWindow(image_path)

            xy1 = (row['X1'],row['Y1'])
            xy2 = (row['X2'],row['Y2'])
            cv2.rectangle(image, xy1, xy2, (255, 0, 255), 1)

            while(True):
                cv2.imshow(image_path, image)

                key = cv2.waitKey(1) & 0xFF

                if key == ord("0"):
                    df['Label'][index] = np.NaN
                    print(label + " is rejected")
                    cv2.destroyAllWindows()
                    break
                if key == ord("1"):
                    print(label + " is accepted")
                    # print("output the csv file")
                    cv2.destroyAllWindows()
                    break

                # if key == ord(";"):
                #     df['Label'][index] = np.NaN
                #     print(image_path + "with" + label + " is deleted")
                #     cv2.destroyAllWindows()
                #     break

        df.to_csv(path, index=False)  # save all the labels back to the csv file
        if df.isnull().values.any():
            print("The task is not done. Some segments need to be relabelled.")
        else:
            print("All the segments are labelled correctly.")
            print("Do you want to download the result (csv file)? (y/n)")
    
    def check(self, state, data):
        if state:
            self.game.accept.append(data)
        else:
            self.game.reject.append(data)
