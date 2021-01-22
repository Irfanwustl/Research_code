import glob
import sys
import pandas as pd

class RegionDepth:
    def __init__(self, querybgfile, fullinfodepthfile, outname):
        self.qbf=pd.read_csv(querybgfile,sep="\t",header=None)
        self.depthfile=pd.read_csv(fullinfodepthfile,sep="\t",header=None)
        self.outname=outname
        self.coreAlgo()







    def coreAlgo(self):

        outdf=pd.DataFrame()
        for index, row in self.qbf.iterrows():
            chrom=row[0]
            start=row[1]
            end=row[2]

            tempdf=self.depthfile.loc[(self.depthfile[0]==chrom) & (self.depthfile[1]>=start) & (self.depthfile[1]<=end) ]

            outdf=outdf.append(tempdf,ignore_index=True)


        outdf.to_csv(self.outname,sep="\t",index=False,header=False)

















def main():
    infodepthfolder = sys.argv[1]  ###file
    qbf = sys.argv[2]  ###with chrom, start, end
    outfolder=sys.argv[3]  ###outname
    rd=RegionDepth(qbf,infodepthfolder,outfolder)


if __name__ == '__main__':
    main()