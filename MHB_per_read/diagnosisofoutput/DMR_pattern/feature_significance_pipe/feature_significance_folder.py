#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import feature_significance_file
import sys
import glob

infol = sys.argv[1] #"/Users/irffanalahi/Research/Research_update/in-silico/background_pattern/readnumber_1000000/mincpg3/somefinalfiles"


outfol=infol+"_feature_significance"

SMrecordfile=sys.argv[2]   #"/Users/irffanalahi/Research/Research_update/in-silico/background_pattern/readnumber_1000000/mincpg3/BL14_atleast.2_top-1_singleCpG_final_record.txt"

celltype='mNeu'


infiles = glob.glob(infol+"/*txt")

os.mkdir(outfol)


# In[2]:


cpgwiseSignificancelist=[]
DMRwiseSignificancelist=[]

for infile in infiles:
    filewiseoutpath=outfol+"/"+os.path.basename(infile)
  
    cpgwiseSignificance,DMRwiseSignificance = feature_significance_file.featureSignificance(infile,celltype,SMrecordfile,filewiseoutpath)
    cpgwiseSignificancelist.append(cpgwiseSignificance)
    DMRwiseSignificancelist.append(DMRwiseSignificance)


# In[3]:


cpgwiseSignificancelistDF=pd.concat(cpgwiseSignificancelist)
cpgwiseSignificancelistDF.to_csv(outfol+"_Allfile_CpGwise.txt",sep="\t", index=False)
cpgwiseSignificancelistDF.head()


# In[4]:


cpgwisegroup=cpgwiseSignificancelistDF.groupby(['chrom','start','end'])
cpgwisegroupList=[]
for name, group in cpgwisegroup:
    group_subset=(group[['#TP_fragment','#FP_fragment','#TN_fragment','#FN_fragment','#Total_Fragment','TPR','FPR','FDR']]).mean(axis=0)
    group_subset['chrom']=(group['chrom'].tolist())[0]
    group_subset['start']=(group['start'].tolist())[0]
    group_subset['end']=(group['end'].tolist())[0]    
    
    group_subset=group_subset[['chrom','start','end','#TP_fragment','#FP_fragment','#TN_fragment','#FN_fragment','#Total_Fragment','TPR','FPR','FDR']]
    
    cpgwisegroupList.append(group_subset)
    
cpgwisegroupListDF=pd.DataFrame(cpgwisegroupList)

cpgwisegroupListDF.to_csv(outfol+"_Allfile_CpGwise_avg.txt",sep="\t", index=False)
cpgwisegroupListDF.head()


# In[5]:


DMRwiseSignificancelistDF=pd.concat(DMRwiseSignificancelist)

DMRwiseSignificancelistDF.to_csv(outfol+"_Allfile_DMRwise.txt",sep="\t", index=False)
DMRwiseSignificancelistDF.head()


# In[6]:


DMRwisegroup=DMRwiseSignificancelistDF.groupby(['DMRchr','DMRstart','DMRend'])
DMRwisegroupList=[]
for name, group in DMRwisegroup:
    group_subset=(group[['#TP_fragment','#FP_fragment','#TN_fragment','#FN_fragment','#Total_Fragment','TPR','FPR','FDR']]).mean(axis=0)
    group_subset['fileName']=group['fileName'].tolist()[0]

    group_subset['DMRchr']=(group['DMRchr'].tolist())[0]
    group_subset['DMRstart']=(group['DMRstart'].tolist())[0]
    group_subset['DMRend']=(group['DMRend'].tolist())[0]


    group_subset=group_subset[['DMRchr','DMRstart','DMRend','#TP_fragment','#FP_fragment','#TN_fragment','#FN_fragment','#Total_Fragment','TPR','FPR','FDR']]


    DMRwisegroupList.append(group_subset)


DMRwisegroupListDF=pd.DataFrame(DMRwisegroupList)

DMRwisegroupListDF.to_csv(outfol+"_Allfile_DMRwise_avg.txt",sep="\t", index=False)

