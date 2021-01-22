from scipy.stats import ttest_ind

import pandas as pd

import statsmodels.stats.multitest


import numpy as np
import math
import concurrent.futures

import sys

import multiprocessing




class PerFeatureAlgorithm:
    def __init__(self,df,gra_index,grb_index):
        self.df=df
        self.gra_index=gra_index
        self.grb_index=grb_index

    def getresult(self):
        pass




class statlikealgo(PerFeatureAlgorithm):
    def bh_qvalue(self,pvals):

        return statsmodels.stats.multitest.multipletests(pvals,method="fdr_bh" )[1]








class TTest(statlikealgo):
    def getresult(self):



        ####multiprepare######


        totalrow= self.df.shape[0] ##########should be self.df.shape[0]





        chunk =multiprocessing.cpu_count()-1

        print("chunk===")
        print(chunk)




        if chunk==0:
            chunk=1


        trdGroupSize=math.floor(totalrow/chunk)

        if trdGroupSize==0:
            print("trd group size 0. Exit")

            sys.exit(1)






        trdend =0


        ####multiprepare######
        multiresult = []

        with concurrent.futures.ProcessPoolExecutor() as executor:

            processlist=[]
            for trdgrtemp in range(trdGroupSize):
                trdstart = trdend
                trdend = trdstart + trdGroupSize  ###end excluded in python subset
                if trdgrtemp == trdGroupSize - 1:
                    trdend = totalrow


                currentdf=self.df[trdstart:trdend]


                processlist.append(executor.submit(ttestformultiprocess,currentdf,self.gra_index,self.grb_index)) #######################



            for process in concurrent.futures.as_completed(processlist):

                multiresult.append(process.result())

        multiresultdf=pd.concat(multiresult)
        multiresultdf['qvalue'] = self.bh_qvalue(multiresultdf['pvalue'])
        return multiresultdf








def ttestformultiprocess(df,gra_index,grb_index):
    result = []

    for i in range(df.shape[0]):

        testrawresult = ttest_ind(df.iloc[i, gra_index], df.iloc[i, grb_index], equal_var=False,nan_policy='omit')[1]

        ####nan behaves correctly in python

        if np.isnan(testrawresult):
            testrawresult = 1

        result.append(testrawresult)



    result_df = pd.DataFrame(result, columns=['pvalue'], index=df.index.values)



    return result_df













