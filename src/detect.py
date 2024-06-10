from Pitch import funcPitch
from aubio import pitch
from RMSE import funcRMSE
from PercentSilence import funcPercentSilence
from FrequencyMagnitude import funcFrequencyMagnitude

### % phần trăm khoảng lặng 0,1
### độ lệch năng lượng 0,3
### pitch 0,3
### tần số có mật độ lớn nhất 0,3
from attribute import toolInstrumentVoice
from result import pathAndResult

configPercentSilence = 0.1
configRMSE = 0.3
configPitch = 0.3
configFrequencyMagnitude = 0.3

def compareFile(att1, att2): 
    maxRes = 1
    for i in range(15):
        for j in range(15):
            # giongnhau
            same = float(abs(att1[i].percentSilence - att2[j].percentSilence) / max(att1[i].percentSilence, att2[j].percentSilence) * configPercentSilence)
            same = same + float(abs(att1[i].RMSE - att2[j].RMSE) / max(att1[i].RMSE, att2[j].RMSE) * configRMSE)
            same = same + float(abs(att1[i].pitch - att2[j].pitch) / max(att1[i].pitch, att2[j].pitch) * configPitch)
            same = same + float(abs(att1[i].magnitude - att2[j].magnitude) / max(att1[i].magnitude, att2[j].magnitude) * configFrequencyMagnitude / 2)
            same = same + float(abs(att1[i].frequency - att2[j].frequency) / max(att1[i].frequency, att2[j].frequency) * configFrequencyMagnitude / 2)
            if(maxRes > same):
                maxRes = same
    
    return maxRes
    
###################################### input ###########################
path = "D:/fullstrack/CSDLDPT/CSDL_DPT/src/File âm thanh/1 Cello/cello_01.wav"

att1 = [] 

pitchAtt = funcPitch(path, pitch)
RMSEAtt = funcRMSE(path)
percentSilenceAtt = funcPercentSilence(path)
frequencyMagnitudeAtt = funcFrequencyMagnitude(path)

magnitudeAtt = []
frequencyAtt = []

for a, b in frequencyMagnitudeAtt:
    magnitudeAtt.append(a)
    frequencyAtt.append(b)

for i in range(15):
    att1.append(
        toolInstrumentVoice(
            pitchAtt[i],
            RMSEAtt[i],
            percentSilenceAtt[i],
            magnitudeAtt[i],
            frequencyAtt[i]
        )
    )



####################################### get data csv #######################
import csv

with open('D:/fullstrack/CSDLDPT/tool_instrument_voice_recognition/src/CSDLDPT.csv', 'r', encoding='UTF8') as f:
    reader = csv.reader(f)
    l = [row for row in reader]
    metadata = []
    for row in range(len(l)):
        if row > 1 and row %2 == 0 :
            metadata.append(l[row])


lastResult = []
for i in range(len(metadata)):
    att = []

    Pitch = metadata[i][1].strip("[]").split(', ')
    RMSE = metadata[i][2].strip("[]").split(', ')
    PercentSilence = metadata[i][3].strip("[]").split(', ')
    frequencyMagnitudeAtt = metadata[i][4].strip("[]").replace("(", "").replace(")", "").split(', ')

    magnitudeAtt = []
    frequencyAtt = []
    for e in range(30):
        if e % 2 == 1:
            frequencyAtt.append(frequencyMagnitudeAtt[e])
        else:
            magnitudeAtt.append(frequencyMagnitudeAtt[e])

    for j in range(15):
        att.append(
            toolInstrumentVoice(
                float(Pitch[j]),
                float(RMSE[j]),
                float(PercentSilence[j]),
                float(magnitudeAtt[j]),
                float(frequencyAtt[j])
            )
        )

    lastResult.append(
        pathAndResult(
            "Type: " + metadata[i][0].split('/')[7],
            compareFile(att1, att)
        )
    )



#### result
    
for i in range(30):
    for j in range(30):
        if(lastResult[i].distance < lastResult[j].distance):
            swap = lastResult[i]
            lastResult[i] = lastResult[j]
            lastResult[j] = swap

for i in range(3):
    print(lastResult[i].type, lastResult[i].distance)
