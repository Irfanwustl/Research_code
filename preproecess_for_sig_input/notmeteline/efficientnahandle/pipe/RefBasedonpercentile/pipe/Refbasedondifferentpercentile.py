#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import sys
dmrfile=sys.argv[1] #"/Users/irffanalahi/Research/Research_update/SM/melcfdref/Allseperated/differenttil/meldifferentTIL_genebody_input_out_mincpg2_q0.05_diff0.1_hypoTIL_genomic_feature_withrepeat_header_celltypeseperated/rowcombined_relevantgenes/Dashboard/bothdelta_q/towardsSM/alldmr/promdatareadyCD8TIL_all_matrixCin_nr0.5_imputed_g1_CD8_TIL_3_g2_others_9.txt_q0.05_diff0.1_hypo.txt"
outfile=sys.argv[2] #"/Users/irffanalahi/Research/Research_update/SM/melcfdref/Allseperated/differenttil/meldifferentTIL_genebody_input_out_mincpg2_q0.05_diff0.1_hypoTIL_genomic_feature_withrepeat_header_celltypeseperated/rowcombined_relevantgenes/Dashboard/bothdelta_q/towardsSM/sampleout.txt"
diffcol=sys.argv[3]

percentillesdiff=[75,95,99]
percentillesq=[75,95,99]


qcol="q"


dmrdf=pd.read_csv(dmrfile,sep="\t")

dmrdf.head()


# In[2]:


dmrdf["diffcolpos"]=np.abs(dmrdf[diffcol])
dmrdf["neglogq"]=-np.log10(dmrdf["q"])

dmrdf.head()


# In[3]:


percentileq=[]
percentilediff=[]
for qpercen in percentillesq:
    tempQpercen=np.percentile(dmrdf["neglogq"],qpercen)
    for diffpercen in percentillesdiff:

    	tempDIFFpercen=np.percentile(dmrdf["diffcolpos"],diffpercen)
    
    	tempdf=dmrdf[(dmrdf["diffcolpos"]>=tempDIFFpercen) & (dmrdf["neglogq"]>=tempQpercen)]
    	tempdfDMRonly=tempdf[["chrom","start","end"]]
    	outname=outfile+"_q"+str(qpercen)+diffcol+str(diffpercen)+"percentile.txt"
    
    	tempdf.to_csv(outname,sep="\t",index=False)
    
    	outnameONLYdmr=outfile+"_ONLYDMR_"+"_q"+str(qpercen)+diffcol+str(diffpercen)+"percentile.txt"
    
    	tempdfDMRonly.to_csv(outnameONLYdmr,sep="\t",index=False)
    
                                                          
    
  


    

