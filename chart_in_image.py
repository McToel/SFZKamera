#import cv2 as cv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from progress.bar import Bar
import glob
import io
from PIL import Image

from datenauswerter import chart_for_timelapse

def put_chart_in_image(chart, img):
    img.paste(chart, (0, 0), chart)
    #img.show()
    return img
    # chimage = img
    # y = chart.shape[0]
    # x = chart.shape[1]
    # #orange bar
    # chimage[-(y+40):,-x:,:][np.where((chart<=[20,128,255]).all(axis=2))] = chart[np.where((chart<=[20,128,255]).all(axis=2))]

    # #blue bar
    # chimage[-(y+40):,-x:,:][np.where((chart<=[180,120,32]).all(axis=2))] = chart[np.where((chart<=[180,120,32]).all(axis=2))]

    # #black
    # chimage[-(y+40):,-x:,:][np.where((chart<=[80,80,80]).all(axis=2))] = chart[np.where((chart<=[80,80,80]).all(axis=2))]
    # # cv.imshow('Test', chimage)
    # return chimage
    # # if cv.waitKey() == ord('q'):
    # #     cv.destroyAllWindows()

import cProfile, pstats, io

def profile(fnc):
    
    """A decorator that uses cProfile to profile a function"""
    
    def inner(*args, **kwargs):
        
        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval

    return inner


@profile
def make():
    images = glob.glob('images/*.jpg')
    path = 'messungen/' + input("Enter path to csv data file: ") + '.csv'
    messung = pd.read_csv(path, sep=',', index_col='time')
    bar = Bar('processing images', max=len(images))

    for i, img_name in enumerate(images):
        img = Image.open(img_name) #cv.imread(img_name)
        #img.putalpha(255)
        img_name = img_name.replace('.jpg','')
        img_name = img_name.replace('img','')
        img_name = img_name.replace('images\\','')
        img_seconds = int(img_name)
        img_name = '%s.jpg'%('{0:06d}'.format(i))

        chart = chart_for_timelapse(messung, cols=['cap_dirt', 'cap_leaf'],
                            max_i=img_seconds, x_lim=[0, messung.index[-1]], 
                            y_lim=[1000, 3000], x_title='Zeit in Sekunden', 
                            y_title='Analogwert')
        #chart = cv.imread("chart.png")
        chimage = put_chart_in_image(chart, img)
        chimage.save('chimages/' + img_name)
        #cv.imwrite('chimages/' + img_name, chimage) 
        bar.next()
        if (i == 100):
            break

    bar.finish()
    # img = cv.imread("img00000.jpg")
    # chart = cv.imread("lol.png")
    # put_chart_in_image(chart, img)
    #'img%s.jpg'%('{0:016d}'.format(time.time() - start_time))

if __name__ == '__main__':
    make()