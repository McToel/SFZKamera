import cv2 as cv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from progress.bar import Bar
import glob

from datenauswerter import chart_for_timelapse

def put_chart_in_image(chart, img):
    chimage = img
    y = chart.shape[0]
    x = chart.shape[1]
    #orange bar
    chimage[-(y+40):,-x:,:][np.where((chart<=[20,128,255]).all(axis=2))] = chart[np.where((chart<=[20,128,255]).all(axis=2))]

    #blue bar
    chimage[-(y+40):,-x:,:][np.where((chart<=[180,120,32]).all(axis=2))] = chart[np.where((chart<=[180,120,32]).all(axis=2))]

    #black
    chimage[-(y+40):,-x:,:][np.where((chart<=[80,80,80]).all(axis=2))] = chart[np.where((chart<=[80,80,80]).all(axis=2))]
    cv.imshow('Test', chimage)
    return chimage
    # if cv.waitKey() == ord('q'):
    #     cv.destroyAllWindows()

images = glob.glob('images/*.jpg')
path = input("Enter path to csv data file: ") + '.csv'
messung = pd.read_csv('path', sep=';', index_col='Zeit')

for img_name in images:
    img = cv.imread(img_name)
    img_name = img_name.replace({'.jpg':'','img':'', 'images\\\\':''})
    img_seconds = int(img_name)

    chart_for_timelapse(messung,
                        cols=['Cap_Dirt', 'Cap_Leaf'],
                        max_i=img_seconds, 
                        x_lim=[0, messund.index[-1]], 
                        y_lim=[0, 300], 
                        x_title='Zeit', 
                        y_title='Analogwert')
    chart = cv.imread("chart.png")
    chimage = put_chart_in_image(chart, img)
    cv.imwrite('chimg' + img_name + '.jpg', chimage) 

img = cv.imread("img00000.jpg")
chart = cv.imread("lol.png")
put_chart_in_image(chart, img)
#'img%s.jpg'%('{0:016d}'.format(time.time() - start_time))