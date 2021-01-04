import sys
import pandas as pd

class Forvisual:
    def __init__(self, naReport, outname, **kwargs):
        self.report=pd.read_csv(naReport,sep="\t")
        self.outname=outname
        self.coreAlgo()

    def coreAlgo(self):
        diffcount=list(set(self.report['count'].to_list()))


        outlist=[]
        for elem in diffcount:
            tempsize=(self.report[self.report['count']==elem]).shape[0]

            tempdict={"sample_count":elem,"pos_count":tempsize}

            outlist.append(tempdict)


        outdf=pd.DataFrame(outlist)

        outdf.to_csv(self.outname,sep="\t",index=False)












def main():
    infile = sys.argv[1]
    outname = sys.argv[2]

    fv = Forvisual(infile, outname)

if __name__ == '__main__':
    main()
