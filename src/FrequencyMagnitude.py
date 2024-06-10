import os
import matplotlib.pyplot as plt
import librosa, librosa.display
import IPython.display as ipd
import numpy as np

# 1500 phần tử. mỗi 1s có 100 p.tử
# giá trị đầu tiên bằng trung bình của 100 phần tử

# Mảng X_mag trả về một mảng bao gồm: 
# Giá trị của phần tử = giá trị magnitude, 
# vị trí của phần tử đó = hz tương ứng => Dùng 2 mảng để lưu lại 2 giá trị đó

def funcFrequencyMagnitude(audio_dir):

    audio, sr = librosa.load(audio_dir, duration = 15)

    #Mảng X là mảng chứa dãy tần số và mật độ của nó (Mặc định thì độ lớn của mật độ là số ảo ) (Số thực = mật độ / Số ảo = giá trị pha (Ko cần))
    X = np.fft.fft(audio)

    #Lấy giá trị tuyệt đối thì sẽ có được phần số thực
    X_mag = np.absolute(X) 

    f = np.linspace(0, sr, len(X_mag))
    f_bins = int(len(X_mag))  

    f[:f_bins], X_mag[:f_bins]

    #Freq là mảng ghi tần số có mức độ xuất hiện lớn nhất
    freq =[]
    freq = [0 for i in range(15)]

    #Magnitude là cụ thể mức độ xuất hiện là bao nhiêu
    magnitude =[]
    magnitude = [0 for i in range(15)]

    position = 0
    max = 0
    pos = 0

    for i in range(0, len(X_mag)):        
        if(X_mag[i] > max):
            max = X_mag[i]
            pos = i
        if(i> 0):
            if( (i % int(len(X_mag)/15)) == 0 and i != len(X_mag)-1):            
                freq[position] = pos
                magnitude[position] = max
                position += 1
                max = 0
            if(i == len(X_mag)-1):            
                freq[position] = pos
                magnitude[position] = max

        
    pairs = list(zip(freq, magnitude))
    return pairs
