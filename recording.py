from NeuroPy import NeuroPy
import pandas as pd
import keyboard
import time


def input_data(data, neuropy):
    while True:
        data['attention'].append(neuropy.attention)
        data['meditation'].append(neuropy.meditation)
        data['delta'].append(neuropy.delta)
        data['theta'].append(neuropy.theta)
        data['lowAlpha'].append(neuropy.lowAlpha)
        data['highAlhpa'].append(neuropy.highAlhpa)
        data['lowBeta'].append(neuropy.lowBeta)
        data['highBeta'].append(neuropy.highBeta)
        data['lowGamma'].append(neuropy.lowGamma)
        data['midGamma'].append(neuropy.midGamma)

        if keyboard.is_pressed('esc'):
            neuropy.stop()
            sn = input('Enter session number')
            df = pd.DataFrame.from_dict(data)
            df.to_pickle(f'./session_{sn}.pkl')
            break

        if keyboard.is_pressed('B'):
            data['event_stream'].append('B')
        elif keyboard.is_pressed('N'):
            data['event_stream'].append('N')
        elif keyboard.is_pressed('A'):
            data['event_stream'].append('A')
        elif keyboard.is_pressed('D'):
            data['event_stream'].append('D')
        else:
            data['event_stream'].append(0)

        time.sleep(.1)


def record(neuropy):
    data = {
        'attention': [],
        'meditation': [],
        'delta': [],
        'theta': [],
        'lowAlpha': [],
        'highAlhpa': [],
        'lowBeta': [],
        'highBeta': [],
        'lowGamma': [],
        'midGamma': [],
        'event_stream': []
    }

    neuropy.start()

    while True:
        if neuropy.poorSignal == 200:
            input_data(data, neuropy)
            break
        else:
            print("Bad signal, retrying connection...")
            time.sleep(.1)


def main():
    x = NeuroPy(dev_loc, 9600)
    record(x)
