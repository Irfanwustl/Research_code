import pandas as pd
import sys

class cutoff:
    def __init__(self, metout, qcut,outname, **kwargs):
        self.metdf=pd.read_csv(metout,sep="\t",header=None)
        self.qcut=qcut
        self.qcol=3
        self.outname=outname
        self.coreAlgo()




    def coreAlgo(self):


        outdf=self.metdf.loc[self.metdf[self.qcol]<=self.qcut]
        outdf.to_csv(self.outname,sep="\t",index=False,header=None)


def main():
    metout = sys.argv[1] #metout ot metoutaddedcol. Have to be with header

    qcut = float(sys.argv[2])  ###signed

    outname = sys.argv[3]

    co = cutoff(metout,qcut,outname)


if __name__ == '__main__':
    main()


