import pandas as pd
import sys
import glob
import os

class Combineall:
    def __init__(self, infolder, outname, **kwargs):
        self.infolder=infolder
        self.outname=outname
        self.coreAlgo()


    def coreAlgo(self):
        allfiles = glob.glob(self.infolder + "/*txt*")
        li = []

        for filename in allfiles:
            if os.stat(filename).st_size == 0:
                continue
            df = pd.read_csv(filename,  sep="\t",index_col=0)

            li.append(df)

        frame = pd.concat(li, axis=1)

        frame=frame.fillna(0)

        frame.index.name = 'position'



        frame.to_csv(self.outname,sep="\t")







def main():
    cpgrecordFolder = sys.argv[1] ### like masterdf or informative masterdf



    outname=sys.argv[2]

    ca=Combineall(cpgrecordFolder,outname)

if __name__ == '__main__':
    main()