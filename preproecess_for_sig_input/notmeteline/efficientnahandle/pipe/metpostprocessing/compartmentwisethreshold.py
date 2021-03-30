import pandas as pd
import sys


class CompartmentWiseThreshold:
    def __init__(self, metoutaddedcol, diffcut, outname, **kwargs):
        self.metadded=pd.read_csv(metoutaddedcol,sep="\t")
        self.diffcut=diffcut
        self.outname=outname

        self.coreAlgo()



    def coreAlgo(self):

        allcols=(self.metadded.columns).tolist()



        celltype=allcols[8]


        allcelltypes=allcols[10:len(allcols)-1]


        allcelltypeslen=len(allcelltypes)
        allcelltypes.remove(celltype+".1")

        othercelltypeslen=len(allcelltypes)

        if allcelltypeslen!=(othercelltypeslen+1):
            print("error in cell types name probably. Exiting")
            sys.exit(1)


        self.subtractallcelltypes(celltype,allcelltypes)




    def subtractallcelltypes(self,thiscelltype,othercelltypes):
        newdf=self.metadded.copy()

        newcollist=[]
        for othercell in othercelltypes:
            tmpcol=thiscelltype+"-"+othercell
            newdf[tmpcol]=newdf[thiscelltype]-newdf[othercell]
            newcollist.append(tmpcol)



        self.buildQyery(newdf,newcollist)



    def buildQyery(self,newdf,newcollist):
        if self.diffcut>=0:
            sign='>'
        else:
            sign='<'

        query =""

        newcollistlen=len(newcollist)
        i=0
        for newcol in newcollist:
            if i==newcollistlen-1:
                query = query + newcol+sign + str(self.diffcut)
            else:
                query=query+newcol + sign+ str(self.diffcut)+ ' & '
            i=i+1





        out=newdf.query(query)

        out.to_csv(self.outname,sep="\t",index=False)







































def main():
    metoutaddedcol = sys.argv[1]



    diffcut = float(sys.argv[2])###signed

    

    outname=sys.argv[3]

    cwt=CompartmentWiseThreshold(metoutaddedcol,diffcut,outname)

if __name__ == '__main__':
    main()
