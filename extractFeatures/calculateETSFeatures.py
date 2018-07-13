'''
Created on 2016. 7. 17.

calculate ETS features

Globsegdur
Wpsec
Wpsecutt
Segdur
Wdpchk
Secpchk
Secpchkmeandev
Wdpchkmeandev
Numsil
Silpwd
Silpsec
Silmean
Silmeandev
Longpfreq
Longpmn
Longpwd
Longpmeandev
Silstddev
Longpstdev


@author: oster
'''


class ETSFeat():
    def __init__(self, df):
        self.df = df
        self.long = 0.2
        self.df.duration = self.df.end - self.df.start
    def Numwds(self):
        '''
        Number of tokens
        words w/o silence
        originally disfluencies are counted, but in this case disfluency is not considered.
        '''
        numwds = len(self.df[(self.df.word != 'silence') & (self.df.word.notnull())].index)
        return numwds

    def Globsegdur(self):
        return self.df.duration.sum()

    def Segdur(self):
        '''
        Total duration of segment w/o disfluencies and pauses
        For now, disfluency is not considered, only silence
        '''
        return self.df.duration[(self.df.ph != 'sil') & (self.df.ph != 'sp')].sum()

    def Wdpchk(self):
        '''
        Average length of speech chunks
        average number of tokens in speech chunks separated by silence
        '''
        numSil = len(self.df[self.df.ph == 'sil'].index)
        numChk = numSil + 1
        numTok = len(self.df[(self.df.word.notnull()) & (self.df.ph != 'sil')].index)
        return float(numTok)/numChk

    def Secpchk(self):
        '''
        Average duration of speech chunks
        Segdur(feat4) / numChk
        '''
        segdur = self.Segdur()
        numSil = len(self.df[self.df.ph == 'sil'].index)
        numChk = numSil + 1
        return float(segdur)/numChk

    def Wpsec(self):
        '''
        Speech articulation rate
        numphs/Segdur
        '''
        numphs = self.Numwds()
        segdur = self.Segdur()
        return float(numphs)/segdur

    def Wpsecutt(self):
        '''
        Speech rate
        numphs/Globsegdur
        '''
        numphs = self.Numwds()
        globsegdur = self.Globsegdur()
        return float(numphs)/globsegdur

    def Secpchkmeandev(self):
        import pandas as pd
        '''
        Mean absolute deviation of speech chunks in seconds
        split dataframe by 'sil'
        get MAD in seconds
        '''
        chunkDurSeries = pd.Series()
        tempChunkDur = 0.0
        for i in self.df.index:
            if self.df.ph.loc[i] == 'sil':
                chunkDurSeries = chunkDurSeries.append(pd.Series([tempChunkDur]))
                tempChunkDur = 0.0
                continue
            elif i == len(self.df.index):
                tempChunkDur += self.df.duration.loc[i]
                chunkDurSeries = chunkDurSeries.append(pd.Series([tempChunkDur]))
                tempChunkDur = 0.0
                continue

            tempChunkDur += self.df.duration.loc[i]

        return chunkDurSeries.mad()

    def Wdpchkmeandev(self):
        import pandas as pd
        '''
        Mean absolute deviation of speech chunks in words
        split dataframe by 'sil'
        get MAD in number of words
        '''
        chunkNumWdSeries= pd.Series()
        tempChunkNumWd = 0
        for i in self.df.index:
            if self.df.ph.loc[i] == 'sil':
                #print tempChunkNumWd
                chunkNumWdSeries = chunkNumWdSeries.append(pd.Series([tempChunkNumWd]))
                tempChunkNumWd = 0
                continue
            elif i == len(self.df.index):
                #print tempChunkNumWd
                tempChunkNumWd += 1
                chunkNumWdSeries = chunkNumWdSeries.append(pd.Series([tempChunkNumWd]))
                tempChunkNumWd = 0
                continue
            elif self.df.word.loc[i] != None:
                #print self.df.word.loc[i]
                tempChunkNumWd += 1

            #tempChunkNumWd += self.df.duration.loc[i]

        #return chunkNumWdSeries.mad()
        return chunkNumWdSeries.mad()

    def Numsil(self):
        '''
        number of words 'sil'
        '''
        return self.df[self.df.ph == 'sil'].shape[0]

    def Silpwd(self):
        '''
        Duration of silences normalized by response length in words (number of words)
        Silpwd = durSil/Numwds
        '''
        # silpwd = durSil / Numwds
        numwds = self.Numwds()
        durSil = self.df.duration[self.df.ph == 'sil'].sum()
        return durSil/numwds

    def Silpsec(self):
        '''
        Duration of silences normalized by total word duration
        Silpsec = durSil/Segdur
        '''
        durSil = self.df.duration[self.df.ph == 'sil'].sum()
        segdur = self.Segdur()
        return durSil/segdur

    def Silmean(self):
        if self.Numsil() == 0:
            silmean = 0.0
        else:
            silmean = self.df.duration[self.df.ph == 'sil'].mean()
        return silmean

    def Silmeandev(self):
        '''
        Mean absolute deviation of duration of silences
        '''
        if self.Numsil() == 0:
            silmeandev = 0.0
        else:
            silmeandev = self.df.duration[self.df.ph == 'sil'].mad()
        return silmeandev

    def Longpfreq(self):
        '''
        Frequency of long pauses
        in this case, threshold of long pauses is 0.2s
        '''
        return self.df.duration[(self.df.ph == 'sil') & (self.df.duration >= self.long)].count()

    def Longpmn(self):
        '''
        Mean duration of long pauses
        '''

        if self.Longpfreq() == 0:
            longpmn = 0.0
        else:
            longpmn = self.df.duration[(self.df.ph == 'sil') & (self.df.duration > self.long)].mean()
        return longpmn

    def Longpwd(self):
        '''
        Frequency of long pauses normalized by response length in words
        Longpfreq(feat17)/Numwds(feat1)
        '''
        return float(self.Longpfreq())/self.Numwds()

    def Longpmeandev(self):
        '''
        mean deviation of long pause
        '''
        if self.Longpfreq() == 0:
            longpmeandev = 0.0
        else:
            longpmeandev = self.df.duration[(self.df.ph == 'sil') & (self.df.duration > self.long)].mad()

        return longpmeandev

    def Silstddev(self):
        '''
        Standard deviation of silence durations
        '''
        if self.Numsil() <= 1: silstddev = 0.0
        else: silstddev = self.df.duration[self.df.ph == 'sil'].std()
        return silstddev

    def Longpstddev(self):
        '''
        standard deviation of long pauses
        '''
        if self.Longpfreq()<=1: longpstddev = 0.0
        else: longpstddev = self.df.duration[(self.df.ph == 'sil') & (self.df.duration >= self.long)].std()
        return longpstddev
