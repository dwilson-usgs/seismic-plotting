#!/usr/bin/env python

from obspy.clients.fdsn import Client
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as ml
from obspy.core import UTCDateTime
from scipy.interpolate import griddata
from obspy.geodetics import gps2dist_azimuth
import matplotlib

from matplotlib import cm
import pickle
import cartopy.crs as ccrs
import cartopy
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib.ticker as mticker
client = Client("IRIS")


# time for station noise analysis
starttime = UTCDateTime("2019-08-01 00:00:00")
endtime = UTCDateTime("2019-08-01 00:10:00")
boxcoords=[38.0, -81.0, 48.0, -66]
nsta=5


stas= "*"
nets="IU,US,N4,NE"
chans="HHZ,BHZ"


slats =[]
slons =[]


inventory = client.get_stations(network=nets,station=stas,channel=chans,starttime=starttime, endtime=endtime, minlatitude=boxcoords[0],
                                minlongitude=boxcoords[1], maxlatitude=boxcoords[2], maxlongitude=boxcoords[3])

for cnet in inventory:
    for stat in cnet:
        slats.append(stat.latitude)
        slons.append(stat.longitude)

            
slats = np.asarray(slats)
slons = np.asarray(slons)
x=np.arange(boxcoords[1],boxcoords[3],.25)
y=np.arange(boxcoords[0],boxcoords[2],.25)
results=[]
for xi in x:
    for yi in y:
        stat_results=[]
        dists=[]
        for n in range(len(slats)):
            epi_dist, az, baz = gps2dist_azimuth(yi,xi,slats[n],slons[n])
            dists.append(epi_dist / 1000)
        if np.min(dists) < 250:
            dists=np.sort(dists)
            stat_results=np.sort(stat_results)
            results.append([xi, yi, dists[nsta-1]])


results=np.asarray(results)


x=np.asarray(results[:,0])
y=np.asarray(results[:,1])
zd=np.asarray(results[:,2])




nbins=300
xi, yi = np.mgrid[x.min():x.max():nbins*1j, y.min():y.max():nbins*1j]

zdi = griddata( (x,y), zd, (xi, yi), method='cubic')
matplotlib.rcParams['xtick.direction'] = 'out'
matplotlib.rcParams['ytick.direction'] = 'out'

# this is the cartopy section
extent=[boxcoords[1], boxcoords[3], boxcoords[0], boxcoords[2]]
central_lon = np.mean(extent[:2])
central_lat = np.mean(extent[2:])
plt.figure(2, figsize=(10,10))
#ax3 = plt.axes(projection=ccrs.AlbersEqualArea(central_lon, central_lat))
ax3 = plt.axes(projection=ccrs.Mercator(central_longitude=central_lon))
ax3.set_extent(extent)

ax3.add_feature(cartopy.feature.OCEAN)
ax3.add_feature(cartopy.feature.LAND, edgecolor='black')
ax3.add_feature(cartopy.feature.LAKES, edgecolor='black')
ax3.add_feature(cartopy.feature.STATES, edgecolor='black')
plt.contourf(xi, yi, zdi.reshape(xi.shape), cmap=plt.cm.plasma, transform=ccrs.PlateCarree() )

gridlines=ax3.gridlines(draw_labels=True, color='gray', alpha=.5, linestyle=':')
gridlines.xlabels_top=False
gridlines.ylabels_right=False
gridlines.xlocator = mticker.FixedLocator(np.arange(-80,-64,2))
gridlines.ylocator = mticker.FixedLocator(np.arange(38,50,2))


# Add color bar
plt.clim(0.0,300)
cbar=plt.colorbar()
cbar.set_label('Distance to 5th nearest station')

plt.xlabel('Longitude')
plt.ylabel('Latitude')

plt.plot(slons,slats, 'kd', markersize=4.5, transform=ccrs.PlateCarree())
plt.show()

