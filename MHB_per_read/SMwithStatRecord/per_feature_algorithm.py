from scipy.stats import ttest_ind

import pandas as pd

import statsmodels.stats.multitest


import numpy as np


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



        result=[]




        for i in range (self.df.shape[0]):


            testrawresult=ttest_ind(self.df.iloc[i, self.gra_index], self.df.iloc[i, self.grb_index],  equal_var=False)[1]


            ####nan behaves correctly in python

            if np.isnan(testrawresult):


                testrawresult=1




            result.append(testrawresult)


        result_df=pd.DataFrame(result,columns=['pvalue'],index=self.df.index.values)



        result_df['qvalue'] = self.bh_qvalue(result_df['pvalue'])
        return result_df

















