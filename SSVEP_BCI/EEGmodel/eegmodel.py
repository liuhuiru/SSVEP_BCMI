import numpy as np
import tensorflow as tf
from scipy import signal



class EEGmodel():
    def __init__(self, modelpath):
        self.model = tf.keras.models.load_model(modelpath, compile=False)

    # 滤波 6-50Hz 按通道数据进行
    def band_filter_process(self, input):
        b_HPF, a_HPF = signal.butter(4, 0.04, btype='highpass')  # 4阶，6Hz ， 6/(sampling_rate/2) 和iirfilter效果一样
        b_LPF, a_LPF = signal.butter(4, 0.333333, btype='lowpass')  # 4阶，50Hz ，50/(sampling_rate/2) 和iirfilter效果一样

        data_HF = signal.filtfilt(b_HPF, a_HPF, input)  # 零相位滤波，滤两次，反向多滤了一次
        band = signal.filtfilt(b_LPF, a_LPF, data_HF)  # 6-50

        return band

    def predict(self, eegdata, channels = [14, 15, 13, 22, 0, 6, 1, 5, 7]):
        #eegdata.shape=(24,300) => (9, 402, 1)
        window_length = 300
        data_length = 1200
        print(eegdata.shape)
        fftdata = []
        for i in range(len(channels)):
            filtered = self.band_filter_process(eegdata[channels[i], :])
            filtered = np.fft.rfft(filtered, data_length)/window_length
            data = np.concatenate((np.real(filtered)[round(5/0.25):round(55/0.25) + 1],np.imag(filtered)[round(5/0.25):round(55/0.25) + 1]),axis=0)
            fftdata.append(data)
        fftdata = np.expand_dims(np.array(fftdata), axis=-1)
        x= np.expand_dims(np.array(fftdata), axis=0)
        print('fftdata', fftdata.shape) #(9, 402)
        pred = self.model.predict(x)
        pred = tf.argmax(pred, axis=1)
        print(pred[0].numpy())
        return pred[0].numpy()

    # def predict(self, eegdata, channels = [14, 15, 13, 22, 0, 6, 1, 5, 7]):
    #     #eegdata.shape=(24,300) => (9, 402, 1)
    #     print(eegdata.shape)
    #     fftdata = []
    #
    #     window_length = 300
    #     data_length =
    #
    #     channel1_data = eegdata[channels[0], :]  # O1
    #     channel2_data = eegdata[channels[1], :]  # O2
    #     channel3_data = eegdata[channels[2], :]  # T3
    #     channel4_data = eegdata[channels[3], :]  # T6
    #     channel5_data = eegdata[channels[4], :]  # P3
    #     channel6_data = eegdata[channels[5], :]  # P4
    #     channel7_data = eegdata[channels[6], :]  # C3
    #     channel8_data = eegdata[channels[7], :]  # C4
    #     channel9_data = eegdata[channels[8], :]  # Cz
    #
    #     yd4_1 = self.band_filter_process(channel1_data)  # 滤波
    #     yd4_2 = self.band_filter_process(channel2_data)
    #     yd4_3 = self.band_filter_process(channel3_data)
    #     yd4_4 = self.band_filter_process(channel4_data)
    #     yd4_5 = self.band_filter_process(channel5_data)
    #     yd4_6 = self.band_filter_process(channel6_data)
    #     yd4_7 = self.band_filter_process(channel7_data)
    #     yd4_8 = self.band_filter_process(channel8_data)
    #     yd4_9 = self.band_filter_process(channel9_data)
    #
    #     for m in range(4):
    #         yd4_1_fft = np.fft.rfft(yd4_1[m * window_length:(m + 1) * window_length], data_length) / window_length
    #         yd4_2_fft = np.fft.rfft(yd4_2[m * window_length:(m + 1) * window_length], data_length) / window_length
    #         yd4_3_fft = np.fft.rfft(yd4_3[m * window_length:(m + 1) * window_length], data_length) / window_length
    #         yd4_4_fft = np.fft.rfft(yd4_4[m * window_length:(m + 1) * window_length], data_length) / window_length
    #         yd4_5_fft = np.fft.rfft(yd4_5[m * window_length:(m + 1) * window_length], data_length) / window_length
    #         yd4_6_fft = np.fft.rfft(yd4_6[m * window_length:(m + 1) * window_length], data_length) / window_length
    #         yd4_7_fft = np.fft.rfft(yd4_7[m * window_length:(m + 1) * window_length], data_length) / window_length
    #         yd4_8_fft = np.fft.rfft(yd4_8[m * window_length:(m + 1) * window_length], data_length) / window_length
    #         yd4_9_fft = np.fft.rfft(yd4_9[m * window_length:(m + 1) * window_length], data_length) / window_length
    #
    #     # for i in range(len(channels)):
    #     #     filtered = self.band_filter_process(eegdata[channels[i], :])
    #     #     data = np.concatenate((np.real(filtered)[round(5/0.25):round(55/0.25) + 1],np.imag(filtered)[round(5/0.25):round(55/0.25) + 1]),axis=0)
    #     #     fftdata.append(data)
    #     fftdata = np.expand_dims(np.array(fftdata), axis=-1)
    #     x= np.expand_dims(np.array(fftdata), axis=0)
    #     print('fftdata', fftdata.shape) #(9, 402)
    #     pred = self.model.predict(x)
    #     pred = tf.argmax(pred, axis=1)
    #     print(pred[0].numpy())
    #     return pred[0].numpy()


# testModel = EEGmodel(1)
# filepath = '../data/s1/block1.csv'
# data = np.loadtxt(open(filepath, "rb"), delimiter=",", skiprows=0)
# temp = np.delete(data,24,axis=1)
# eegdata = np.transpose(temp[0:300, :])
# print(eegdata.shape)
# testModel.predict(eegdata)





