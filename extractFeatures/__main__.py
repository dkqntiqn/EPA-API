'''
Created on 2016. 7. 17.

@author: oster

Modified by Lucie
'''

from readMLF_exec import readMLF
from calculateETSFeatures import ETSFeat
import pandas as pd
from writeDataframe import writeExcel, makeDataframe
from calculateTimeFeature import getSegmentationFeatures

import numpy as np
import os,sys, pickle, sklearn
#
# from sklearn.neural_network import MLPClassifier
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score
# from sklearn.metrics import classification_report,confusion_matrix



def main(folder):

    COLUMNS = ['GOP','ROS', 'AR', 'PTR','Globsegdur', 'Numwds', 'Segdur', 'Wdpchk', 'Wpsec', 'Wpsecutt',
               'Secpchkmeandev', 'Wdpchkmeandev', 'Numsil', 'Silpwd', 'Silpsec', 'Silmean', 'Silmeandev',
               'Longpfreq', 'Longpmn', 'Longpwd', 'Longpmeandev', 'Silstddev', 'Longpstddev']
    df = pd.DataFrame(columns=COLUMNS)

    mlf_ls = os.listdir(folder)
    aligned_mlf = None
    recog_mlf = None
    for file in mlf_ls:
        if file.endswith(".mlf") and file.startswith("aligned"):
            aligned_mlf = file
        elif file.endswith(".mlf"):
            recog_mlf = file
    if not aligned_mlf or not recog_mlf:
        print("two mlf files are needed")
        return "Error Occured"

    aliMLF = readMLF(aligned_mlf, folder, 'align')
    # print(aliMLF.df())
    etsMLF = ETSFeat(aliMLF.df())
    recMLF = readMLF(recog_mlf, folder, 'recognition')

    df = makeDataframe("sample", aliMLF, recMLF, etsMLF, df)

    model = './extractFeatures/finalized_model.sav'

    loaded_model = pickle.load(open(model, 'rb'))
    result = loaded_model.predict(df)
    print("the score is:",result[0])
    return int(result[0])
    # print(df.head())
    #
    # writeExcel(df, './results/sample_Features.xlsx')

if __name__ == "__main__":
    main(sys.argv[1])
