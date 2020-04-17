#!/usr/bin/env python

from obspy.clients.fdsn import Client

import matplotlib.pyplot as plt
#import matplotlib as mpl
import numpy as np
from obspy.core import UTCDateTime


######## end of definitions

client = Client("IRIS")


stime = UTCDateTime("2020-04-16T08:05:00.0")
etime = UTCDateTime("2020-04-16T08:35:00.0")
net = "IU,NE"
stat = "HRV,WES"
loc = "00"
chan = "LH*"

def get_loc_list(sta):
    chanlist=[]
    for chan in sta:
        if chan.location_code not in chanlist:
            chanlist.append(chan.location_code)
    return chanlist
        
inventory = client.get_stations(starttime=stime, endtime=etime, 
   network=net, sta=stat, loc=loc, channel=chan, level="response")

fig=plt.figure(1,figsize=(12,12))
for nt in inventory:
    for sta in nt:
        locs=get_loc_list(sta)
        for lc in locs:
            inv2=inventory.select(station=sta.code) 
            st = client.get_waveforms(nt.code, sta.code, lc, chan, stime, etime, attach_response=True)
            st.rotate(method='->ZNE',inventory=inv2)
            st.detrend(type='linear')
            st.remove_response(output="DISP")
            st.filter(type='bandpass',freqmin=1/60,freqmax=10)
            for n in range(3):
                plt.subplot(3,1,n+1)
                plt.plot(st[n].data,label=sta.code+"-"+st[n].stats.location+"-"+st[n].stats.channel)
            

for n in range(3):
    plt.subplot(3,1,n+1)
    plt.legend()
plt.suptitle('%s-%s-%s-%s %s-%s' % (net, stat, loc, chan, stime, etime))

plt.show()
