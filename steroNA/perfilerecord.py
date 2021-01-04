import pandas as pd
import sys
import numpy as np


class Recordperfile:
    def __init__(self, allmatCiberin, outfolder,outfoldernona, **kwargs):
        self.indf = pd.read_csv(allmatCiberin, sep="\t", index_col=0)

        self.outfolder = outfolder
        self.outfoldernona=outfoldernona

        self.corealgo()



    def corealgo(self):

        cols=self.indf.columns
        indices=set(self.indf.index)


        for col in cols:

            index = self.indf[col].index[self.indf[col].apply(np.isnan)]


            na_indices=set(index)
            nona_indices=indices-na_indices

            outNAname=self.outfolder+"/"+col+"_napos.txt"
            outnoNAname=self.outfoldernona+"/"+col+"_nonapos.txt"


            self.saveset(na_indices,outNAname)


            self.saveset(nona_indices,outnoNAname)


    def saveset(self,myset,myfile):

        with open(myfile, 'w') as f:
            for item in myset:
                f.write("%s\n" % item)




def main():
    infile = sys.argv[1]
    outfolder = sys.argv[2]
    outfoldernona=sys.argv[3]
    rf = Recordperfile(infile, outfolder, outfoldernona)


if __name__ == '__main__':
    main()

