import sys
import pandas as pd
import glob
import os
class CombinePos:
    def __init__(self,infolder,outfolder):
        self.infolder=infolder
        self.outfolder=outfolder
        self.coreAlgo()

    def coreAlgo(self):
        allhypo=glob.glob(self.infolder+"/*hypo*")
        allhyper=glob.glob(self.infolder+"/*hyper*")


        allhypopos=self.combine(allhypo)
        allhyperpos=self.combine(allhyper)

        ############# save with good name #####


    def combine(self,folder):
        li = []



        for filename in folder:
            if os.stat(filename).st_size == 0:
                continue
            df = pd.read_csv(filename, header=None,sep="\t")

            li.append(df)

        frame = pd.concat(li, axis=0, ignore_index=True)

        outdf=frame[[0,1,2]]

        return outdf







def main():
    infolder = sys.argv[1]
    outfolder=sys.argv[2]
    cp=CombinePos(infolder,outfolder)

if __name__ == '__main__':
    main()
