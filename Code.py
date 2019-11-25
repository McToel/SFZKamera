import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

a = 0
while(True):
    Path = input("Enter path to file: ")

    Messung = pd.read_csv(Path, sep=';', index_col='Zeit')
    Messung.index =  Messung.index / 3600 / 24

    cap_dirt = Messung[['Cap_Dirt']]
    cap_leaf = Messung[['Cap_Leaf']]
    cap_air = Messung[['Cap_Air']]
    Messung['Cap_Dirt_Rol'] = Messung['Cap_Dirt'].rolling(min_periods = 10, window = 60, center = False).mean()
    Messung['Cap_Leaf_Rol'] = Messung['Cap_Leaf'].rolling(min_periods = 10, window = 60, center = False).mean()
    Messung.to_csv(str(a) + '.csv')
    a += 1
print(Messung)

#temp = Messung[['temperatur']]
#temp -= cap
both = cap_dirt.join((cap_leaf), how='inner')
plotting = both.plot(linewidth=1)
plt.show(plotting)
Rol = both.rolling(min_periods = 10, window = 60, center = False).mean().plot(linewidth=1)
plt.show(Rol)
