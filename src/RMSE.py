import matplotlib.pyplot as plt
import numpy as np
import librosa
import librosa.display
import IPython.display as ipd

# 1000 phần tử. mỗi 1s có 100 p.tử
# giá trị đầu tiên bằng trung bình của 100 phần tử

def funcRMSE(tool1_file):
    tool1, sr = librosa.load(tool1_file, duration = 15)
    FRAME_SIZE = 4096
    HOP_LENGTH = 512
    
    rms = librosa.feature.rms(y=tool1, frame_length=FRAME_SIZE, hop_length=HOP_LENGTH)[0]

    #Mảng arr là mảng 15 phần tử, mỗi phần tử là đoạn 1/15 cua rms được split ra
    arr = np.array_split(rms, 15)

    result = []
    result = [0 for i in range(15)] 
    window = 0

    #-----------------------Difference Percentage------------
    for i in range(len(arr)):
        sum = 0
        count = 0
        for j in range(len(arr[i])-1):
            if(arr[i][j] != 0):  
                sum += ((abs(arr[i][j] - arr[i][j+1]))/arr[i][j])*100
                #TBC hiệu 2 giá trị cạnh nhau / giá trị tiếp theo để tính xem 
                #năng lượng trung bình ở giá trị tiếp theo lệch bn % so với giá trị hiện tại

            else:
                sum += 0
            count += 1
        avg = sum/count
        result[window] = avg
        window += 1
    return result
