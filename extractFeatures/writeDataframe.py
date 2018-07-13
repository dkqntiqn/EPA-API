'''
Created on 2016. 7. 18.

@author: oster
'''

import pandas as pd
from pandas import ExcelWriter
import os
from calculateTimeFeature import getSegmentationFeatures, getGOPFeature

def makeDataframe(wavName, aliMLF, recMLF, etsMLF, df):
    wavFileName = os.path.splitext(wavName)[0] 

    ROS, AR, PTR = getSegmentationFeatures(aliMLF)
    GOP = getGOPFeature(aliMLF, recMLF)

    
    df.loc[wavFileName] = [GOP, ROS, AR, PTR, etsMLF.Globsegdur(), etsMLF.Segdur(), etsMLF.Wdpchk(), etsMLF.Secpchk(), etsMLF.Wpsec(),
                           etsMLF.Wpsecutt(), etsMLF.Secpchkmeandev(), etsMLF.Wdpchkmeandev(), etsMLF.Numsil(), etsMLF.Silpwd(),
                           etsMLF.Silpsec(), etsMLF.Silmean(), etsMLF.Silmeandev(), etsMLF.Longpfreq(), etsMLF.Longpmn(), 
                           etsMLF.Longpwd(), etsMLF.Longpmeandev(), etsMLF.Silstddev(), etsMLF.Longpstddev()]
    return df


def writeExcel(df, excelName):
    writer = ExcelWriter(excelName)
    df.to_excel(writer)
    writer.save()
    pass