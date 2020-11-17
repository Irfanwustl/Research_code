"""
this class takes a sm and a mastrdir which has subdir with cell type name. Then it parse the final file of the sub dir.
"""



import os
import sys
import pandas as pd








class FilterFeature:
    def __init__(self, sm, masterdir, outfilepath, **kwargs):
        self.sm=sm
        self.masterdir=masterdir

        self.outfilepath=outfilepath

        self.coreAlgo()



    def coreAlgo(self):
        subdirlist=self.parsedir(self.masterdir)


        gropedsm=self.sm.groupby("celltype")

        rejectionlist=[]
        for subdir in subdirlist:
            flag=0
            for name, group in gropedsm:
                namelist=name[1:-1].split(',')

                if len(namelist)!=1:
                    print("sm error. Exiting")
                    sys.exit(1)


                celltype=namelist[0]

                if subdir==eval(celltype):
                    flag=1


                    finalfileList=self.parsedir(self.masterdir+"/"+subdir)




                    for finalfile in finalfileList:

                        finalfiledf=pd.read_csv(self.masterdir+"/"+subdir+"/"+finalfile,sep="\t")
                        finalfiledf['acceptedCpG'] = finalfiledf.acceptedCpG.apply(lambda x: x[1:-1].split(','))
                        rejectionlist=rejectionlist+self.rejectionCandidate(group,finalfiledf,celltype)


            if flag==0:
                print("subdir corres celltype not found. Exiting ",subdir)
                sys.exit(1)


        rejectionlist=list(set(rejectionlist))
        finalsmldf, rejectedsmdf=self.manipulateRejectionlist(rejectionlist)

        finalsmldf.to_csv(self.outfilepath+"_adjusted.txt",sep="\t",index=False)
        rejectedsmdf.to_csv(self.outfilepath+"_rejected.txt",sep="\t",index=False)


    def manipulateRejectionlist(self,rejectionlist):
        finalsmlist=[]
        rejectedsmlist=[]
        for index, row in self.sm.iterrows():
            chrom=row['chrom']
            start=row['start']
            cpgname=chrom+":"+str(start)

            if cpgname in rejectionlist:
                rejectedsmlist.append(row)
            else:
                finalsmlist.append(row)


        finalsmldf=pd.DataFrame(finalsmlist)
        rejectedsmdf=pd.DataFrame(rejectedsmlist)


        return finalsmldf,rejectedsmdf





    def rejectionCandidate(self,groupdf,finalfile,celltype):


        celldf = finalfile[finalfile['finalacceptedfor'] == celltype]
        correscpg = (celldf['acceptedCpG']).tolist()

        correscpg = [x for sublist in correscpg for x in sublist]

        correscpg = [i for i in correscpg if i]

        correscpg = list(map(eval, correscpg))

        correscpgunique = list(set(correscpg))

        groupdfcpg=groupdf['chrom'].map(str) + ':' + groupdf['start'].map(str)
        groupdfcpg=groupdfcpg.tolist()
        groupdfcpg=set(groupdfcpg)
        correscpgunique=set(correscpgunique)

        rejcpg=groupdfcpg-correscpgunique

        sanity=correscpgunique-groupdfcpg
        if len(sanity)!=0:
            print("some error in set calculation. Exiting")
            sys.exit(1)


        return list(rejcpg)




    def parsedir(self,dir):
        subdirs=[f for f in os.listdir(dir) if not f.startswith('.')]
        return subdirs















