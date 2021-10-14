import pandas as pd
from collections import defaultdict
import sys

class ParseMasterDF:
    def __init__(self,MasterDf,celltyplist,**kwargs):
        self.masterdf=MasterDf
        self.celltypes=celltyplist





        self.minCpGforpositivecall=1
        if 'minCpGforpositivecall' in kwargs:
            self.minCpGforpositivecall=kwargs['minCpGforpositivecall']

        self.percentCpGcoverforrejection=1.0 ##full cover. If negative int, it means integer cover 
        if  'percentCpGcoverforrejection' in kwargs:
            self.percentCpGcoverforrejection = kwargs['percentCpGcoverforrejection']


        self.rejectionmode="ov" ####overlapping
        if 'rejectionmode' in kwargs:
            if kwargs['rejectionmode']=="nov":  ####not overlapping
                self.rejectionmode="nov"








    def coreAlgo(self):
        self.prepareNotassigneddf()
        self.determinepositivehits()
        ABSestimate,poscount,allcount,negcount=self.inferABSresult()

        ABSestimate=pd.DataFrame(ABSestimate)

        ABSestimateNormalized=ABSestimate.div(ABSestimate.sum(axis=1), axis=0)


        poscountdf=pd.DataFrame(poscount)
        allcountdf=pd.DataFrame(allcount)
        negcountdf=pd.DataFrame(negcount)





        return self.masterdf,ABSestimate,ABSestimateNormalized,poscountdf,allcountdf,negcountdf


    def inferABSresult(self):
        ABSdict=defaultdict(list)
        posdict=defaultdict(list)
        alldict=defaultdict(list)
        negdict=defaultdict(list)
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
            posdict[cell].append(pos)
            alldict[cell].append(pos+neg)
            negdict[cell].append(neg)

        return dict(ABSdict),dict(posdict),dict(alldict),dict(negdict)


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
            self.findcorressnegativereads(cell,cellcorresrejectiondf)


            for index, prow in positiverows.iterrows():
                if len(prow['acceptedCpG']) >= self.minCpGforpositivecall:

                    if int(prow['len_hypolist'])>=0.6*(int(prow['len_hyperlist'])+int(prow['len_hypolist'])):
                        if self.masterdf.loc[index, 'finalacceptedfor']=='notdetermined':

                            self.masterdf.loc[index, 'finalacceptedfor'] = cell
                        else:
                            print('already finalacceptedfor has value. Something wrong?')

                    



                    











    '''
    def cellspecificrejectiondf(self,cell):
        cellrejectionlist = []
        for index, row in self.notassignedrelevantDF.iterrows():

            if cell in row['ucelltype']:
                cellrejectionlist.append(row)
        crdf = pd.DataFrame(cellrejectionlist)


        return crdf
    '''
    def cellspecificrejectiondf(self,cell):

        crdf=(self.notassignedrelevantDF[pd.DataFrame(self.notassignedrelevantDF.ucelltype.tolist()).isin([cell]).any(1).values]).copy()
        
        return crdf

    

    def findcorressnegativereads(self,cell,cellcorresrejectiondf):
        if self.rejectionmode=="ov":
            print("ov not implemented")
            sys.exit(1)

            #self.ovcorressnegativereads(cell,prow,cellcorresrejectiondf)

        elif self.rejectionmode=="nov":
            self.novcorressnegativereads(cell,cellcorresrejectiondf)


    def novcorressnegativereads(self,cell,cellcorresrejectiondf):
        for index, row in cellcorresrejectiondf.iterrows():
            currentrejcpg=set(row['notacceptedCpG'])
            if len(currentrejcpg)>=self.minCpGforpositivecall:
                if self.masterdf.loc[index, 'finalrejectedfor']=='notdetermined':
                    self.masterdf.at[index, 'finalrejectedfor'] = [cell]
                else:
                    if cell not in self.masterdf.loc[index, 'finalrejectedfor']:
                        self.masterdf.loc[index, 'finalrejectedfor'].append(cell)


    ######not efficient. So not using. If necessary, implelement again#####
    '''
    def ovcorressnegativereads(self,cell,prow,cellcorresrejectiondf):
        poscpg=set(prow['acceptedCpG'])
        poscpglen=len(poscpg)
        flag = 0
        for index, row in cellcorresrejectiondf.iterrows():
            currentrejcpg=set(row['notacceptedCpG'])
            intersected=currentrejcpg.intersection(poscpg)



            if self.percentCpGcoverforrejection<0:
                if len(intersected)>=abs(self.percentCpGcoverforrejection):
                    if self.masterdf.loc[index, 'finalrejectedfor']=='notdetermined':
                        self.masterdf.at[index, 'finalrejectedfor'] = [cell]
                    else:
                        if cell not in self.masterdf.loc[index, 'finalrejectedfor']:
                            self.masterdf.loc[index, 'finalrejectedfor'].append(cell)


                    flag=1

            elif len(intersected)>=(1.0*self.percentCpGcoverforrejection*poscpglen):
                if self.masterdf.loc[index, 'finalrejectedfor']=='notdetermined':
                    self.masterdf.at[index, 'finalrejectedfor'] = [cell]
                else:
                    if cell not in self.masterdf.loc[index, 'finalrejectedfor']:
                        self.masterdf.loc[index, 'finalrejectedfor'].append(cell)


                flag=1

        '''
        
        





