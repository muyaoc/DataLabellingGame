"""
Main file to execute the game.

Author: Cindy
"""
# import pandas as pd
from csv import writer


def saveCordinates(list_data):
    #  output as csv file
    with open('test.csv', 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(list_data)

        f_object.close()


if __name__ == '__main__':
    f = open('test.csv', 'w')
    attr = ['ImageName','X1','Y1','X2','Y2','Label']
    wri = writer(f)
    wri.writerow(attr)
    f.close()
    # df = pd.DataFrame(columns=attr)
    # df.set_index('ImageName')
    # df.to_csv('test.csv')

    saveCordinates(['test', 0, 1, 1, 0])
    saveCordinates(['test2', 0, 2, 2, 0])
