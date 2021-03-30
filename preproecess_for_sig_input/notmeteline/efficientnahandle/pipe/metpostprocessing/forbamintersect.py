#### pending : negative not handled+ better name

import pandas as pd

import sys
import pandas as pd
import glob
import os
class CombinePos:
    def __init__(self,infolder,forbamDMRno,forbamoffset,outfolder):
        self.infolder=infolder
        self.forbamDMRno=forbamDMRno
        self.forbamoffset=forbamoffset
        self.outfolder=outfolder
        self.coreAlgo()

    def coreAlgo(self):
        allfiles=glob.glob(self.infolder+"/*g1*")



        alldmr,alldmrbam=self.combine(allfiles)


        sanityname=self.infolder+"_top_"+str(self.forbamDMRno)+"_sanity.txt"
        bamname = self.infolder + "_top_" + str(self.forbamDMRno) +"_bam.txt"

        alldmr.to_csv(sanityname,sep="\t",index=False)
        alldmrbam.to_csv(bamname,sep="\t",index=False,header=False)


    def combine(self,folder):
        li = []



        for filename in folder:
            if os.stat(filename).st_size == 0:
                continue
            df = (pd.read_csv(filename, sep="\t")).head(n=self.forbamDMRno)

            li.append(df)

        frame = pd.concat(li, axis=0, ignore_index=True)

        outdf=frame[['chrom','start','end']]

        

        outdfbam=outdf.copy()

        outdfbam['start']=outdfbam['start']-self.forbamoffset
        outdfbam['end']=outdfbam['end']+self.forbamoffset

        #####outdfbam[outdfbam<0]=0      ###########did not handle here. probably in future

        return outdf,outdfbam







def main():
    infolder = sys.argv[1] #final sorted
    forbamnumofDMR=int(sys.argv[2])
    forbamoffset=int(sys.argv[3])
    outfolder=sys.argv[4]
    cp=CombinePos(infolder,forbamnumofDMR,forbamoffset,outfolder)

if __name__ == '__main__':
    main()
