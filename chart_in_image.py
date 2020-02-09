import pandas as pd
import numpy as np
import os
from progress.bar import Bar
import glob
import io
from PIL import Image

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib


#from datenauswerter import chart_for_timelapse
class Plotter:
    def __init__(self, df, x_lim, y_lim, x_title, y_title, cols):
        self.df = df
        self.x_lim = x_lim
        self.y_lim = y_lim
        self.x_title = x_title
        self.y_title = y_title
        self.cols = cols
        self.buf = io.BytesIO()
        self.fontdict_x = {'fontsize': 17,
                'fontweight' : 'normal',
                'verticalalignment': 'top',
                'horizontalalignment': 'center'}
        self.fontdict_y = {'fontsize': 17,
                'fontweight' : 'normal',
                'verticalalignment': 'baseline',
                'horizontalalignment': 'center'}
        self.fig_plot()

    def fig_plot(self):
        pass

    def chart_for_timelapse(self, max_i):
        fig, plot = plt.subplots()

        plot.set_xlim(self.x_lim[0], self.x_lim[1])
        plot.set_ylim(self.y_lim[0], self.y_lim[1])

        plot.plot(self.df.loc[:max_i, self.cols], linewidth=3)
        plot.set_xlabel(self.x_title, fontdict = self.fontdict_x)
        plot.set_ylabel(self.y_title, fontdict = self.fontdict_y)
        #plt.savefig('chart.png')
        buf = io.BytesIO()
        plt.savefig(buf, format='png', transparent=True)
        buf.seek(0)
        img = Image.open(buf)
        plot.clear()
        plt.close(fig)
        

        return img

def put_chart_in_image(chart, img):
    img.paste(chart, (0, 0), chart)
    return img


def make():
    images = glob.glob('images/*.jpg')
    path = 'messungen/' + input("Enter path to csv data file: ") + '.csv'
    messung = pd.read_csv(path, sep=',', index_col='time')
    bar = Bar('processing images', max=len(images))
    plotter = Plotter(messung, cols=['cap_dirt', 'cap_leaf'], x_lim=[0, messung.index[-1]], 
                            y_lim=[1000, 3000], x_title='Zeit in Sekunden', y_title='Analogwert')


    for i, img_name in enumerate(images):
        img = Image.open(img_name) #cv.imread(img_name)
        img_name = img_name.replace('.jpg','')
        img_name = img_name.replace('img','')
        img_name = img_name.replace('images\\','')
        img_seconds = int(img_name)
        img_name = '%s.jpg'%('{0:06d}'.format(i))

        chart = plotter.chart_for_timelapse(max_i=img_seconds)

        chimage = put_chart_in_image(chart, img)
        chimage.save('chimages/' + img_name)
        if (i % 10 == 0):
            bar.next(10)
            print(' eta: ', bar.eta_td, end='\r')
        # if (i == 100):
        #    break

    bar.finish()

if __name__ == '__main__':
    make()