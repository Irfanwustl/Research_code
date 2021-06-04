import pandas as pd
import sys
import concurrent.futures
import plotter

import glob
import os.path




class Driver_plotter:
    def __init__(self, metoutwithheader,deltacol,outfolder,annotfile,mode, **kwargs):
        self.metoutwithheaderdir=metoutwithheader
        self.deltacol=deltacol
        self.outtfolder=outfolder
        self.annotfile=annotfile
        self.mode=mode

        self.runallfilesparallal()


    def runallfilesparallal(self):
        objlist = []
        for file in glob.glob(self.metoutwithheaderdir + "/*.txt"):
            
            tempobj = plotter.Plottter(file,self.deltacol, self.outtfolder + "/" + os.path.basename(file),self.annotfile,self.mode)
            objlist.append(tempobj)

        with concurrent.futures.ProcessPoolExecutor() as executor:
            for obj in objlist:
                executor.submit(obj.corealgo())






def main():
    metoutwithheader = sys.argv[1] ###dir
    deltacol=sys.argv[2]
    outfolder=sys.argv[3]
    annotfile=sys.argv[4]
    mode=sys.argv[5]

   

    dp=Driver_plotter(metoutwithheader,deltacol,outfolder,annotfile,mode)


if __name__ == '__main__':
    main()