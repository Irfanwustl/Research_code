####### percentile plot only works for hypo

import pandas as pd
import matplotlib.pyplot as plt
import sys
import matplotlib.backends.backend_pdf
import numpy as np
import seaborn as sns

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
        logqvsdeltafiglist=self.all_plot_logqvsdelta()
        logqvsdeltafiglistpercentile = self.all_plot_logqvsdelta(percentile_plot=True)

        logqvsdeltaSIZEfiglist = self.all_plot_logqvsdelta(size=self.numCpG,percentile_plot=True)

        logqvsdeltabpSIZEfiglist=self.all_plot_logqvsdelta(size=self.bplength,percentile_plot=True)

        #logqvsdeltacpgper300bp=self.all_plot_logqvsdelta(size=self.cpgper300bp)

        figlist=logqvsdeltafiglist+logqvsdeltafiglistpercentile + logqvsdeltaSIZEfiglist+logqvsdeltabpSIZEfiglist  #+logqvsdeltacpgper300bp



        pdf = matplotlib.backends.backend_pdf.PdfPages(self.outname+"_"+self.deltcol+".pdf")

        '''
        pdf.savefig(fig1)
        pdf.savefig(fig2)
        pdf.savefig(fig3)
        pdf.savefig(fig4)
        '''
        for fig in figlist:
            pdf.savefig(fig)
        pdf.close()







    def storealldfspecificinfo(self):
        self.isdelta2 =False
        if self.deltcol in self.metoutdf.columns:

            self.deltcol2=self.deltcol
            self.delta2 = self.metoutdf[self.deltcol2]
            self.isdelta2=True


        self.deltcol="diff"
        self.delta = self.metoutdf[self.deltcol]

        self.numCpG=self.metoutdf.iloc[:, 5]


        self.metoutdf['bp_length']=self.metoutdf.iloc[:, 2]-self.metoutdf.iloc[:, 1]
        self.bplength =self.metoutdf['bp_length']

        self.metoutdf['cpg_per300bp'] = self.numCpG*1.0*300/self.bplength
        self.cpgper300bp=self.metoutdf['cpg_per300bp']



        #######plot_delta_vs_numdmr#######

        
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




    def all_plot_logqvsdelta(self,size=None,percentile_plot=False):
        nplog = -np.log10(self.qval)
        figlist=[]

        figlist.append(self.plot_logq_vs_delta(self.delta, nplog, "global delta", "-log10(q)",
                                               "qval vs global delta", True,size=size,percentile_plot=percentile_plot))
        figlist.append(self.plot_logq_vs_delta(self.delta, nplog, "global delta", "-log10(q)",
                                               "qval vs global delta", False,size=size,percentile_plot=percentile_plot))

        if self.isdelta2==True:
            figlist.append(self.plot_logq_vs_delta(self.delta2,nplog,"compartmentwise delta", "-log10(q)","qval vs compartmentwise delta",True,size=size,percentile_plot=percentile_plot))
            figlist.append(self.plot_logq_vs_delta(self.delta2, nplog, "compartmentwise delta", "-log10(q)","qval vs compartmentwise delta", False,size=size,percentile_plot=percentile_plot))

        return figlist




    def plot_logq_vs_delta(self,x,y,xlabel,ylabel,title,islim,size=None,percentile_plot=False):


        nplog=-np.log10(self.qval)


        if islim==True:
            return self.coreScatterplot(self.delta, nplog, xlabel, ylabel, title,size=size,percentile_plot=percentile_plot,xlim=[-1, 1])
        else:
            return self.coreScatterplot(self.delta, nplog, xlabel, ylabel, title,size=size,percentile_plot=percentile_plot)


    def core_percentile(self,a,perc):
        return np.percentile(a,perc)







    def plot_delta_vs_numdmrofCpG(self):


       return  self.coreScatterplot(self.windowesCpGSum, self.absdelta, "#CpG", "delta","delta vs #CpG")






    def coreScatterplot(self,x,y,xlabel,ylabel,title,size=None,percentile_plot=False,**kwargs):
        fig = plt.figure()


        if 'qvalue' in kwargs:
            '''
            plt.scatter(x, y,c=kwargs['qvalue'],cmap='viridis')
            plt.colorbar(label="qvalue")
            '''
            print("need to test/implement again. Exiting")
            sys.exit(1)

        elif 'xlim' in kwargs:
            sns.scatterplot(x, y,edgecolor='none',size=size)
            plt.xlim(kwargs['xlim'])

        else:
            sns.scatterplot(x, y,edgecolor='none',size=size)

        if percentile_plot==True: ####### only works for hypo

            xpos=np.abs(x)
            x75=self.core_percentile(xpos,75)
            x95=self.core_percentile(xpos,95)
            x99 = self.core_percentile(xpos, 99)
            y75=self.core_percentile(y,75)
            y95=self.core_percentile(y,95)
            y99 = self.core_percentile(y, 99)


            #print(x75,x95,x99,y75,y95,y99)  #### need to show on text

            plt.axvline(-x99, color='r', ls='--', label="99 percentile")
            plt.axvline(-x95, color='g', ls='--', label="95 percentile")
            plt.axvline(-x75,color='b',ls='--',label="75 percentile")

            plt.axhline(y99, color='r', ls='--')
            plt.axhline(y95, color='g', ls='--')
            plt.axhline(y75,color='b',ls='--')





            plt.legend()







        

        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.close()

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