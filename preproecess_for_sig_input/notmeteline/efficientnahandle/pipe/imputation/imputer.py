import pandas as pd
import sys

class Imputer:
    def __init__(self, afterNAref, pheno, outname, **kwargs):
        self.ref = pd.read_csv(afterNAref, sep="\t", index_col=0)
        self.pheno = pd.read_csv(pheno, sep="\t", header=None, index_col=0)

        self.outname = outname

        self.coreAlgo()



    def coreAlgo(self):

        outlist=[]

        for i in range(self.pheno.shape[0]):
            classes = self.pheno.iloc[i, :]


            class1 = (classes == 1).tolist()



            valuetoput=self.ref.iloc[:, class1].mean(axis=1)

            valdf=pd.DataFrame(index=self.ref.index, columns=self.ref.columns[class1])
            #print(valdf)

            #print(valuetoput)

            valdf.loc[:]=pd.concat([valuetoput]*valdf.columns.size, axis=1)    #####################################################
            #print(valdf)

            temp=self.ref.iloc[:, class1].fillna(valdf)

            outlist.append(temp)

        outdf=pd.concat(outlist,axis=1)

        outdf=outdf[self.ref.columns]
        outdf.to_csv(self.outname,sep="\t")








def main():
    reffile = sys.argv[1]
    phenfile = sys.argv[2]

    outname = sys.argv[3]

    im = Imputer(reffile, phenfile, outname)

if __name__ == '__main__':
    main()