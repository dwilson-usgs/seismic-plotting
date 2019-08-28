"""
Global Map
----------

An example of a simple map that compares Geodetic and Plate Carree lines
between two locations.

"""


import matplotlib.pyplot as plt

import cartopy.crs as ccrs
import cartopy.feature as cf

def main():
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())
    #ax = fig.add_subplot(1, 1, 1, projection=ccrs.Mercator())
    ax.set_global()

    ax.coastlines()
    #gridlines=ax.gridlines()
    #gridlines=ax.gridlines(draw_labels=True)
    ax.plot(-106.46, 34.95, 'o', transform=ccrs.PlateCarree())
    ax.plot([-106.46, 16.4], [34.95, 48.1], transform=ccrs.PlateCarree())
    ax.plot([-106.46, 16.4], [34.95, 48.1], transform=ccrs.Geodetic())
    #ax.add_feature(cf.OCEAN)
    plt.show()


if __name__ == '__main__':
    main()
