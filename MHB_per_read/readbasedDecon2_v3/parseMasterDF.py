import pandas as pd
from collections import defaultdict

class ParseMasterDF:
    def __init__(self,MasterDf,celltyplist,**kwargs):
        self.masterdf=MasterDf
        self.celltypes=celltyplist





        self.minCpGforpositivecall=1
        if 'minCpGforpositivecall' in kwargs:
            self.minCpGforpositivecall=kwargs['minCpGforpositivecall']

        self.percentCpGcoverforrejection=1.0 ##full cover
        if  'percentCpGcoverforrejection' in kwargs:
            self.percentCpGcoverforrejection = kwargs['percentCpGcoverforrejection']





    def coreAlgo(self):
        self.prepareNotassigneddf()
        self.determinepositivehits()
        ABSestimate=pd.DataFrame(self.inferABSresult())

        ABSestimateNormalized=ABSestimate.div(ABSestimate.sum(axis=1), axis=0)





        return self.masterdf,ABSestimate,ABSestimateNormalized


    def inferABSresult(self):
        ABSdict=defaultdict(list)
        for cell in self.celltypes:

            pos=(self.masterdf[self.masterdf['finalacceptedfor']==cell]).shape[0]



            #neg=(self.masterdf[cell in self.masterdf['finalrejectedfor']]).shape[0]

            negmask=self.masterdf['finalrejectedfor'].apply(lambda x: cell in x)
            neg=(self.masterdf[negmask]).shape[0]

            '''
            print(cell)
            print(pos)
            print(neg)
            '''

            if pos+neg >0:
                ratio=1.0*pos/(pos+neg)
            else:
                ratio=0
            ABSdict[cell].append(ratio)

        return dict(ABSdict)


    def prepareNotassigneddf(self):
        temp=self.masterdf[self.masterdf['assignedcelltype'] == 'NotAssigned']


        relevantnotassigned=[]
        for index, nrow in temp.iterrows():


            if len(nrow['notacceptedCpG'])>0:
                if len(nrow['notacceptedCpG'])==1 and nrow['notacceptedCpG'][0]=="":
                    if len(nrow['mismatchCpG'])>0:
                        if len(nrow['mismatchCpG']) == 1 and nrow['mismatchCpG'][0] == "":
                            pass
                        else:
                            relevantnotassigned.append(nrow)



                else:
                    relevantnotassigned.append(nrow)

            else:
                if len(nrow['mismatchCpG']) > 0:
                    if len(nrow['mismatchCpG']) == 1 and nrow['mismatchCpG'][0] == "":
                        pass
                    else:
                        relevantnotassigned.append(nrow)





        self.notassignedrelevantDF=pd.DataFrame(relevantnotassigned)





    def determinepositivehits(self):

        for cell in self.celltypes:
            positiverows=self.masterdf[self.masterdf['assignedcelltype']==cell]

            cellcorresrejectiondf=self.cellspecificrejectiondf(cell)


            for index, prow in positiverows.iterrows():
                if len(prow['acceptedCpG']) >= self.minCpGforpositivecall:
                    if self.masterdf.loc[index, 'finalacceptedfor']=='notdetermined':

                        self.masterdf.loc[index, 'finalacceptedfor'] = cell
                    else:
                        print('already finalacceptedfor has value. Something wrong?')



                    self.findcorressnegativereads(cell,prow,cellcorresrejectiondf)












    def cellspecificrejectiondf(self,cell):
        cellrejectionlist = []
        for index, row in self.notassignedrelevantDF.iterrows():

            if cell in row['ucelltype']:
                cellrejectionlist.append(row)
        crdf = pd.DataFrame(cellrejectionlist)


        return crdf

    def findcorressnegativereads(self,cell,prow,cellcorresrejectiondf):
        poscpg=set(prow['acceptedCpG'])
        poscpglen=len(poscpg)
        flag = 0
        for index, row in cellcorresrejectiondf.iterrows():
            currentrejcpg=set(row['notacceptedCpG'])
            intersected=currentrejcpg.intersection(poscpg)



            if len(intersected)>=(1.0*self.percentCpGcoverforrejection*poscpglen):
                if self.masterdf.loc[index, 'finalrejectedfor']=='notdetermined':
                    self.masterdf.loc[index, 'finalrejectedfor'] = [cell]
                else:
                    if cell not in self.masterdf.loc[index, 'finalrejectedfor']:
                        self.masterdf.loc[index, 'finalrejectedfor'].append(cell)


                flag=1

        '''
        if flag==0:
            print("no rejection")
            print(cell)
            print(poscpg)
        '''





