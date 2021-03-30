import pandas as pd
import sys



class SortDMR:
    def __init__(self, metoutcompartementwise,metric,sortcriteria, outname, **kwargs):
        self.dfmet=pd.read_csv(metoutcompartementwise,sep="\t")
        self.metric=metric
        self.sortcriteria=sortcriteria
        self.outname=outname

        self.coreAlgo()

    def coreAlgo(self):
        allcols=self.dfmet.columns

        metricname=allcols[self.metric]

        out=self.dfmet.copy()


        if self.sortcriteria==1:
            asc=True
        elif self.sortcriteria==2:
            asc=False
        else:
            print("wrong sort criteria.Exiting=",self.sortcriteria)
            sys.exit(1)


        out=out.sort_values(metricname,ascending=asc)

        out.to_csv(self.outname+"_"+metricname+"_asc"+str(asc)+".txt",sep="\t",index=False)










def main():
    metoutcompartementwise = sys.argv[1]
    metric = int(sys.argv[2])  ##index of the metric

    sortcriteria=int(sys.argv[3]) ### asc =1, desc=2



    outname=sys.argv[4]

    sd = SortDMR(metoutcompartementwise,metric,sortcriteria,outname)

if __name__ == '__main__':
    main()