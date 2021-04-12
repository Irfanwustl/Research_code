import pandas as pd
import sys
import concurrent.futures
import compartmentmean_parallal
import glob
import os.path












class driverCompartmentmean:
    def __init__(self, metoutfolder, phenofile, imputedfileorrowmean,isrowmean,outname, **kwargs):

        self.indir=metoutfolder

        self.pheno=pd.read_csv(phenofile, sep="\t", header=None, index_col=0)

        self.outdir=outname


        if isrowmean == 0:
            self.imputedfile=pd.read_csv(imputedfileorrowmean,sep="\t",index_col=0)
            self.rowmeandf=self.rowmean()

            self.rowmeandf = self.rowmeandf.reset_index()

            self.rowmeandf[['chrom', 'pos']] = self.rowmeandf.iloc[:, 0].str.split(":", expand=True)

            self.rowmeandf['pos'] = self.rowmeandf['pos'].astype(int)
            self.rowmeandf.to_csv(imputedfileorrowmean+"_rowmean.txt",sep="\t",index=False)

        else:
            self.rowmeandf = pd.read_csv(imputedfileorrowmean,sep="\t")

        self.runallfilesparallal()





    def rowmean(self):
        rowmeanlist = []

        for i in range(self.pheno.shape[0]):
            classes = self.pheno.iloc[i, :]
            class1 = (classes == 1).tolist()
            class1_mean = self.imputedfile.iloc[:, class1].mean(axis=1)

            temdf =class1_mean.to_frame(self.pheno.index[i])



            rowmeanlist.append(temdf)


        rowmeandf=pd.concat(rowmeanlist,axis=1)  #########if necessary can save in future


        print("row mean done")

        return rowmeandf

    def runallfilesparallal(self):
        objlist = []
        for file in glob.glob(self.indir+"/*.txt"):
            tempobj=compartmentmean_parallal.AllCompartmentMean(self.rowmeandf,file,self.pheno,self.outdir+"/"+os.path.basename(file))
            objlist.append(tempobj)

        with concurrent.futures.ProcessPoolExecutor() as executor:
            for obj in objlist:

                executor.submit(obj.coreAlgo())










def main():
    metoutfolder = sys.argv[1]
    phenofile = sys.argv[2]
    imputedfileorrowmean = sys.argv[3]
    isrowmean = int(sys.argv[4]) #0 need to run rowmean, 1 = this is rowmean

    outname = sys.argv[5] ###outfolder

    dc = driverCompartmentmean(metoutfolder,phenofile,imputedfileorrowmean,isrowmean,outname)

if __name__ == '__main__':
    main()