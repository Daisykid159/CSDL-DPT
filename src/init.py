from Pitch import funcPitch
from aubio import pitch
from RMSE import funcRMSE
from PercentSilence import funcPercentSilence
from FrequencyMagnitude import funcFrequencyMagnitude

import os
# get subpath
listsubpath = []
for x in os.walk("D:/fullstrack/CSDLDPT/CSDL_DPT/src/File âm thanh"):
    listsubpath.append(x[0].replace("\\", "/"))

listsubpath.pop(0)

# get files
allpath = []
for subpath in listsubpath:
    f = []
    for (dirpath, dirnames, filenames) in os.walk(subpath):
        f.extend(filenames)
        break
    for namefile in f:
        allpath.append(subpath + "/" + namefile)

# write to csv
import csv

with open('D:/fullstrack/CSDLDPT/CSDL_DPT/src/CSDLDPT.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    header = ['Path', 'Pitch', 'RMSE', 'PercentSilence', 'FrequencyMagnitude']
    writer.writerow(header)
    
    for path in allpath:
        try:
            data = [
                path, 
                funcPitch(path, pitch), #xong
                funcRMSE(path), #xong
                funcPercentSilence(path),
                funcFrequencyMagnitude(path)
            ]
            writer.writerow(data)   
        except:
            print("======" + path)
            print('Have exception')
