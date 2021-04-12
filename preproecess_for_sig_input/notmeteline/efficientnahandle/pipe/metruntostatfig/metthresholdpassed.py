import pandas as pd
import sys

class ThresholdPass:
    def __init__(self, metout, qcut, diffcut, outname, **kwargs):
        self.metdf=pd.read_csv(metout,sep="\t",header=None)
        self.qcut=qcut
        self.diffcut=diffcut
        self.outname=outname

        self.qcol=3
        self.diffcol=4

        self.coreAlgo()

    def coreAlgo(self):


        hyperdf=self.metdf.loc[(self.metdf[self.qcol]<=self.qcut) & (self.metdf[self.diffcol]>=self.diffcut)]

        hypodf=self.metdf.loc[(self.metdf[self.qcol]<=self.qcut) & (self.metdf[self.diffcol]<=-self.diffcut)]

        hyperdf.to_csv(self.outname+"_hyper.txt",sep="\t",index=False,header=None)

        hypodf.to_csv(self.outname + "_hypo.txt", sep="\t", index=False, header=None)








def main():
    metout = sys.argv[1]
    qcut = float(sys.argv[2])

    diffcut = float(sys.argv[3])

    outname=sys.argv[4]

    tp = ThresholdPass(metout,qcut,diffcut,outname)

if __name__ == '__main__':
    main()

