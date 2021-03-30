import pandas as pd
import collections
import os.path

import sys

class DetectedCpG:
    def __init__(self, rdout,outname,**kwargs):
        self.colnametoset=os.path.basename(rdout)
        self.rdout=pd.read_csv(rdout,sep="\t")
        self.rdout['acceptedCpG'] = self.rdout.acceptedCpG.apply(lambda x: x[1:-1].split(','))


        self.outname=outname
        self.coreAlgo()




    def coreAlgo(self):
        allacceptedCpG=self.rdout['acceptedCpG']

        allacceptedCpG = [x for sublist in allacceptedCpG for x in sublist]

        allacceptedCpG = list(map(eval, allacceptedCpG))


        counter = collections.Counter(allacceptedCpG)

        outdf=pd.DataFrame.from_dict(counter, orient='index')

        outdf.reset_index(inplace=True)
        outdf = outdf.rename(columns={'index': 'position',0:self.colnametoset})

        outdf.to_csv(self.outname,sep="\t",index=False)


def main():
    rdout = sys.argv[1] ### like masterdf or informative masterdf



    outname=sys.argv[2]

    of=DetectedCpG(rdout, outname)

if __name__ == '__main__':
    main()