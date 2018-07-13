'''
Created on 2016. 7. 17.

read mlf
create one class, so it makes possible to treat recognition and align results as two instances of the identical class.

@author: oster

Modified by Lucie
'''

class readMLF():
    '''
    read recognition and align mlf files
    each mlf contains only one sentence
    extract start time, end time, phone, likelihood
    for alignment, some line contains word at the last.
    '''

    def __init__(self, fname, mlfPos, types):
        import numpy as np
        import pandas as pd
        import os
        import re
        '''
        ex.
        fname = 'Japanese_001_0001'
        mlfPos = 'Japanese__recogNforcedDir'
        two types = 'recognition' or 'align'
        country = 'Japanese'
        '''
        if 'rec' in types:
            # Japanese_recogNforcedDir/Japanese_recognised
            fullName = '{}/{}'.format(mlfPos, fname)
        elif 'align' in types:
            # Japanese_recogNforcedDir/Japanese_aligned
            fullName = '{}/{}'.format(mlfPos, fname)

        self.fullName = fullName
        self.mlfName = os.path.split(fullName)[1]
        with open(fullName, 'rt') as fp:
            lineList = [line.strip() for line in fp if ('MLF' not in line) and ('rec' not in line) and (not re.match(r'^\.', line))]
        self.lineList = lineList
        # print(lineList)


    def df(self):
        import pandas as pd
        import numpy as np
        # make dataframe for ETS feat.
        df = pd.read_table(self.fullName, sep=' ', header=None, usecols=range(5), skiprows=2, skipfooter=1,engine='python', names = ['stTime', 'edTime', 'ph', 'likelihood', 'word'])
        df.stTime.astype(np.float32)
        df.edTime.astype(np.float32)
        # remove silences and short pauses from the start and end
        if df.iloc[0]['ph'].lower() == 'sil' or df.iloc[0]['ph'].lower() == 'sp':df = df.iloc[1:]
        if df.iloc[-1]['ph'].lower() == 'sil' or df.iloc[-1]['ph'].lower() == 'sp': df = df.iloc[:-1]

        df['start'] = df.stTime/10000000
        df['end'] = df.edTime/10000000
        # convert short pauses longer than 200 msec to silence
        # sp = (df['ph'] == 'sp')
        # sil = df['end'] - df['start'] > 0.2
        # df.loc[sp & sil, 'ph'] = 'sil'
        #
        # df['duration'] =  df['end'] - df['start']
        # print(df)

        return df

    def size(self):
        return len(self.lineList)

    def start(self):
        stList = []
        for line in self.lineList:
            if not line[0].isdigit():
                continue
            st = line.split(' ')[0]
            fl = float(st)
            stList.append(float(st)/10000000) # s
        return stList

    def end(self):
        edList = []
        for line in self.lineList:
            if not line[0].isdigit():
                continue
            ed = line.split(' ')[1]
            edList.append(float(ed)/10000000) # s

        return edList

    def phone(self):
        phoneList = []
        for line in self.lineList:
            if not line[0].isdigit():
                continue
            ph = line.split(' ')[2]
            phoneList.append(ph)
        return phoneList

    def likelihood(self):
        likelihoodList = []
        for line in self.lineList:
            if not line[0].isdigit():
                continue
            like = float(line.split(' ')[3])
            likelihoodList.append(like)
        return likelihoodList
