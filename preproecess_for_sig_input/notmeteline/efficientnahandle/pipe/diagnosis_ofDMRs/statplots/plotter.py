####### percentile plot only works for hypo

import pandas as pd
import matplotlib.markers as mmarkers
import matplotlib.pyplot as plt
import sys
import matplotlib.lines as mlines
import matplotlib.backends.backend_pdf
import numpy as np
import seaborn as sns
from sklearn import preprocessing


class Plottter:

    def __init__(self, metoutile,deltacol,outname,annotfile,mode,**kwargs):
        self.metout=metoutile
        self.metoutdf=pd.read_csv(self.metout,sep="\t")
        self.outname=outname

        self.deltcol=deltacol

        self.annotationfile=pd.read_csv(annotfile,sep="\t")

        self.mode=mode
   #("/Users/irffanalahi/Research/weekly/for_4_14_21/newRefs/CD8til/metout/genomic_analysis/meltumMONOvsTCOMBINEDCD4tilexcludedgeneboby_input_out_mincpg2_q0.05_diff0.1_genomic_feature_withrepeat_header_celltypeseperated/plot/subsetofCD8genes.txt",sep="\t")

        
       

        #self.corealgo()




    def corealgo(self):

       
        self.storealldfspecificinfo()
        self.annotattionsupport()


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







    def annotattionsupport(self):


        self.annotcorresmtout=pd.merge(self.metoutdf,self.annotationfile,left_on=['chrom','start','end'],right_on=['chrom','start','end'])





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
        self.metoutdf['npqlog'] = -np.log10(self.qval)
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




    def all_plot_logqvsdelta(self,size=None,percentile_plot=False,**kwargs):
        nplog = self.metoutdf['npqlog']
        figlist=[]

        figlist.append(self.plot_logq_vs_delta(self.delta, nplog, "global delta", "-log10(q)",
                                               "qval vs global delta", True,size=size,percentile_plot=percentile_plot,annot=self.deltcol))
        figlist.append(self.plot_logq_vs_delta(self.delta, nplog, "global delta", "-log10(q)",
                                               "qval vs global delta", False,size=size,percentile_plot=percentile_plot,annot=self.deltcol))

        if self.isdelta2==True:
            figlist.append(self.plot_logq_vs_delta(self.delta2,nplog,"compartmentwise delta", "-log10(q)","qval vs compartmentwise delta",True,size=size,percentile_plot=percentile_plot,annot=self.deltcol2))
            figlist.append(self.plot_logq_vs_delta(self.delta2, nplog, "compartmentwise delta", "-log10(q)","qval vs compartmentwise delta", False,size=size,percentile_plot=percentile_plot,annot=self.deltcol2))

        return figlist




    def plot_logq_vs_delta(self,x,y,xlabel,ylabel,title,islim,size=None,percentile_plot=False,**kwargs):





        if islim==True:
            return self.coreScatterplot(x, y, xlabel, ylabel, title,size=size,percentile_plot=percentile_plot,xlim=[-1, 1],**kwargs)

        else:
            return self.coreScatterplot(x, y, xlabel, ylabel, title,size=size,percentile_plot=percentile_plot,**kwargs)


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

        if 'xlim' in kwargs:
            sns.scatterplot(x, y,edgecolor='none',size=size)
            plt.xlim(kwargs['xlim'])
           



        else:
            sns.scatterplot(x, y,edgecolor='none',size=size,color='lightgrey',marker=".")
            #plt.scatter(-0.414764, -np.log10(2.2127e-06),color="black")
            #plt.annotate("TIGIT", (-0.414764, -np.log10(2.2127e-06)))

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

        if "annot" in  kwargs:



            annotdelta=kwargs["annot"]
            if annotdelta in self.annotcorresmtout.columns:
                pass
            elif annotdelta+"_x" in self.annotcorresmtout.columns:
                annotdelta=annotdelta+"_x"
            else:

                print(annotdelta)
                print("above annotation wrong delta. Exiting")
                sys.exit(1)


            if "color" in self.annotcorresmtout.columns:
                plt.scatter(self.annotcorresmtout[annotdelta], self.annotcorresmtout['npqlog'], color=self.annotcorresmtout['color'])
            else:
                plt.scatter(self.annotcorresmtout[annotdelta], self.annotcorresmtout['npqlog'], color="black")


            if "c" in self.annotcorresmtout.columns:

                plt.scatter(self.annotcorresmtout[annotdelta], self.annotcorresmtout['npqlog'],
                            c=self.annotcorresmtout['c'] ,vmin=.5,vmax=1,marker=".")
                plt.colorbar()

            if self.mode=="allgenes" or self.mode=="Region":
                le = preprocessing.LabelEncoder()
                if self.mode=="Region":
                    le.fit(self.annotcorresmtout["Region"])
                    self.annotcorresmtout['categorical_label'] = le.transform(self.annotcorresmtout["Region"])
                else:
                    le.fit(self.annotcorresmtout['Gene/Repeat type'])
                    self.annotcorresmtout['categorical_label'] = le.transform(self.annotcorresmtout['Gene/Repeat type'])

                uniquegenesnumber=list(set(self.annotcorresmtout['categorical_label'].tolist()))
                uniquegenesname=le.inverse_transform(uniquegenesnumber)
               
                uniquegenesname=list(uniquegenesname)
            
                genecolormap = "Set3"
                if self.mode=="Region":
                    genecolormap = "Accent"
                    allgenesscatter=plt.scatter(self.annotcorresmtout[annotdelta], self.annotcorresmtout['npqlog'], c=self.annotcorresmtout['categorical_label'],cmap=genecolormap)

                else:                
                    allgenesscatter=plt.scatter(self.annotcorresmtout[annotdelta], self.annotcorresmtout['npqlog'], c=self.annotcorresmtout['categorical_label'],cmap=genecolormap,edgecolor='black')
                

                if self.mode=="Region":

                    priority_list=['repeat','cds','3/5 utrexon','promoter','intron']  #['promoter','cds','3/5 utrexon','intron','repeat']
                    priority_handlelist=[]
                    if len(priority_list)==len(uniquegenesname):
                        for pregion in priority_list:
                            priority_handlelist.append(allgenesscatter.legend_elements()[0][uniquegenesname.index(pregion)])


                        plt.legend(handles=priority_handlelist, labels=priority_list)
                    else:
                        plt.legend(handles=allgenesscatter.legend_elements()[0], labels=uniquegenesname)


                else:
                    plt.legend(handles=allgenesscatter.legend_elements()[0], labels=uniquegenesname)
               





            if self.mode=="AUC_Region":


                priority_regions=['promoter','cds','3/5 utrexon','intron','repeat','Others']
                region_marker = ["o", "s", "D", "*", "^","x"]

                #priority_regions=['repeat','promoter','3/5 utrexon','intron','cds','Others']
                #region_marker = ["^","o","D","*","s","x"]



                self.annotcorresmtout['marker']=-1

                legendhandles = []
                prcount=0
                for pr in priority_regions:
                    self.annotcorresmtout.loc[self.annotcorresmtout["Region"]==pr,'marker']=region_marker[prcount]

                    legendhandles.append(mlines.Line2D([], [],color="black", marker=region_marker[prcount],
                                                       label=pr))


                    prcount=prcount+1






                mscatter(self.annotcorresmtout[annotdelta], self.annotcorresmtout['npqlog'],m=self.annotcorresmtout['marker'].tolist(),
                            c=self.annotcorresmtout['c'] ,vmin=.5,vmax=1)





                plt.legend(handles=legendhandles)
                #plt.legend([matplotlib.markers.MarkerStyle('.'),matplotlib.markers.MarkerStyle('o'),matplotlib.markers.MarkerStyle('v'),matplotlib.markers.MarkerStyle('^'),matplotlib.markers.MarkerStyle('<'),matplotlib.markers.MarkerStyle('>')], uniqueregionname)




            if 'Gene/Repeat type' in self.annotcorresmtout.columns:

                for index, row in self.annotcorresmtout.iterrows():

                    if self.mode=="allgenes":
                        pass

                    elif "color" in self.annotcorresmtout.columns:
                        if row['color']=="black":
                            plt.annotate(row['Gene/Repeat type'], (row[annotdelta], row['npqlog']),fontsize=8)

                    elif "c" in self.annotcorresmtout.columns:
                        pass
                    else:
                        plt.annotate(row['Gene/Repeat type'], (row[annotdelta], row['npqlog']), fontsize=8)












        

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




def mscatter(x,y,ax=None, m=None, **kw):
    
    if not ax: ax=plt.gca()
    sc = ax.scatter(x,y,**kw)
    if (m is not None) and (len(m)==len(x)):
        paths = []
        for marker in m:
            if isinstance(marker, mmarkers.MarkerStyle):
                marker_obj = marker
            else:
                marker_obj = mmarkers.MarkerStyle(marker)
            path = marker_obj.get_path().transformed(
                        marker_obj.get_transform())
            paths.append(path)
        sc.set_paths(paths)
    return sc












def main():
    metoutwithheader = sys.argv[1]
    deltacol=sys.argv[2]
    outname=sys.argv[3]



    pt=Plottter(metoutwithheader,deltacol,outname)


if __name__ == '__main__':
    main()