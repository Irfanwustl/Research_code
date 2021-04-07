import pandas as pd
import matplotlib.pyplot as plt
import sys
import matplotlib.backends.backend_pdf

class Plottter:

    def __init__(self, metoutile,outname,**kwargs):
        self.metout=metoutile
        self.metoutdf=pd.read_csv(self.metout,sep="\t")
        self.outname=outname

        self.corealgo()




    def corealgo(self):
        self.storealldfspecificinfo()



        fig1=self.plot_delta_vs_numdmrofDMR()

        fig2=self.plot_delta_vs_numdmrofCpG()
        fig3=self.plot_DMRlengthCpG()
        fig4=self.plot_DMRlengthBP()


        pdf = matplotlib.backends.backend_pdf.PdfPages(self.outname+".pdf")

        pdf.savefig(fig1)
        pdf.savefig(fig2)
        pdf.savefig(fig3)
        pdf.savefig(fig4)
        pdf.close()







    def storealldfspecificinfo(self):
        #######plot_delta_vs_numdmr#######
        self.delta = self.metoutdf.iloc[:, 4]
        self.absdelta = self.delta.abs()
        self.lenabsdelta = len(self.absdelta)

        self.numofDMR_array = list(range(1, self.lenabsdelta + 1))


        #######plot_delta_vs_numCpG#######
        self.windowesCpGSum=self.metoutdf.iloc[:, 5].rolling(self.lenabsdelta,min_periods=1).sum()
        #print(self.windowesCpGSum)

        ####### plot_delta_vs_DMR length(CpG) #######
        self.DMRlengthCpG=self.metoutdf.iloc[:, 5]
        self.DMRlengthbp=self.metoutdf.iloc[:, 2]-self.metoutdf.iloc[:, 1]






    def plot_DMRlengthCpG(self):
        return self.coreBarplot(self.numofDMR_array,self.DMRlengthCpG,"Decreasing delta", "DMR length (CpG)","DMR length (CpG)")

    def plot_DMRlengthBP(self):
        return self.coreBarplot(self.numofDMR_array,self.DMRlengthbp,"Decreasing delta", "DMR length (bp)", "DMR length (bp)")


    def plot_delta_vs_numdmrofDMR(self):


        return self.coreScatterplot(self.numofDMR_array, self.absdelta, "#DMR", "delta","delta vs #DMR")


    def plot_delta_vs_numdmrofCpG(self):


       return  self.coreScatterplot(self.windowesCpGSum, self.absdelta, "#CpG", "delta","delta vs #CpG")






    def coreScatterplot(self,x,y,xlabel,ylabel,title,**kwargs):
        fig = plt.figure()

        plt.scatter(x,y)


        

        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        return fig


    def coreBarplot(self,x,y,xlabel,ylabel,title,**kwargs):
        fig = plt.figure()

        plt.bar(x,y)

        plt.title(title)
        plt.tick_params(bottom=False,labelbottom=False)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        return fig

















def main():
    metoutwithheader = sys.argv[1]
    outname=sys.argv[2]



    pt=Plottter(metoutwithheader,outname)


if __name__ == '__main__':
    main()