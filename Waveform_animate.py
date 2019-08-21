from obspy.core import read, UTCDateTime, Stream
from obspy.clients.fdsn.client import Client
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from scipy.signal import hilbert
import matplotlib.animation as animation
Writer = animation.writers['pillow']
writer = Writer(fps=20, metadata=dict(artist='Me'), bitrate=1800)
       
sta='R32B'
loc='00'
net = 'N4'
chan='HHZ'

stime = UTCDateTime('2019-08-16 12:59:10')
etime = stime + 120

client = Client()
inv=client.get_stations(network=net,station=sta,starttime=stime,endtime=etime,
                        channel=chan, level="response")
st = Stream()
st += client.get_waveforms(net,sta,loc,chan,stime,etime)


st.detrend('constant')
st.merge(fill_value=0)
st.attach_response(inv)
st.remove_response(output="DISP")
#st.rotate(method="->ZNE",inventory=inv)
st.filter("bandpass",freqmin=.5, freqmax=5)
tr = st[0]
t=np.linspace(0, (tr.stats.npts-1)/ tr.stats.sampling_rate,num=tr.stats.npts)

fig=plt.figure(1,figsize=(12,12))
plt.ylabel('Displacement (mm)',fontsize=14)
plt.xlim([0, 120])
plt.ylim([-.02 ,.02])
plt.xlabel('seconds after origin',fontsize=14)
plt.title('%s-%s-%s-%s, 2019-08-16, Hutchinson, KS Earthquake'%(net,sta,loc,chan),fontsize=14)

def animate(i):
    plt.plot(t[:(i+1)*100],tr[:(i+1)*100]*1000,'k')

ani = mpl.animation.FuncAnimation(fig, animate, frames=119, repeat=True)
#ani.save('R32B_KS20190816.gif', writer=writer)
plt.show()


