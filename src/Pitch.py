import sys
import numpy as np
from aubio import source, pitch

# 700 phần tử. mỗi 1s có 100 p.tử
# giá trị đầu tiên bằng trung bình của 100 phần tử

def funcPitch(path, pitch):
    win_s = 4096
    hop_s = 512

    samplerate = 44100
    s = source(path, samplerate, hop_s)
    samplerate = s.samplerate

    #### Giá trị mặc định của tolerance trong nhiều thư viện pitch estimation thường là 0.8.
    tolerance = 0.8

    pitch_o = pitch("yin", win_s, hop_s, samplerate)
    pitch_o.set_unit("midi")
    pitch_o.set_tolerance(tolerance)

    pitches = []
    confidences = []

    total_frames = 0
    while True:
        samples, read = s()
        pitch = pitch_o(samples)[0]
        pitches += [pitch]
        confidence = pitch_o.get_confidence()
        confidences += [confidence]
        total_frames += read
        if read < hop_s: break

    result = []

    # print(len(pitches))
    step = int(len(pitches)/15)

    for i in range(0, 15, 1):
        max = step*(i+1)
        if(i == 14):
            max = len(pitches) - 1
        pitchLocal = []
        for j in range(step*i, max, 1):
            pitchLocal.append(pitches[j])
        result.append(np.array(pitchLocal).mean())  # tính trung bình 

    return result