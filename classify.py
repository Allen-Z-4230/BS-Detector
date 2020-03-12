import pandas as pd
import numpy as np
import os
import mne
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from preprocessing import *

#############
# blf = [ep['bluffing'].average() for ep in epochs]
# nblf = [ep['not_bluffing'].average() for ep in epochs]
#############

epochs = [create_epochs(recording) for recording in recordings[1:]]

events = extract_events(np.array(recordings[0]['event_stream']))

# subject 1: Adrianna, subject 2: Lucas, subject 3: Allen
epochs = [mne.concatenate_epochs(epochs[:3]), epochs[3], epochs[4]]

for epoch in epochs:
    X, b_inds, nb_inds = get_features(epoch, tmin=-2)
    pca = PCA(n_components=2)
    X_t = pca.fit_transform(X)
    plot_pca(X_t*10**12, b_inds, nb_inds)

Y = np.zeros(X.shape[0])
Y[b_inds] = 0
Y[nb_inds] = 1

X_train, X_test, y_train, y_test = train_test_split(X, Y)

clf = SVC(gamma='auto')
clf.fit(X_train, y_train)
train_acc = clf.score(X_train, y_train)
test_acc = clf.score(X_test, y_test)
print(f'training accuracy : {train_acc}, testing accuracy: {test_acc}')
