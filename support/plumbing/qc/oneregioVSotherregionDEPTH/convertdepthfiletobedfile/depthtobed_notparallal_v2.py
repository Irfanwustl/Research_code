
import pandas as pd
import glob
import sys
import concurrent.futures
import os.path



class Depthtobed:

    def __init__(self,fullinfodepthfolder,outfolder):

        self.depthfolder=fullinfodepthfolder
        self.outfolder=outfolder
        self.setuprun()

    def setuprun(self):


        #with concurrent.futures.ProcessPoolExecutor() as executor:
        
        coreAlgo(self.depthfolder, self.outfolder)






















def coreAlgo(depthfile,outname):
    depthdf=pd.read_csv(depthfile,sep="\t",header=None)

    outdf=depthdf

    outdf[3]=outdf[1]+1


    outdf=outdf[[0,1,3,2]]

    outdf.to_csv(outname,sep="\t",index=False,header=False)













def main():

    infodepthfolder = sys.argv[1]  ###file
    outfolder=sys.argv[2]  ###file
    dtb=Depthtobed(infodepthfolder,outfolder)


if __name__ == '__main__':
    main()