import pandas as pd
import sys


class AllCompartmentMean:
    def __init__(self, imputedfile, metoutfile, phenofile, outname, **kwargs):
        self.imputedfile = pd.read_csv(imputedfile,sep="\t",index_col=0)
        self.metoutfile = pd.read_csv(metoutfile,sep="\t",header=None)
        self.pheno = pd.read_csv(phenofile, sep="\t", header=None, index_col=0)
        self.outname = outname
        self.coreAlgo()

    def coreAlgo(self):


        rowmeandf=self.rowmean()

        rowmeandf=rowmeandf.reset_index()



        rowmeandf[['chrom', 'pos']]=rowmeandf.iloc[:,0].str.split(":",expand=True)


        rowmeandf['pos']=rowmeandf['pos'].astype(int)



        outdf=self.finalout(rowmeandf)

        filsuffix="_".join(str(x) for x in self.pheno.index)

        out=self.outname+"_"+filsuffix+".txt"

        outdf.to_csv(out,sep="\t",index=False,header=False)

    def finalout(self,rowmeandf):

        rowlist=[]
        for index, row in self.metoutfile.iterrows():     ###tqdm
            mchrom=row[0]
            mstart=row[1]
            mend=row[2]

            tempdf=rowmeandf[(rowmeandf['chrom']==mchrom) & (rowmeandf['pos']>=mstart) & (rowmeandf['pos']< mend)]


            tempsize=pd.Series({"mycpgcount":tempdf.shape[0]})

            tempmean=tempdf[self.pheno.index].mean()



            temprow=row.append(tempmean)
            temprow=temprow.append(tempsize)


            rowlist.append(temprow)

        outdf=pd.DataFrame(rowlist)



        return outdf


    def rowmean(self):
        rowmeanlist = []

        for i in range(self.pheno.shape[0]):
            classes = self.pheno.iloc[i, :]
            class1 = (classes == 1).tolist()
            class1_mean = self.imputedfile.iloc[:, class1].mean(axis=1)

            temdf =class1_mean.to_frame(self.pheno.index[i])

            rowmeanlist.append(temdf)


        rowmeandf=pd.concat(rowmeanlist,axis=1)  #########if necessary can save in future

        return rowmeandf







def main():
    imputedfile=sys.argv[1]
    metoutfile = sys.argv[2]
    phenfile = sys.argv[3]

    outname = sys.argv[4]

    acm = AllCompartmentMean(imputedfile,metoutfile,phenfile,outname)

if __name__ == '__main__':
    main()