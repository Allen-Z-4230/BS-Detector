from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import os
import mne

# List of dataframes
recordings = [pd.read_pickle(f) for f in os.listdir('.') if f.endswith('.pkl')]

# settings
mne.set_log_level(verbose="warning")
epoch_settings = dict(event_id=dict(call=1, no_call=2, not_bluffing=3, bluffing=4),
                      tmin=-4, tmax=4)


def extract_events(ev_stream):

    evs = []
    ev_codes = {'D': 1, 'A': 2, 'N': 3, 'B': 4}
    for letter, code in ev_codes.items():
        sp = np.where(ev_stream == letter)[0]
        evs.append(np.column_stack((sp, np.zeros(len(sp)), np.full(len(sp), code))))

    events = np.concatenate(evs)
    events = events[events[:, 0].argsort()]

    return events.astype(int)


def calc_iti(events, srate):
    n_events = events.shape[0]
    iti = np.zeros(n_events - 1)
    for ind in range(1, n_events):
        iti[ind - 1] = (events[ind] - events[ind-1])[0]
    return iti/srate


def create_raw(df, sfreq=10):

    # define data array, channel names, and channel types to create info object
    df = df.drop(columns=['event_stream'])
    data = df.values.T
    ch_names = df.columns.tolist()
    info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types='eeg')

    return mne.io.RawArray(data, info)


def create_epochs(raw):
    epochs = mne.Epochs(create_raw(raw),
                        events=extract_events(np.array(raw['event_stream'])),
                        **epoch_settings, preload=True)
    return epochs


def get_features(epochs, tmin=-4, tmax=0, bins=4):
    epochs = epochs['bluffing', 'not_bluffing']
    t_delt = (tmax - tmin)/bins
    ranges = [(tmin + t_delt*i, tmin + t_delt*(i+1)) for i in range(0, bins)]
    X = np.concatenate([epochs.copy().crop(tmin=min, tmax=max).get_data().mean(axis=2)
                        for (min, max) in ranges], axis=1)
    _, b_inds = epochs._getitem(['bluffing'], return_indices=True)
    _, nb_inds = epochs._getitem(['not_bluffing'], return_indices=True)

    Y = np.zeros(X.shape[0])
    Y[b_inds] = 0
    Y[nb_inds] = 1

    return X, Y


def plot_pca(data, Y):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel('Principal Component 1', fontsize=15)
    ax.set_ylabel('Principal Component 2', fontsize=15)
    ax.set_title('PCA Decomposition of Neurosky Features', fontsize=20)
    targets = ['Bluffing', 'Not Bluffing']
    colors = ['r', 'b']
    inds = [Y == 0, Y == 1]
    for target, color, ind in zip(targets, colors, inds):
        ax.scatter(data[ind, 0], data[ind, 1], c=color, s=50)
        ax.legend(targets)
        ax.grid()
    plt.show()


def tt_split(percent_training):
    pass


def main():
    epochs = mne.Epochs(create_raw(recordings[1]),
                        events=extract_events(np.array(recordings[1]['event_stream'])),
                        event_id=event_id, tmin=tmin, tmax=tmax)
    epochs['bluffing'].average().plot()
    epochs['not_bluffing'].average().plot()


if __name__ == '__main__':
    main()
