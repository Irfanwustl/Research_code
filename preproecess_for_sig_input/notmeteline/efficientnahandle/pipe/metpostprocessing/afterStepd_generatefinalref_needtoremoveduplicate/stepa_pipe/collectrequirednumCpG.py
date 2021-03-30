import pandas as pd
import re
import sys
import glob
import os
import os.path

class CollectCpG:

    def __init__(self,DMRwithCpGfolder,targetnumcpg,outfolder,**kwargs):

        self.DMRwithCpG=DMRwithCpGfolder
        self.numCpG=targetnumcpg
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
        li = []

        for filename in folder:
            if os.stat(filename).st_size == 0:
                continue
            df = (pd.read_csv(filename, sep="\t",header=None))

            df['celltype']="["+self.parseFileName(filename)+"]"    #########################for read counting######

            df1=df.head(n=self.numCpG)

            lastrow=df1.tail(n=1)
            dmrchr=lastrow.iloc[0][0]
            dmrstart=lastrow.iloc[0][1]
            dmrend=lastrow.iloc[0][2]





            df2=df[(df[0]==dmrchr) & (df[1]==dmrstart) & (df[2]==dmrend)]


            finaltmpdf=pd.concat([df1,df2], axis=0, ignore_index=True)
            finaltmpdf.drop_duplicates(inplace=True)




            li.append(finaltmpdf)

        frame = pd.concat(li, axis=0, ignore_index=True)
        frame.rename(columns={0: "DMRchr", 1: "DMRstart",2:"DMRend",3:"q",4:"diff",16:"chrom",17:"start",18:"end"},inplace=True)



        outdf=frame[["DMRchr",  "DMRstart","DMRend","q","diff","chrom","start","end",'celltype']]

        outdfref =outdf[["chrom","start","end",'celltype']]



        outdf.to_csv(self.outfolder+"/"+os.path.basename(self.outfolder)+"_record.txt",sep="\t",index=False )

        outdfref.to_csv(self.outfolder+"/"+os.path.basename(self.outfolder)+"_assignedref.txt",sep="\t",index=False )



















def main():
    infolder = sys.argv[1] #DMRwithCpG
    targetednumCpG=int(sys.argv[2])
    outfolder=sys.argv[3]
    cc=CollectCpG(infolder,targetednumCpG,outfolder)

if __name__ == '__main__':
    main()









