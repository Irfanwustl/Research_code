import pandas as pd

import per_feature_algorithm_multithreaded


import numpy as np

class StoreStat:
    def __init__(self,ref,pheno,outname,**kwargs):
        self.refdf=ref
        self.refdf = self.log2trans(self.refdf)
        self.phenoclassdf=pheno

        self.outame=outname

        self.coreAlgo()



    def coreAlgo(self):
        profile_list = self.generateProfile()
        assigned_list=self.assignFeature(profile_list)
        mergedProfile=self.mergeProfiles(assigned_list)
        outdf=self.addStatinfo(mergedProfile,assigned_list)

        outdf.to_csv(self.outame,sep="\t",na_rep="NA")





    def generateProfile(self):
        profilelist = []
        for i in range(self.phenoclassdf.shape[0]):
            classes = self.phenoclassdf.iloc[i, :]
            class1 = (classes == 1).tolist()
            class2 = (classes == 2).tolist()

            class1_mean = self.refdf.iloc[:, class1].mean(axis=1)
            class2_mean = self.refdf.iloc[:, class2].mean(axis=1)

            foldchange = class1_mean - class2_mean

            pfa=per_feature_algorithm_multithreaded.TTest(self.refdf, class1, class2)  ###########
            stat_liketest_result = pfa.getresult()
            stat_liketest_result["fold_change"] = foldchange

            ###########################################
            class1_repp=[class1]*((self.refdf).shape[0])
            class2_repp=[class2]*((self.refdf).shape[0])
            stat_liketest_result["class1"]=class1_repp
            stat_liketest_result["class2"]=class2_repp
            ##########################################

            profilelist.append(stat_liketest_result)
        return profilelist

    def assignFeature(self,profile_list):
        result = []
        for profile in profile_list:
            result.append(profile[profile["fold_change"] > 0])
        return result

    def mergeProfiles(self,profile_list):
        mergedFeatureList = []
        for profile in profile_list:

            mergedFeatureList.append(profile.index.tolist())

        flat_list = [item for sublist in mergedFeatureList for item in sublist]

        flat_list = pd.Series(flat_list).drop_duplicates().tolist()
        cslike_unlog = 2 ** self.refdf.loc[flat_list,:]  ################################################################################################

        return cslike_unlog

    def addStatinfo(self,mergeddf,assignedlist):
        allassigned = pd.concat(assignedlist)





        allassigned.index.name = mergeddf.index.name

        result=mergeddf.merge(allassigned, left_index=True, right_index=True)
        return result





    def log2trans(self,df):

        newdf=df+1

        return newdf.applymap(np.log2)

