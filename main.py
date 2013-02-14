#!/usr/bin/python

from datetime import datetime
from time import sleep
import pyaudio
import struct
import math
import numpy as np
from matplotlib import mlab, pyplot
import pymongo

#Python 2.x:
#from __future__ import division

INITIAL_TAP_THRESHOLD = 0.010
FORMAT = pyaudio.paInt16 
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 2
RATE = 44100  
INPUT_BLOCK_TIME = 0.005
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)
# if we get this many noisy blocks in a row, increase the threshold
OVERSENSITIVE = 15.0/INPUT_BLOCK_TIME                    
# if we get this many quiet blocks in a row, decrease the threshold
UNDERSENSITIVE = 120.0/INPUT_BLOCK_TIME 
# if the noise was longer than this many blocks, it's not a 'tap'
MAX_TAP_BLOCKS = 0.15/INPUT_BLOCK_TIME

def get_rms( block ):
    # RMS amplitude is defined as the square root of the 
    # mean over time of the square of the amplitude.
    # so we need to convert this string of bytes into 
    # a string of 16-bit samples...

    # we will get one short out for each 
    # two chars in the string.
    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )

    sum_squares = 0.0
    for sample in shorts:
        # sample is a signed short in +/- 32768. 
        # normalize it to 1.0
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n

    return math.sqrt( sum_squares / count )

class TapTester(object):
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.stream = self.open_mic_stream()
        self.tap_threshold = INITIAL_TAP_THRESHOLD
        self.noisycount = MAX_TAP_BLOCKS+1 
        self.quietcount = 0 
        self.errorcount = 0

    def stop(self):
        self.stream.close()

    def find_input_device(self):
        device_index = None            
        for i in range( self.pa.get_device_count() ):     
            devinfo = self.pa.get_device_info_by_index(i)   
            print( "Device %d: %s"%(i,devinfo["name"]) )

            for keyword in ["mic","input"]:
                if keyword in devinfo["name"].lower():
                    print( "Found an input: device %d - %s"%(i,devinfo["name"]) )
                    device_index = i
                    return device_index

        if device_index == None:
            print( "No preferred input found; using default input device." )

        return device_index

    def open_mic_stream( self ):
        device_index = self.find_input_device()

        stream = self.pa.open(   format = FORMAT,
                                 channels = CHANNELS,
                                 rate = RATE,
                                 input = True,
                                 input_device_index = device_index,
                                 frames_per_buffer = INPUT_FRAMES_PER_BLOCK)

        return stream

    def tapDetected(self):
        print "Tap!"

    def listen(self):
        try:
            block = self.stream.read(INPUT_FRAMES_PER_BLOCK)
        except IOError, e:
            # dammit. 
            self.errorcount += 1
            print( "(%d) Error recording: %s"%(self.errorcount,e) )
            self.noisycount = 1
            return

        amplitude = get_rms( block )
        if amplitude > self.tap_threshold:
            # noisy block
            self.quietcount = 0
            self.noisycount += 1
            if self.noisycount > OVERSENSITIVE:
                # turn down the sensitivity
                self.tap_threshold *= 1.1
        else:            
            # quiet block.
            if 1 <= self.noisycount <= MAX_TAP_BLOCKS:
                self.tapDetected()
                print "\t"
                print amplitude
            self.noisycount = 0
            self.quietcount += 1
            if self.quietcount > UNDERSENSITIVE:
                # turn up the sensitivity
                self.tap_threshold *= 0.9
        return amplitude if amplitude > self.tap_threshold else False

if __name__ == "__main__":
    tt = TapTester()
    mclient = pymongo.MongoClient("localhost", 27017)
    db = mclient.soundlog
    for i in range(2000000):
        amp = tt.listen()
        if amp:
            db.amps.save({"a":amp,"time" : datetime.now()})
    Fs = 48000
    f = np.arange(1, 9) * 2000
    t = np.arange(8 * Fs) / Fs
    x = np.empty(t.shape)
    for i in range(8):
        x[i*Fs:(i+1)*Fs] = np.cos(2*np.pi * f[i] * t[i*Fs:(i+1)*Fs])

    w = np.hamming(512)
    Pxx, freqs, bins = mlab.specgram(x, NFFT=512, Fs=Fs, window=w,
                                 noverlap=464)

    Pxx_dB = np.log10(Pxx)
    pyplot.subplots_adjust(hspace=0.4)
    
    pyplot.subplot(211)
    ex1 = bins[0], bins[-1], freqs[0], freqs[-1]
    pyplot.imshow(np.flipud(Pxx_dB), extent=ex1)
    pyplot.axis('auto')
    pyplot.axis(ex1)
    pyplot.xlabel('time (s)')
    pyplot.ylabel('freq (Hz)')
    pyplot.show()

