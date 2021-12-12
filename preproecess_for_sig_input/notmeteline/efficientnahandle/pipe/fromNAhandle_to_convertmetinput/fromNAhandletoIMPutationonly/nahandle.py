import pandas as pd
import sys

class NaHandle:
    def __init__(self, ref, pheno, rate, outname, **kwargs):
        self.ref=pd.read_csv(ref,sep="\t",index_col=0)
        self.pheno=pd.read_csv(pheno,sep="\t",header=None,index_col=0)
        self.rate=rate
        self.outname=outname

        self.coreAlgo()


    def coreAlgo(self):
        naindex=self.allNAindex()

        allnoselindex=[]
        for i in range(self.pheno.shape[0]):
            classes = self.pheno.iloc[i, :]


            class1 = (classes == 1).tolist()

            class1total=(classes == 1).sum()



            class1cutoff=class1total*self.rate*1.0

            tmp=naindex.iloc[:, class1]

            tmpsum=tmp.sum(axis=1)
            tmpsumselectedindex=tmpsum[tmpsum>class1cutoff].index

            allnoselindex.append(tmpsumselectedindex.tolist())







        allnoselindex = [x for sublist in allnoselindex for x in sublist]

        allnoselindex=list(set(allnoselindex))

        outdf = self.ref[~self.ref.index.isin(allnoselindex)]

        outdf.to_csv(self.outname,sep="\t",na_rep="NA")



    def allNAindex(self):
        return self.ref.isna()







def main():
    reffile = sys.argv[1]
    phenfile=sys.argv[2]
    rate=float(sys.argv[3])  #### 0.4. rate of NA per group. 0 mean no na
    outname = sys.argv[4]

    nh=NaHandle(reffile,phenfile,rate,outname)

if __name__ == '__main__':
    main()