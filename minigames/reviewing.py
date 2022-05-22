from interface import *


class Reviewer(Player):
    def __init__(self, game, pid) -> None:
        super().__init__(game, pid)

    def listen(self):
        path = 'tasks/test.csv'
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
