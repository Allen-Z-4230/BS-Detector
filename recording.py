from NeuroPy import NeuroPy
import pandas as pd
import keyboard
import time


def input_data(data, neuropy):
    print('RECORDING STARTED, YAYY')
    while True:
        data['attention'].append(neuropy.attention)
        data['meditation'].append(neuropy.meditation)
        data['delta'].append(neuropy.delta)
        data['theta'].append(neuropy.theta)
        data['lowAlpha'].append(neuropy.lowAlpha)
        data['highAlpha'].append(neuropy.highAlpha)
        data['lowBeta'].append(neuropy.lowBeta)
        data['highBeta'].append(neuropy.highBeta)
        data['lowGamma'].append(neuropy.lowGamma)
        data['midGamma'].append(neuropy.midGamma)

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

        if keyboard.is_pressed('esc'):
            print("RECORDING ENDED")
	    neuropy.stop()
            sn = raw_input('Enter session number')
            df = pd.DataFrame.from_dict(data)
            df.to_pickle('./session_'+ str(sn) + '.pkl')
            break

	
	print(neuropy.attention, neuropy.meditation)

        time.sleep(.1)	


def record(neuropy):
    data = {
        'attention': [],
        'meditation': [],
        'delta': [],
        'theta': [],
        'lowAlpha': [],
        'highAlpha': [],
        'lowBeta': [],
        'highBeta': [],
        'lowGamma': [],
        'midGamma': [],
        'event_stream': []
    }

    neuropy.start()

    while True:
        if neuropy.poorSignal < 80:
            input_data(data, neuropy)
            break
        else:
            print("Bad signal, retrying connection...")
	    print(neuropy.poorSignal, neuropy.attention)
            time.sleep(1)


def main():
    x = NeuroPy('/dev/tty.MindWaveMobile-DevA', 57600)
    record(x)

if __name__=='__main__':
	main()
