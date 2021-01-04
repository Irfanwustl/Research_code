import sys
import pandas as pd



class ConsiderfoorSM:
    def __init__(self, nonaReport,rate,outname, **kwargs):
        self.indf=pd.read_csv(nonaReport,sep="\t",index_col=0)
        self.rate=rate ### 0 to 1
        self.outname=outname

        self.coreAlgo()

    def coreAlgo(self):


        copieddf=self.indf.copy()

        copieddf['samplelist']= copieddf.samplelist.apply(lambda x: x[1:-1].split(','))

        allsamples=(copieddf['samplelist']).to_list()

        allsamples = [item for sublist in allsamples for item in sublist]


        allsamples = list(map(eval, allsamples))


        uniquesample=list(set(allsamples))



        uniquesamplelen=len(uniquesample)


        rslt_df = copieddf[copieddf['count'] >= uniquesamplelen*self.rate*1.0]

        rslt_df.to_csv(self.outname,sep="\t")







def main():
    infile = sys.argv[1]
    rate=float(sys.argv[2])
    outname = sys.argv[3]

    csm = ConsiderfoorSM(infile,rate,outname)

if __name__ == '__main__':
    main()

