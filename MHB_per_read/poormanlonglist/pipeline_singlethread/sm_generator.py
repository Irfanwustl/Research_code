'''
qvalue name is used here

'''


import numpy as np

import pandas as pd

import per_feature_algorithm as pfa_module

import math



class CsLikeSM:

    def __init__(self, refdf, phenoclassdf,qcutoff,foldcutoff,**kwargs):

        self.rawdata=refdf
        self.refdf = self.log2trans(refdf)



        self.phenoclassdf = phenoclassdf
        self.qcutoff=qcutoff
        self.foldcutoff=foldcutoff
        ########################
        self.sortcriteria="fold_change"
        self.numofFeature=math.inf

        self.finalSMval="median"




        if 'sortcriteria' in kwargs.keys():
            self.sortcriteria = kwargs['sortcriteria']

        if "numofFeature" in kwargs.keys():
            self.numofFeature=kwargs["numofFeature"]

        if "finalSMval" in kwargs.keys():
            self.finalSMval=kwargs["finalSMval"]





        #############################
        if "outdir" in kwargs.keys():
            self.outdir=kwargs["outdir"]
        else:
            print ("provide outdir")

        if "smName" in kwargs.keys():
            self.smName=kwargs["smName"]
        else:
            self.smName="SigMatrix"



    def log2trans(self,df):

        newdf=df+1

        return newdf.applymap(np.log2)



    def generateSM(self):

        profile_list=self.generateProfile()



        filtered_profile=self.filterProfile(profile_list)




        sorted_profile=self.sortProfie(filtered_profile)



        merged_profile=self.mergeProfile(sorted_profile)


        SM=self.takefinalSMval(merged_profile)

        SM.index.names=["NAME"]

        print(self.condNumber(SM))


        self.afterSM(SM)

        return SM


    def afterSM(self,SM):
        self.saveSM(SM)
        #self.saveFig(SM)

    def saveSM(self,SM):
        outfile=self.outdir+"/"+self.smName
        SM.to_csv(outfile, sep="\t")

    def condNumber(self,SM):
        return np.linalg.cond(SM, p=2)


    def saveFig(self,SM):
        raw_sm_data=self.rawdata.loc[SM.index,:]

        print("not implemented")





    def takefinalSMval(self, mergedProfile):
        mergedDF = pd.DataFrame()
        for i in range(self.phenoclassdf.shape[0]):
            classes = self.phenoclassdf.iloc[i, :]
            class1 = (classes == 1).tolist()

            if self.finalSMval=="mean":

                newdf=(mergedProfile.iloc[:,class1].mean(axis=1)).to_frame(name=["NAME",self.phenoclassdf.index[i]])

            elif self.finalSMval=="median":

                newdf=pd.DataFrame(mergedProfile.iloc[:, class1].median(axis=1),columns=[self.phenoclassdf.index[i]])#(mergedProfile.iloc[:, class1].median(axis=1)).to_frame(name=self.phenoclassdf.index[i])

            else:
                print("...........ERROR: finalSMval not supported")



            if i==0:

                mergedDF=newdf

            else:

                mergedDF =mergedDF.merge(newdf, left_index=True,right_index=True)
                #mergedDF = mergedDF.merge(newdf)
                #mergedDF=mergedDF.set_index(mergedDF.iloc[:,0])



        return mergedDF






    def mergeProfile(self,profile_list):

        mergedFeatureList=[]


        for profile in profile_list:
            if profile.shape[0]>self.numofFeature:
                mergedFeatureList.append((profile.index[0:self.numofFeature]).tolist())

            else:
                mergedFeatureList.append(profile.index.tolist())


        flat_list = [item for sublist in mergedFeatureList for item in sublist]


        flat_list=pd.Series(flat_list).drop_duplicates().tolist()
        cslike_unlog=2**self.refdf.loc[flat_list,:] ################################################################################################

        return cslike_unlog


    def sortProfie(self,profile_list):
        result=[]
        for profile in profile_list:
            if self.sortcriteria=="fold_change":
                result.append(profile.sort_values(by=["fold_change"],ascending=False))



            elif self.sortcriteria=="qvalue":
                result.append(profile.sort_values(by=["qvalue"]))
            else:
                print("...........ERROR: Sort not supported")
        return result

    def filterProfile(self,profile_list):
        result=[]
        for profile in profile_list:
            result.append(profile[(profile['qvalue']<=self.qcutoff) & (profile["fold_change"] > self.foldcutoff)])
        return result






    ###template pattern###
    def generateProfile(self):
        profilelist=[]
        for i in range (self.phenoclassdf.shape[0]) :
            classes = self.phenoclassdf.iloc[i, :]
            class1 = (classes == 1).tolist()
            class2 = (classes == 2).tolist()


            class1_mean=self.refdf.iloc[:,class1].mean(axis=1)
            class2_mean=self.refdf.iloc[:,class2].mean(axis=1)

            foldchange=class1_mean-class2_mean





            stat_liketest_result=self.per_feature_hooked(self.refdf,class1,class2)
            stat_liketest_result["fold_change"]=foldchange

            profilelist.append(stat_liketest_result)
        return profilelist


    def per_feature_hooked(self,df,gra_index,grb_index):
        pass



class TTest_hooked(CsLikeSM):
    def __init__(self, refdf, phenoclassdf, per_feature_algorithm,qcutoff,foldcutoff,**kwargs):
        super().__init__(refdf, phenoclassdf,qcutoff,foldcutoff,**kwargs)

        self.PerFeatureAlgotithm = getattr(pfa_module, per_feature_algorithm)


    def per_feature_hooked(self,df,gra_index,grb_index):
        ttest = self.PerFeatureAlgotithm(df, gra_index, grb_index)
        return ttest.getresult()



