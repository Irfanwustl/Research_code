
import pandas as pd
import re
import sys
import glob
import os
import os.path

class CollectCpG:

    def __init__(self,DMRwithCpGfolder,outfolder,**kwargs):

        self.DMRwithCpG=DMRwithCpGfolder
       
        self.outfolder=outfolder

        self.coreAlgo()



    def coreAlgo(self):
        allfiles = glob.glob(self.DMRwithCpG + "/*g1*")
        self.combine(allfiles)

    def parseFileName(self,filename):
        m = re.search('g1_(.+)?_\d+_g2', filename)

        if m:
            found = m.group(1)
            return found

        else:
            print("wrong file name type")

    def combine(self, folder):
        

        for filename in folder:
            if os.stat(filename).st_size == 0:
                continue
            df = (pd.read_csv(filename, sep="\t", header=None))

            df['celltype'] = "[" + self.parseFileName(filename) + "]"  #########################for read counting######

            df1 = df



            finaltmpdf = df1
            finaltmpdf.drop_duplicates(inplace=True)

            

            frame = finaltmpdf
            frame.rename(columns={0: "DMRchr", 1: "DMRstart", 2: "DMRend", 3: "q", 4: "diff", 12: "chrom", 13: "start", 14: "end"},inplace=True)

            outdf = frame[["DMRchr", "DMRstart", "DMRend", "q", "diff", "chrom", "start", "end", 'celltype']]

            outdfref = outdf[["chrom", "start", "end", 'celltype']]

            outdfrefuniq=outdfref.drop_duplicates(subset=['chrom', 'start','end'], keep=False)

            outdf.to_csv(self.outfolder + "/" + os.path.basename(filename) + "_record.txt", sep="\t", index=False)

            outdfref.to_csv(self.outfolder + "/" + os.path.basename(filename) + "_assignedref.txt", sep="\t",index=False)

            outdfrefuniq.to_csv(self.outfolder + "/" + os.path.basename(filename) + "_assignedref_uniq.txt", sep="\t",index=False)


def main():
    infolder = sys.argv[1] #DMRwithCpG

    outfolder=sys.argv[2]
    cc=CollectCpG(infolder,outfolder)

if __name__ == '__main__':
    main()






