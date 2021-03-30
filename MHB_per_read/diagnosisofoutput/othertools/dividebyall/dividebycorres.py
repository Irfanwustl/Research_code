import pandas as pd
import sys


class Dividebycorress:
    def __init__(self, combinedmergedwithSM,dividerfile, outname, **kwargs):
        self.givenfile=pd.read_csv(combinedmergedwithSM,sep="\t",index_col=0)

        self.divider=pd.read_csv(dividerfile,sep='\t')


        self.outname=outname


        self.coreAlgo()



    def coreAlgo(self):


        for index, row in self.divider.iterrows():


            colnames=row.index.tolist()


            mix=row[0]

            celltypeindex=1

            while celltypeindex < len(colnames):
                celltype=colnames[celltypeindex]
                celltype_value=row[celltypeindex]
                if celltype_value==0:
                    celltype_value=0.0000000000000001


                self.givenfile.loc[self.givenfile['celltype'] == "[" + celltype + "]", mix]=self.givenfile.loc[self.givenfile['celltype']=="["+celltype+"]",mix]/celltype_value






                celltypeindex=celltypeindex+1


            self.givenfile.to_csv(self.outname,sep="\t")











def main():
    combinedmergedwithSM = sys.argv[1] 

    dividerfile=sys.argv[2]

    outname=sys.argv[3]

    dcorr=Dividebycorress(combinedmergedwithSM,dividerfile,outname)

if __name__ == '__main__':
    main()