# Authors: Romain Trachel <romain.trachel@ens.fr>
#
# License: Artistic License (2.0)

import time
import numpy as np

from random import random
from simpleOSC import initOSCClient, initOSCServer, setOSCHandler, sendOSCMsg, closeOSC, \
        createOSCBundle, sendOSCBundle, startOSCServer

import mne
from mne.realtime import FieldTripClient
from mne.filter import band_pass_filter
from mne.time_frequency import cwt_morlet

ip = "127.0.0.1"
client_port = 8001

n_samples = 2000
fmin = 8
fmax = 12

baseline = 3
bp_base = []

n_eeg = 16
sfreq = 250
picks = np.arange(n_eeg)

# takes args : ip, port
initOSCClient(ip=ip, port=client_port)

# takes args : ip, port, mode --> 0 for basic server,
# 1 for threading server, 2 for forking server
initOSCServer(ip=ip, port=6400, mode=1)

# and now set it into action
startOSCServer()

# get measurement info guessed by MNE-Python
ch_names = ['EEG-%i' % i for i in np.arange(n_eeg)]
raw_info = mne.create_info(ch_names, sfreq)

with FieldTripClient(info=raw_info, host='localhost', port=1972,
                     tmax=150, wait_max=10) as rt_client:

    tstart = time.time()
    told = tstart
    for ii in range(100):
        epoch = rt_client.get_data_as_epoch(n_samples=n_samples, picks=picks)
        filt = band_pass_filter(epoch.get_data(), sfreq, fmin, fmax)
        # compute band power features
        bp = np.log10(np.abs(cwt_morlet(filt[0], sfreq, [(fmin + fmax) / 2.])))
        if told - tstart < baseline:
            bp_base.append(bp[:, 0, n_samples/2].mean())
        else:
            bp_sample = bp[:, 0, n_samples/2].mean()
            bp_ratio = (np.mean(bp_base) - bp_sample) / np.mean(bp_base)
            sendOSCMsg("/nmx/bandpower/", [bp_ratio])
            print "%i - sending /nmx/bandpower/%i" %(ii, bp_ratio)

        tcurrent = time.time()
        time.sleep(.5)
        told = tcurrent
