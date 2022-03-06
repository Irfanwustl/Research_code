#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys
import glob
import os
import sys
filelits=sys.argv[1] #'/Users/irffanalahi/Research/Research_update/SoftRD/hashtable_stats/tieredApproach/OwnGrouptest/try1/someTcell/n4n8/n4n8thresholder_linecount/n8_thresholdpos_allthresholdcombinations.txt_fianlselection.txt'
locationofrefs=sys.argv[2] #'/Users/irffanalahi/Research/Research_update/SoftRD/hashtable_stats/tieredApproach/OwnGrouptest/try1/someTcell/n4n8/n4n8thresholder_linecount/testsmselect'
outdir=locationofrefs+"_bestref"

total_compartments=['chrom','start','NaiveCD4-others','NaiveCD8-others','nB-others','NK-others','PC-others','Mono-others','M0-others','M1-others','M2-others','iDC-others','mDC-others','PMN-others','cm8-others','em8-others','Eo-others','Tregs-others','em4-others','ed8-others','Mg-others','cm4-others','Er-others','mB-others']
os.mkdir(outdir)
filelistdf=pd.read_csv(filelits,sep='\t')
filelistdf.head()


# In[2]:


def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))


# In[3]:


allfiles=listdir_nohidden(locationofrefs)


# In[4]:


total_compartments_set=set(total_compartments)
for index, row in filelistdf.iterrows():
    currentfile=locationofrefs+'/'+row['Filename']
    tdf=pd.read_csv(currentfile,sep='\t',header=None)
    tdf.rename(columns={0:'chrom',1:'start',2:'end'},inplace=True)
    
    
    tdfsmpos=tdf[['chrom','start','end']]
    
    
    tdf[row['Cell Type']+'-others']=-1*row['Average Value']
    
    tdf=tdf[['chrom','start',row['Cell Type']+'-others']]
    
    tdfcolumns=set(tdf.columns.tolist())






    missingcols=total_compartments_set-tdfcolumns
    missingcolslist=list(missingcols)
    for micol in missingcolslist:
        tdf[micol]=0.9
    
    
    tdf=tdf[total_compartments]
    outname=outdir+"/"+row['SM']
    

 
    tdf.to_csv(outname,sep='\t',index=False)
    tdfsmpos.to_csv(outname+'pos',sep='\t',index=False,header=False)
    
    
    

