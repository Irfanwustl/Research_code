import Tools
import sys
import pandas as pd

class ScaleMasterdf:
    def __init__(self,sm,finaldf,**kwargs):
        self.sm=sm
        self.finaldf=finaldf
        celllist = (self.sm['celltype']).tolist()
        celllist = [x for sublist in celllist for x in sublist]
        celllist = list(set(celllist))
        self.cells=celllist




        self.truecelltype="NotApplicable"
        self.samplename = "NotApplicable"  ## sample file name



        ###### for purified####
        if 'truecelltype' in kwargs:
            self.truecelltype=kwargs['truecelltype']

        if 'samplename' in kwargs:
            self.samplename =kwargs['samplename']



    def coreAlgo(self):
        accfeature=self.accfeatures()
        rejfeature=self.rejfeatures()

        outlist=self.calculate_pos_neg_scalefactor(accfeature,rejfeature)

        column_names = ["LinkageGroup","total","positive","negative","posDividedByTotal","SmCellType","TrueCellType","filename"]

        outdf=pd.DataFrame(outlist, columns=column_names)

        return outdf


    def calculate_pos_neg_scalefactor(self,posfeature,negfeature):
        caltools=Tools.ScalingFactorTools()


        ### check if posfeature and negfeature has equal number of cells (keys)
        samekey=set(posfeature.keys()) == set(negfeature.keys())
        if samekey==True:
            print("all cells covered")


        outlist=[]
        for cell in posfeature:
            tempposcounter=caltools.countDupInalistofSet(posfeature[cell])
            tempnegcounter=caltools.countDupInalistofSet(negfeature[cell])

            outlist=outlist+self.combine_posnegcounter(tempposcounter,tempnegcounter,cell)

        return outlist




    ### all lg is recorded. idea is first loop using pos and remove that from the neg. add remaining neg  #####
    def combine_posnegcounter(self,poscounter,negcounter,cell):

        outlist=[]
        for lg in poscounter:
            #print(set(map(eval,lg)))


            if lg in negcounter:
                templist=[set(map(eval,lg)),poscounter[lg]+negcounter[lg],poscounter[lg],negcounter[lg],1.0*poscounter[lg]/(poscounter[lg]+negcounter[lg]),cell,self.truecelltype,self.samplename]

                del negcounter[lg] ### it works in place
            else:
                templist = [set(map(eval,lg)), poscounter[lg] + 0, poscounter[lg], 0,
                            1.0 * poscounter[lg] / (poscounter[lg] + 0), cell, self.truecelltype,
                            self.samplename]

            outlist.append(templist)


        for lg in negcounter:
            templist = [set(map(eval,lg)), 0 + negcounter[lg], 0, negcounter[lg],
                        1.0 * 0 / (0 + negcounter[lg]), cell, self.truecelltype,
                        self.samplename]

            outlist.append(templist)

        return outlist







    def accfeatures(self):
        outdict = {}
        for cell in self.cells:
            celldf = self.finaldf[self.finaldf['finalacceptedfor'] == cell]
            correscpg = (celldf['acceptedCpG']).tolist()
            correscpg = list(map(frozenset, correscpg))

            #correscpg = list(set(correscpg))
            outdict[cell] = correscpg ### what if a cell has no correscpg?????
        return outdict

    def rejfeatures(self):
        outdict = {}

        for cell in self.cells:
            # print(" \""+cell+"\"")
            negmask = self.finaldf['finalrejectedfor'].apply(
                lambda x: ("\"" + cell + "\"" in x) or (" \"" + cell + "\"" in x))  ###check

            neg = self.finaldf[negmask]

            correscpg = (neg['notacceptedCpG']).tolist()

            correscpg = self.realCorresCpg(correscpg, cell)

            correscpg = list(map(frozenset, correscpg))

            #correscpg = list(set(correscpg))
            outdict[cell] = correscpg

        return outdict


    def realCorresCpg(self,correscpg, cell):
        realcorres = []
        for cpglist in correscpg:
            temp = []
            for ccpg in cpglist:

                eccpg = eval(ccpg)

                if not eccpg:  #####################################check thoroughly
                    continue

                chrom, start = eccpg.split(":")

                fromsm = self.sm[(self.sm['chrom'] == chrom) & (self.sm['start'] == int(start))]
                if fromsm.shape[0] != 1:
                    print("error. Exiting")
                    sys.exit(1)

                celltype = fromsm['celltype']
                celltype = [x for sublist in celltype for x in sublist]
                if len(celltype) != 1:
                    print("wrong.Exiting")
                    sys.exit(1)

                if cell == celltype[0]:
                    temp.append(ccpg)

            if len(temp) != 0:
                realcorres.append(temp)

        return realcorres