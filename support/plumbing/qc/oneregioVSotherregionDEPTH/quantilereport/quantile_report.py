import pandas as pd
import glob
import sys
import concurrent.futures
import os.path

class QuantileReport:
    def __init__(self,infolder, outfolder,col):
        self.infolder=infolder
        self.outfolder=outfolder
        self.col=col

        self.setuprun()


    def setuprun(self):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            for name in glob.glob(self.infolder + "/*.txt"):
                executor.submit(coreAlgo, name, self.outfolder+"/"+os.path.basename(name)+"_quant.txt",self.col)


def coreAlgo(infile,outname,col):
    indf = pd.read_csv(infile, sep="\t", header=None)
    fifth=indf[col].quantile(0.05)
    med=indf[col].quantile(0.5)
    ninefive=indf[col].quantile(0.95)

    with open(outname, 'w') as the_file:
        the_file.write(str(fifth)+"\n")
        the_file.write(str(med) + "\n")
        the_file.write(str(ninefive) + "\n")





def main():

    infodepthintersectedfolder = sys.argv[1]
    outfolder=sys.argv[2]
    col=int(sys.argv[3])
    qr=QuantileReport(infodepthintersectedfolder,outfolder,col)


if __name__ == '__main__':
    main()