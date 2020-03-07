from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import os
recordings = [pd.read_pickle(f) for f in os.listdir('.') if f.endswith('.pkl')]
ev_stream = np.array(recordings[0]['event_stream'])

ev_codes = {'D':1, 'A':2,'N':3,'B':4}

def extract_events(ev_stream, ev_codes):

    evs = []
    for letter, code in ev_codes.items():
        sp = np.where(ev_stream == letter)[0]
        evs.append(np.column_stack((sp, np.zeros(len(sp)), np.full(len(sp), code))))

    events = np.concatenate(evs)
    events = events[events[:, 0].argsort()]

    return  events



extract_events(ev_stream, ev_codes)
