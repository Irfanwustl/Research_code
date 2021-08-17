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
          

            class1df=self.ref.iloc[:,class1]
    

            class1dfcols=class1df.columns.tolist()
        

            class1dfcolslen=len(class1dfcols)
     


            class1coldict=self.renameCol(class1dfcols,"g1")
    



            class1df=class1df.rename(columns=class1coldict,errors="raise")
       
            

            for iini in range(self.pheno.shape[0]):
                if i==iini:
                    continue

                classesiini=self.pheno.iloc[iini, :]
                class2iini= (classesiini == 1).tolist()
                class2iinidf=self.ref.iloc[:,class2iini]
                class2iinidfcols=class2iinidf.columns.tolist()
                class2iinidfcolslen=len(class2iinidfcols)
                class2iinicoldict=self.renameCol(class2iinidfcols,"g2")
                class2iinidf=class2iinidf.rename(columns=class2iinicoldict,errors="raise")


            #########################################################







                combdf=pd.concat([class1df,class2iinidf],axis=1)






                combdf.reset_index(inplace=True)


                combdf[['chrom','pos']]=combdf.position.str.split(":",expand=True)
                combdf['pos']=combdf['pos'].astype(int)
                combdf['pos']=combdf['pos']+1






                outdf=combdf[['chrom', 'pos', 'g1', 'g2']]



                outdf.to_csv(self.outname+"_g1_"+self.pheno.index[i]+"_"+str(class1dfcolslen)+"_g2_"+self.pheno.index[iini]+"_"+str(class2iinidfcolslen), sep="\t",index=False)




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
    