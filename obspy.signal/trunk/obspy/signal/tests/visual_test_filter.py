#!/usr/bin/env python

from pylab import *
from numpy import *
from obspy.core import read
import obspy.filter, os, inspect
from scipy.signal import remez, convolve, get_window, firwin
import gzip

file = os.path.join(os.path.dirname(inspect.getfile(obspy)), "gse2",
                    "tests", "data", "loc_RNON20040609200559.z")
#g = obspy.Trace()
#g.read(file,format='GSE2')
g = read(file, format='GSE2')

#data = array(g.data,dtype='f')
data = array(g[0].data, dtype='f')
newdata = data[0.45 * 1e4:0.59 * 1e4]

fmin = 5.
fmax = 20.

tworunzph = obspy.filter.lowpassZPHSH(newdata, fmin, corners=4)
olifir = obspy.filter.lowpassFIR(newdata, fmin)

clf()
plot(newdata, 'r', linewidth='1', label='Original Data')
plot(tworunzph, 'b', linewidth='2', label='2 Run Zero Phase Butterworth Lowpass Filtered')
plot(olifir, 'g', linewidth='2', label='FIR lowpass Filtered')
title("Compare Zero Phase Lowpass Methods, Lowpass @ 5Hz")
legend()

#visualization of filter tests below
file = os.path.join(os.getcwd(), 'data', 'rjob_20051006.gz')
f = gzip.open(file)
d = loadtxt(file)
f.close()

figure()
sp_1 = subplot(211)
title("Bandpass Test, 5-10Hz, 4 corners / 2 sections")
file = os.path.join(os.getcwd(), 'data', 'rjob_20051006_bandpass.gz')
f = gzip.open(file)
p = loadtxt(file)
f.close()
o = obspy.filter.bandpass(d, 5, 10, df=200, corners=4)
plot(p, label="PITSA")
plot(o, label="ObsPy")
legend()
subplot(212, sharex=sp_1)
rms = sqrt(sum((p - o) ** 2) / sum(p ** 2))
title("RMS: %s" % rms)
plot(p - o, label="Difference PITSA-ObsPy")
legend()

figure()
sp_2 = subplot(211)
title("Bandpass Zero-Phase-Shift Test, 5-10Hz, 2 corners / 1 section")
file = os.path.join(os.getcwd(), 'data', 'rjob_20051006_bandpassZPHSH.gz')
f = gzip.open(file)
p = loadtxt(file)
f.close()
o = obspy.filter.bandpassZPHSH(d, 5, 10, df=200, corners=2)
plot(p, label="PITSA")
plot(o, label="ObsPy")
legend()
subplot(212, sharex=sp_2)
rms = sqrt(sum((p - o) ** 2) / sum(p ** 2))
rms2 = sqrt(sum((p[:-200] - o[:-200]) ** 2) / sum(p[:-200] ** 2))
title("RMS: %s   RMS(w/o last 200 samples): %s" % (rms, rms2))
plot(p - o, label="Difference PITSA-ObsPy")
legend()

figure()
sp_3 = subplot(211)
title("Lowpass Test, 5Hz, 4 corners / 2 section")
file = os.path.join(os.getcwd(), 'data', 'rjob_20051006_lowpass.gz')
f = gzip.open(file)
p = loadtxt(file)
f.close()
o = obspy.filter.lowpass(d, 5, df=200, corners=4)
plot(p, label="PITSA")
plot(o, label="ObsPy")
legend()
subplot(212, sharex=sp_3)
rms = sqrt(sum((p - o) ** 2) / sum(p ** 2))
title("RMS: %s" % rms)
plot(p - o, label="Difference PITSA-ObsPy")
legend()

figure()
sp_4 = subplot(211)
title("Lowpass Zero-Phase-Shift Test, 5Hz, 2 corners / 1 section")
file = os.path.join(os.getcwd(), 'data', 'rjob_20051006_lowpassZPHSH.gz')
f = gzip.open(file)
p = loadtxt(file)
f.close()
o = obspy.filter.lowpassZPHSH(d, 5, df=200, corners=2)
plot(p, label="PITSA")
plot(o, label="ObsPy")
legend()
subplot(212, sharex=sp_4)
rms = sqrt(sum((p - o) ** 2) / sum(p ** 2))
rms2 = sqrt(sum((p[:-200] - o[:-200]) ** 2) / sum(p[:-200] ** 2))
title("RMS: %s   RMS(w/o last 200 samples): %s" % (rms, rms2))
plot(p - o, label="Difference PITSA-ObsPy")
legend()

figure()
sp_5 = subplot(211)
title("Highpass Test, 10Hz, 4 corners / 2 section")
file = os.path.join(os.getcwd(), 'data', 'rjob_20051006_highpass.gz')
f = gzip.open(file)
p = loadtxt(file)
f.close()
o = obspy.filter.highpass(d, 10, df=200, corners=4)
plot(p, label="PITSA")
plot(o, label="ObsPy")
legend()
subplot(212, sharex=sp_5)
rms = sqrt(sum((p - o) ** 2) / sum(p ** 2))
title("RMS: %s" % rms)
plot(p - o, label="Difference PITSA-ObsPy")
legend()

figure()
sp_6 = subplot(211)
title("Highpass Zero-Phase-Shift Test, 10Hz, 2 corners / 1 section")
file = os.path.join(os.getcwd(), 'data', 'rjob_20051006_highpassZPHSH.gz')
f = gzip.open(file)
p = loadtxt(file)
f.close()
o = obspy.filter.highpassZPHSH(d, 10, df=200, corners=2)
plot(p, label="PITSA")
plot(o, label="ObsPy")
legend()
subplot(212, sharex=sp_6)
rms = sqrt(sum((p - o) ** 2) / sum(p ** 2))
rms2 = sqrt(sum((p[:-200] - o[:-200]) ** 2) / sum(p[:-200] ** 2))
title("RMS: %s   RMS(w/o last 200 samples): %s" % (rms, rms2))
plot(p - o, label="Difference PITSA-ObsPy")
legend()

figure()
sp_7 = subplot(211)
title("Envelope Test")
file = os.path.join(os.getcwd(), 'data', 'rjob_20051006_envelope.gz')
f = gzip.open(file)
p = loadtxt(file)
f.close()
o = obspy.filter.envelope(d)
plot(p, label="PITSA")
plot(o, label="ObsPy")
legend()
subplot(212, sharex=sp_6)
rms = sqrt(sum((p - o) ** 2) / sum(p ** 2))
title("RMS: %s" % rms)
plot(p - o, label="Difference PITSA-ObsPy")
legend()

show()
