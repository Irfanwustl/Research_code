import pandas as pd
import sys


class GeneratePromoter:
    def __init__(self, ucscfile, upstream,downstream, outname, **kwargs):
        self.ucscfile=pd.read_csv(ucscfile,sep="\t")
        self.upstream=upstream
        self.downstream=downstream
        self.outname=outname

        self.strand='strand'
        self.start='txStart'
        self.end='txEnd'
        self.gene='name2'

        self.coreAlgo()


    def coreAlgo(self):
        posstrand=(self.ucscfile.loc[self.ucscfile[self.strand]=='+']).copy()
        negstrand=(self.ucscfile.loc[self.ucscfile[self.strand]=='-']).copy()

        posstrand['addedupstream']=posstrand[self.start]-self.upstream
        negstrand['addedupstream']=negstrand[self.end]+self.upstream

        posstrand['addeddownstream']=posstrand[self.end]+self.downstream
        negstrand['addeddownstream']=negstrand[self.start]-self.downstream

        posout=posstrand[['chrom','addedupstream','addeddownstream',self.gene]]

        posout=posout.rename(columns={'addedupstream':'start','addeddownstream':'end'})

        negout=negstrand[['chrom','addeddownstream','addedupstream',self.gene]]
        negout=negout.rename(columns={'addeddownstream':'start','addedupstream': 'end'})



        outdf=pd.concat([posout,negout])

        outdf=outdf.drop_duplicates()

        outdf['start'][outdf['start'] < 0] = 0

        outdf.to_csv(self.outname+"_withgenename.txt",sep="\t",index=False,header=False)

        outdf=outdf.drop(self.gene,axis=1)

        outdf.to_csv(self.outname,sep="\t",index=False,header=False)










def main():
    ucscfile= sys.argv[1]
    upstream = int(sys.argv[2])
    downstream=int(sys.argv[3])

    outname = sys.argv[4]

    gp=GeneratePromoter(ucscfile,upstream,downstream,outname)

if __name__ == '__main__':
    main()