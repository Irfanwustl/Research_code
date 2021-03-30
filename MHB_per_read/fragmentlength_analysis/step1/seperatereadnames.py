import pandas as pd
import os.path
import sys

class SeperateReadnames:
    def __init__(self,finalfile,outdir,**kwargs):
        self.outprefix=os.path.basename(finalfile)
        self.finaldf=pd.read_csv(finalfile,sep="\t",index_col=0)
        self.outdir=outdir


        self.fileprefix=self.outdir+"/"+ self.outprefix
        self.coreAlgo()

    def coreAlgo(self):
        celltype=list(set(self.finaldf.loc[self.finaldf['finalacceptedfor']!='notdetermined','finalacceptedfor'].tolist()))


        for cell in celltype:
            corresreadpos=(self.finaldf.loc[self.finaldf['finalacceptedfor'] == cell].index).tolist()

            posfilename=self.fileprefix+"_celltype_"+cell+"_posread.txt"


            corresreadneg=(self.finaldf.loc[self.finaldf['finalrejectedfor'].str.contains("'"+cell+"'")].index).tolist()

            negfilename=self.fileprefix+"_celltype_"+cell+"_negread.txt"


            self.writelisttofiles(corresreadpos,posfilename)

            self.writelisttofiles(corresreadneg,negfilename)


    def writelisttofiles(self,my_list,filename):
        with open(filename, 'w') as f:
            for item in my_list:
                f.write("%s\n" % item)

















def main():
    finalfile = sys.argv[1] #final sorted
    outdir=sys.argv[2]

    sr=SeperateReadnames(finalfile,outdir)

if __name__ == '__main__':
    main()
