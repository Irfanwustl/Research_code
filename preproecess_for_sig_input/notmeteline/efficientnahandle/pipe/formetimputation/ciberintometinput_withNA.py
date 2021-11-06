import pandas as pd
import sys


class CintoMetinput:
    def __init__(self, ciberin, pheno, outname, **kwargs):
        self.ref = pd.read_csv(ciberin, sep="\t", index_col=0)
        self.pheno = pd.read_csv(pheno, sep="\t", header=None, index_col=0)

        self.outname = outname

        self.coreAlgo()

    def coreAlgo(self):
        for i in range(self.pheno.shape[0]):
            classes = self.pheno.iloc[i, :]


            class1 = (classes == 1).tolist()
            class2 = (classes == 2).tolist()

            class1df=self.ref.iloc[:,class1]
            class2df=self.ref.iloc[:,class2]

            class1dfcols=class1df.columns.tolist()
            class2dfcols=class2df.columns.tolist()

            class1dfcolslen=len(class1dfcols)
            class2dfcolslen=len(class2dfcols)


            class1coldict=self.renameCol(class1dfcols,"g1")
            class2coldict=self.renameCol(class2dfcols,"g2")



            class1df=class1df.rename(columns=class1coldict,errors="raise")
            class2df=class2df.rename(columns=class2coldict,errors="raise")






            combdf=pd.concat([class1df,class2df],axis=1)






            combdf.reset_index(inplace=True)


            combdf[['chrom','pos']]=combdf.position.str.split(":",expand=True)
            combdf['pos']=combdf['pos'].astype(int)
            combdf['pos']=combdf['pos']+1






            outdf=combdf[['chrom', 'pos', 'g1', 'g2']]



            outdf.to_csv(self.outname+"_g1_"+self.pheno.index[i]+"_"+str(class1dfcolslen)+"_g2_others_"+str(class2dfcolslen), sep="\t",index=False, na_rep='NA')




    def renameCol(self,collist,newname):
        outdict={}

        for c in collist:
            outdict[c]=newname


        return outdict

def main():
    reffile = sys.argv[1]
    phenfile = sys.argv[2]

    outname = sys.argv[3]  ###outprefix

    cmi = CintoMetinput(reffile, phenfile, outname)

if __name__ == '__main__':
    main()