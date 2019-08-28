import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from obspy.core import UTCDateTime
from obspy.clients.fdsn import Client
client = Client("IRIS")


def main():
    slats =[]
    slons =[]
    starttime = UTCDateTime("2019-08-01 00:00:00")
    endtime = UTCDateTime("2019-08-01 00:10:00")

    inventory = client.get_stations(network="IU,IC,CU",station="*",channel="LHZ",
                                    starttime=starttime,endtime=endtime)

    for cnet in inventory:
        for stat in cnet:
            slats.append(stat.latitude)
            slons.append(stat.longitude)

    for n in range(5):
        plt.figure(figsize=(9, 6))
        ax = plt.axes(projection=ccrs.Robinson())
        ax.coastlines(resolution='110m')
        ax.gridlines()
        if n==0:
            plt.title('First build the map axes with gridlines')
            plt.show()
        elif n==1:
            # now I want to plot my stations
            ax.plot(slons,slats, 'kd', linestyle='None',markersize=4.5)
            plt.title('Hey, what happened to my map?')
            plt.show()
        elif n==2:
            # now I want to plot my stations (try 2)
            ax.plot(slons,slats, 'kd', linestyle='None',markersize=4.5, transform=ccrs.Geodetic())
            plt.title('Now what is going on?')
            plt.show()
        elif n==3:
            # now I want to plot my stations (try 3)
            ax.scatter(slons,slats, transform=ccrs.Geodetic(),marker='d' , edgecolor='black',facecolor=[.5,.9,.5])
            plt.title("scatter works better for transforms")
            plt.show()
        elif n==4:
            # now make it pretty
            ax.scatter(slons,slats, transform=ccrs.Geodetic(),marker='d' , edgecolor='black',facecolor=[.5,.9,.5])
            plt.title("The IRIS/USGS GSN")
            ax.stock_img()
            plt.show()

if __name__ == '__main__':
    main()

