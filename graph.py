import numpy as np
from matplotlib import mlab, pyplot

#Python 2.x:
#from __future__ import division

Fs = 48000
f = np.arange(1, 9) * 2000
t = np.arange(8 * Fs) / Fs 
x = np.empty(t.shape)
for i in range(8):
    x[i*Fs:(i+1)*Fs] = np.cos(2*np.pi * f[i] * t[i*Fs:(i+1)*Fs])

w = np.hamming(512)
Pxx, freqs, bins = mlab.specgram(x, NFFT=512, Fs=Fs, window=w, 
                                 noverlap=464)

#plot the spectrogram in dB

Pxx_dB = np.log10(Pxx)
pyplot.subplots_adjust(hspace=0.4)

pyplot.subplot(211)
ex1 = bins[0], bins[-1], freqs[0], freqs[-1]
pyplot.imshow(np.flipud(Pxx_dB), extent=ex1)
pyplot.axis('auto')
pyplot.axis(ex1)
pyplot.xlabel('time (s)')
pyplot.ylabel('freq (Hz)')

#zoom in at t=4s to show transient

pyplot.subplot(212)
n1, n2 = int(3.991/8*len(bins)), int(4.009/8*len(bins))
ex2 = bins[n1], bins[n2], freqs[0], freqs[-1]
pyplot.imshow(np.flipud(Pxx_dB[:,n1:n2]), extent=ex2)
pyplot.axis('auto')
pyplot.axis(ex2)
pyplot.xlabel('time (s)')
pyplot.ylabel('freq (Hz)')

pyplot.show()