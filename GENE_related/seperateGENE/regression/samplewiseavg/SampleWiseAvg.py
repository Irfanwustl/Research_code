import sys
import pandas as pd
import os

class PerSampleAvg:
    def __init__(self,pergeneFile,outname,**kwargs):
        self.pergenefile=pd.read_csv(pergeneFile,sep="\t", index_col=0)
        self.outname=outname

        self.gene=os.path.splitext(os.path.basename(pergeneFile))[0]

        self.coreAlgo()


    def coreAlgo(self):
        ax=0
        samplavg=self.pergenefile.mean(axis=ax)
        samplmedian=self.pergenefile.median(axis=ax)




        samplavgdf=pd.DataFrame({'Mixture':samplavg.index, self.gene+"_mean":samplavg.values})
        samplmediandf=pd.DataFrame({'Mixture':samplmedian.index, self.gene+"_median":samplmedian.values})

        samplavgdf.to_csv(self.outname+"_mean.txt",sep="\t",index=False)
        samplmediandf.to_csv(self.outname+"_median.txt",sep="\t",index=False)















def main():
    inciberinfile = sys.argv[1]
    outname = sys.argv[2]

    psa=PerSampleAvg(inciberinfile,outname)



if __name__ == '__main__':
    main()