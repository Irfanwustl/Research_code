import pandas as pd
import matplotlib.pyplot as plt
import sys
import matplotlib.backends.backend_pdf
import numpy as np

class Plottter:

    def __init__(self, metoutile,deltacol,outname,**kwargs):
        self.metout=metoutile
        self.metoutdf=pd.read_csv(self.metout,sep="\t")
        self.outname=outname

        self.deltcol=deltacol

       

        #self.corealgo()




    def corealgo(self):
       
        self.storealldfspecificinfo()


        '''
        fig1=self.plot_delta_vs_numdmrofDMR()

        fig2=self.plot_delta_vs_numdmrofCpG()
        fig3=self.plot_DMRlengthCpG()
        fig4=self.plot_DMRlengthBP()
        '''
        fig5=self.plot_logq_vs_delta()
        fig6=self.plot_logq_vs_delta_nolim()
        fig7=self.plot_logq_vs_deltadiff()
        fig8=self.plot_logq_vs_deltadiffnolim()



        pdf = matplotlib.backends.backend_pdf.PdfPages(self.outname+"_"+self.deltcol+".pdf")

        '''
        pdf.savefig(fig1)
        pdf.savefig(fig2)
        pdf.savefig(fig3)
        pdf.savefig(fig4)
        '''
        pdf.savefig(fig5)
        pdf.savefig(fig6)
        pdf.savefig(fig7)
        pdf.savefig(fig8)
        pdf.close()







    def storealldfspecificinfo(self):
        if self.deltcol in self.metoutdf.columns:
            self.deltcol=self.deltcol
            self.deltcol2="diff"  ###it must be present
            self.delta2 = self.metoutdf[self.deltcol2]
        elif "diff" in self.metoutdf.columns:
            self.deltcol="diff"
        else:
            print("wrong column")
            print(self.metout)
            print("exiting")
            sys.exit(1)



        #######plot_delta_vs_numdmr#######
        self.delta = self.metoutdf[self.deltcol]
        
        self.qval = self.metoutdf.iloc[:, 3]
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


        return self.coreScatterplot(self.numofDMR_array, self.absdelta, "#DMR", "delta","delta vs #DMR",qvalue=self.qval)



    def plot_logq_vs_delta(self):


        nplog=-np.log10(self.qval)


        return  self.coreScatterplot(self.delta, nplog, "delta", "-log10(q)","qval vs compamentwise delta",xlim=[-1,1])

    def plot_logq_vs_deltadiff(self):


        nplog=-np.log10(self.qval)


        return  self.coreScatterplot(self.delta2, nplog, "delta", "-log10(q)","qval vs global delta",xlim=[-1,1])

    def plot_logq_vs_deltadiffnolim(self):


        nplog=-np.log10(self.qval)


        return  self.coreScatterplot(self.delta2, nplog, "delta", "-log10(q)","qval vs global delta")


    def plot_logq_vs_delta_nolim(self):

        nplog=-np.log10(self.qval)


        return  self.coreScatterplot(self.delta, nplog, "delta", "-log10(q)","qval vs compamentwise delta")



    def plot_delta_vs_numdmrofCpG(self):


       return  self.coreScatterplot(self.windowesCpGSum, self.absdelta, "#CpG", "delta","delta vs #CpG")






    def coreScatterplot(self,x,y,xlabel,ylabel,title,**kwargs):
        fig = plt.figure()


        if 'qvalue' in kwargs:
            plt.scatter(x, y,c=kwargs['qvalue'],cmap='viridis')
            plt.colorbar(label="qvalue")

        elif 'xlim' in kwargs:
            plt.scatter(x, y)
            plt.xlim(kwargs['xlim'])

        else:
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
    deltacol=sys.argv[2]
    outname=sys.argv[3]



    pt=Plottter(metoutwithheader,deltacol,outname)


if __name__ == '__main__':
    main()