import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
from PIL import Image


def chart_for_timelapse(df, max_i, x_lim, y_lim, x_title, y_title, cols):
    fontdict_x = {'fontsize': 17,
                'fontweight' : 'normal',
                'verticalalignment': 'top',
                'horizontalalignment': 'center'}

    fontdict_y = {'fontsize': 17,
                'fontweight' : 'normal',
                'verticalalignment': 'baseline',
                'horizontalalignment': 'center'}
    
    fig, plot = plt.subplots()

    plot.set_xlim(x_lim[0], x_lim[1])
    plot.set_ylim(y_lim[0], y_lim[1])

    plot.plot(df.loc[:max_i, cols], linewidth=3)
    plot.set_xlabel(x_title, fontdict = fontdict_x)
    plot.set_ylabel(y_title, fontdict = fontdict_y)
    #plt.savefig('chart.png')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=True)
    buf.seek(0)
    img = Image.open(buf)
    plot.clear()
    plt.close(fig)
    

    return img

# Messung = pd.read_csv('m2.csv', sep=';', index_col='Zeit')
# chart_for_timelapse(Messung,
#                     cols=['Cap_Dirt', 'Cap_Leaf'],
#                     max_i=10000, 
#                     x_lim=[0, 10000], 
#                     y_lim=[0, 400], 
#                     x_title='Zeit', 
#                     y_title='Analogwert')



# Path = input("Enter path to file: ")

# Messung = pd.read_csv(Path, sep=';', index_col='Zeit')
# Messung.index =  Messung.index / 3600 / 24

# cap_dirt = Messung[['Cap_Dirt']]
# cap_leaf = Messung[['Cap_Leaf']]

# both = cap_dirt.join((cap_leaf), how='inner')
# plotting = both.plot(linewidth=1)
# plt.show(plotting)
# Rol = both.rolling(min_periods = 10, window = 60, center = False).mean().plot(linewidth=1)
# plt.show(Rol)
