import numpy as np
import pymongo
from matplotlib import mlab, pyplot
from datetime import datetime, date, time, timedelta
from pylab import *
#Python 2.x:
#from __future__ import division

#plot the spectrogram in dB
#t1 = np.arange(0.0, 5.0, 0.1)
#t2 = np.arange(0.0, 5.0, 0.02)
#pyplot.figure(1)
#pyplot.subplot(211)
#pyplot.plot(t1, f(t1), 'bo', t2, f(t2), 'k')
#pyplot.show()

"""
dt = 0.0005
t = arange(0.0, 20.0, dt)
s1 = sin(pi*t)
s2 = sin(t)
print s1
# create a transient "chirp"
mask = where(logical_and(t>10, t<12), 1.0, 0.0)
s2 = s2 * mask

x = s1 + s2 # the signal
NFFT = 1024       # the length of the windowing segments
Fs = int(1.0/dt)  # the sampling frequency

plot(t, x)
Pxx, freqs, bins, im = specgram(x, NFFT=NFFT, Fs=Fs, noverlap=900,cmap=cm.gist_heat)
show()
"""
Fs = 256.0        # Hz
duration = 1     # seconds

m = pymongo.MongoClient()
db = m.soundlog
data = db.amps
amps = []
for doc in data.find():
    amps.append(double(Fs*doc['a']))

t = np.arange(0, duration, 1 / Fs)


frequency = 100.0    # Hz
amplitude = 4.0     # volts
y = amps #amplitude * np.sin(2 * np.pi * frequency * t)
pyplot.plot(t, y)
pyplot.show()

#for item in db.my_collection.find():
#   print item["x"]
