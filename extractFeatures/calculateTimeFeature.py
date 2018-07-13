'''
Created on 2016. 7. 17.

@author: oster
'''
from readMLF import readMLF
from numpy import mean



VOWELSET = set([
                "AA0", "AA1", "AA2", "AE0", "AE1", "AE2", "AH0", "AH1", "AH2", "AO0", "AO1", "AO2",
           "AW0", "AW1", "AW2", "AY0", "AY1", "AY2", "EH0", "EH1", "EH2", "ER0", "ER1", "ER2",
           "EY0", "EY1", "EY2", "IH0", "IH1", "IH2", "IY0", "IY1", "IY2", "OW0", "OW1", "OW2",
           "OY0", "OY1", "OY2", "UH0", "UH1", "UH2", "UW0", "UW1", "UW2"
                ])

def getSegmentationFeatures(aliMLF):
    nSyll = 0 # number of syllable
    start = 1e+10 # start time
    end = 0 # end time
    articulationTime = 0 # articulation time

    phList = aliMLF.phone()
    stList = aliMLF.start()
    edList = aliMLF.end()


    for i in range(len(phList)):
        ph = phList[i]
        # print(ph)
        if ph == 'sil' or ph == 'sp': continue
        articulationTime += edList[i] - stList[i]

        if stList[i] < start: start = stList[i]
        if edList[i] > end: end = edList[i]
        if ph in VOWELSET: nSyll += 1

    speechRate = float(nSyll)/(end-start)
    articulationRate = float(nSyll)/articulationTime
    phonationTimeRatio = float(articulationTime)/(end-start)
    # print(nSyll)
    return speechRate, articulationRate, phonationTimeRatio


def getGOPFeature(aliMLF, recMLF):
    phList_ali = aliMLF.phone()
    stList_ali = aliMLF.start()
    edList_ali = aliMLF.end()
    lkList_ali = aliMLF.likelihood()
    stList_rec = recMLF.start()
    edList_rec = recMLF.end()
    lkList_rec = recMLF.likelihood()
    phoneGOPList = []

    # phoneGOP
    for i in range(len(phList_ali)):
        phAli = phList_ali[i]
        if phAli == 'sil' or phAli == 'sp': continue
        phoneGOP = lkList_ali[i] # initialized as p_qi(forced)
        alignPhoneDur = edList_ali[i] - stList_ali[i]
        if alignPhoneDur == 0.0: continue # do not count short pause which has zero duration

        for j in range(recMLF.size()):
            if stList_rec[j] >= stList_ali[i] and edList_rec[j] <= edList_ali[i]:
                # (t3-t2)/(t4-t1) * p_qi(rec)
                phoneGOP -= lkList_rec[j] * (edList_rec[j] - stList_rec[j])/alignPhoneDur
            elif edList_rec[j] >= stList_ali[i] and edList_rec[j] <= edList_ali[i]:
                # (t2-t1)/(t4-t1) * p_qi(rec)
                phoneGOP -= (edList_rec[j]-stList_ali[i])/alignPhoneDur * lkList_rec[j]
            elif  stList_rec[j] >= stList_ali[i] and stList_rec[j] <= edList_ali[i]:
                # (t4-t3)/(t4-t1)*p_qi(rec)
                phoneGOP -= (edList_ali[i]-stList_rec[j])/alignPhoneDur * lkList_rec[j]
            elif stList_rec[j] <= stList_ali[i] and edList_rec[j] >= edList_ali[i]:
                phoneGOP -= lkList_rec[j]
        phoneGOPList.append(phoneGOP)

    return mean(phoneGOPList)
