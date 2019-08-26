"""
Global Map
----------

An example of a simple map that compares Geodetic and Plate Carree lines
between two locations.

"""


import matplotlib.pyplot as plt

import cartopy.crs as ccrs


def main():
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())
    #ax = fig.add_subplot(1, 1, 1, projection=ccrs.Mercator())
    # make the map global rather than have it zoom in to
    # the extents of any plotted data
    ax.set_global()

    ax.stock_img()
    ax.coastlines()
    #gridlines=ax.gridlines(draw_labels=True)
    ax.plot(-106.46, 34.95, 'o', transform=ccrs.PlateCarree())
    ax.plot([-106.46, 16.4], [34.95, 48.1], transform=ccrs.PlateCarree())
    ax.plot([-106.46, 16.4], [34.95, 48.1], transform=ccrs.Geodetic())

    plt.show()


if __name__ == '__main__':
    main()
