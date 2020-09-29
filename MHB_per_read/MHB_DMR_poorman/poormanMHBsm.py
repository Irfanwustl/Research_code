import pandas as pd
import math


class poormanMHBsm:
    def __init__(self, statinfo, phenodf, qcutoff, fcutoff, numfeature, **kwargs):
        self.statinfo = statinfo
        self.pheno = phenodf
        self.qcutoff = qcutoff #<=
        self.fcutoff = fcutoff  # > 0
        self.numfeature = numfeature

        self.radius = 0  # out put default sm


        if 'radius' in kwargs.keys():
            self.radius = kwargs['radius']

        self.supportingpcutoff = 0.9 #<=
        self.supportingqcutoff = 1 #<=
        self.supportingfcutoff = 0 #>

        if 'supportingpcutoff' in kwargs.keys():
            self.supportingpcutoff=kwargs['supportingpcutoff']

        if 'supportingqcutoff' in kwargs.keys():
            self.supportingqcutoff=kwargs['supportingqcutoff']

        if 'supportingfcutoff' in kwargs.keys():
            self.supportingfcutoff=kwargs['supportingfcutoff']


        self.minblocksize=2 ### at least 2 cpg in every block

        if 'minblocksize' in kwargs.keys():
            self.minblocksize = kwargs['minblocksize']

        self.coreAlgo()


    def coreAlgo(self):
        filteredDF = self.filterdf(self.statinfo)
        sortedDF = self.sortdf(filteredDF)


        MHB = self.createMHB(sortedDF)
        MHBsorted=self.sortdf(MHB)


        ########### SM ######################
        SMlike=self.createSMlike(MHBsorted)
        Smlike_surebalanced=self.adjustgroupsize(MHBsorted)





        print(MHB)
    def postprocessing(self,SMlike):
        SMlikedroppedstatinf

    #df must be sorted
    def adjustgroupsize(self,df):
        grouped = df.groupby('class1')
        minsize=math.inf
        for name, group in grouped:
            csize=group.shape[0]
            if  csize <=minsize:
                minsize=csize
        if minsize >=self.numfeature:
            return self.createSMlike(df)
        else:
            sigcpglist = []
            for name, group in grouped:

                if group.shape[0] > minsize:
                    sigcpglist.append(group.head(minsize))

                else:

                    sigcpglist.append(group)

            return pd.concat(sigcpglist)





    ############################################################
    def infercelltype(self):
        inferredcelltype = self.statinfo.class1.unique()
        return inferredcelltype

    ############################################################

    def filterdf(self, df):
        outdf = df[(df['qvalue'] <= self.qcutoff) & (df["fold_change"] > self.fcutoff)]
        return outdf

    ### also makes the df unique
    def sortdf(self, filterddf):
        outdf = filterddf.sort_values(by=["fold_change"], ascending=False)
        outdf = outdf[~outdf.index.duplicated(keep='first')]

        return outdf

    def createSMlike(self, sorteddf, **kwargs):

        sigcpglist = []

        grouped = sorteddf.groupby('class1')

        for name, group in grouped:

            if group.shape[0] > self.numfeature:
                sigcpglist.append(group.head(self.numfeature))

            else:

                sigcpglist.append(group)

        return pd.concat(sigcpglist)

    def createMHB(self, SMlike):

        groupedFullstat = self.statinfo.groupby('class1')
        groupedSMlike = SMlike.groupby('class1')

        result=[]
        for sname, sgroup in groupedSMlike:
            for fullname, fullgroup in groupedFullstat:
                if sname==fullname:
                    result.append(self.mhbpergroup(sgroup,fullgroup))

        return pd.concat(result)



    def mhbpergroup(self,sgroup,fullgroup):
        RI_sgroup=sgroup.reset_index() #reset index

        RI_fullgroup=fullgroup.reset_index()


        RI_sgroup[["chrom","pos"]]=RI_sgroup[sgroup.index.name].str.split(pat=":",expand=True)
        RI_sgroup["pos"] = RI_sgroup["pos"].astype(int)


        RI_fullgroup[["chrom","pos"]]=RI_fullgroup[fullgroup.index.name].str.split(pat=":",expand=True)
        RI_fullgroup["pos"]=RI_fullgroup["pos"].astype(int)


        result=[]
        for smindex, smrow in RI_sgroup.iterrows():

            upper=smrow["pos"]-self.radius
            lower=smrow["pos"]+self.radius

            supportfromfull=RI_fullgroup.loc[(RI_fullgroup["chrom"] == smrow["chrom"]) & (RI_fullgroup["pos"] >= upper) & (RI_fullgroup["pos"] <= lower) & (RI_fullgroup["pvalue"]<=self.supportingpcutoff) & (RI_fullgroup["qvalue"]<=self.supportingqcutoff) & (RI_fullgroup["fold_change"]>self.supportingfcutoff)]




            if supportfromfull.shape[0]>=self.minblocksize:
                mhbstart=(supportfromfull["pos"].min())-1
                mhbend=(supportfromfull["pos"].max())+1

                tempdf=smrow
                tempdf["start"]=mhbstart
                tempdf["end"]=mhbend


                result.append(tempdf)



                ##### to avoid overlapping ######

                cond = RI_fullgroup[fullgroup.index.name].isin(supportfromfull[fullgroup.index.name])
                RI_fullgroup.drop(RI_fullgroup[cond].index,inplace = True)





        outdf=pd.DataFrame(result)
        return outdf










