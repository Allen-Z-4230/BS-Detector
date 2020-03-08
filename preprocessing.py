from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import os
import mne

# List of dataframes
recordings = [pd.read_pickle(f) for f in os.listdir('.') if f.endswith('.pkl')]

# settings
event_id = dict(call=1, no_call=2, not_bluffing=3, bluffing=4)
tmin, tmax = -2, 2


def extract_events(ev_stream):

    evs = []
    ev_codes = {'D': 1, 'A': 2, 'N': 3, 'B': 4}
    for letter, code in ev_codes.items():
        sp = np.where(ev_stream == letter)[0]
        evs.append(np.column_stack((sp, np.zeros(len(sp)), np.full(len(sp), code))))

    events = np.concatenate(evs)
    events = events[events[:, 0].argsort()]

    return events.astype(int)


def create_raw(df, sfreq=10):

    # define data array, channel names, and channel types to create info object
    df = df.drop(columns=['event_stream'])
    data = df.values.T
    ch_names = df.columns.tolist()
    info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types='eeg')

    return mne.io.RawArray(data, info)


def main():

    epochs = mne.Epochs(create_raw(recordings[0]),
                        events=extract_events(np.array(recordings[0]['event_stream'])),
                        event_id=event_id, tmin=tmin, tmax=tmax)

    epochs['bluffing'].average().plot()
    epochs['not_bluffing'].average().plot()
