import pandas as pd
import sys

class Onlyinformative:
    def __init__(self, rdout,outname,**kwargs):
        self.rdout=pd.read_csv(rdout,sep="\t")


        self.outname=outname
        self.coreAlgo()


    def coreAlgo(self):

        outdf=self.rdout[(self.rdout['assignedcelltype']!="NotAssigned") & (self.rdout['assignedcelltype']!="lowmapq") & (self.rdout['assignedcelltype']!="DupRead") ]

        outdf.to_csv(self.outname,sep="\t",index=False)






def main():
    rdout = sys.argv[1] ### like masterdf



    outname=sys.argv[2]

    of=Onlyinformative(rdout,outname)

if __name__ == '__main__':
    main()