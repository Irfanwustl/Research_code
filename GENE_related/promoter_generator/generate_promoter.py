import pandas as pd
import sys


class GeneratePromoter:
    def __init__(self, ucscfile, upstream, outname, **kwargs):
        self.ucscfile=pd.read_csv(ucscfile,sep="\t")
        self.upstream=upstream
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

        posout=posstrand[['chrom','addedupstream',self.start,self.gene]]

        posout=posout.rename(columns={'addedupstream':'start',self.start:'end'})

        negout=negstrand[['chrom',self.end,'addedupstream',self.gene]]
        negout=negout.rename(columns={self.end:'start','addedupstream': 'end'})



        outdf=pd.concat([posout,negout])

        outdf=outdf.drop_duplicates()

        outdf.to_csv(self.outname,sep="\t",index=False,header=False)










def main():
    ucscfile= sys.argv[1]
    upstream = int(sys.argv[2])

    outname = sys.argv[3]

    gp=GeneratePromoter(ucscfile,upstream,outname)

if __name__ == '__main__':
    main()