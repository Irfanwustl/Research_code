#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys
import glob
import os
filelits=sys.argv[1] #'/Users/irffanalahi/Research/Research_update/SoftRD/hashtable_stats/tieredApproach/OwnGrouptest/try1/someTcell/someTcell_linecount/em4_thresholdpos_allthresholdcombinations.txt_finalselection.txt'
locationofrefs=sys.argv[2] #'/Users/irffanalahi/Research/Research_update/SoftRD/hashtable_stats/tieredApproach/OwnGrouptest/try1/someTcell/someTcell_linecount/TowardsSM/samplin'
outdir=locationofrefs+"_bestref"
os.mkdir(outdir)
filelistdf=pd.read_csv(filelits,sep='\t')
filelistdf.head()


# In[2]:


def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))


# In[3]:


allfiles=listdir_nohidden(locationofrefs)


# In[4]:


for index, row in filelistdf.iterrows():
    currentfile=locationofrefs+'/'+row['Filename']
    tdf=pd.read_csv(currentfile,sep='\t',header=None)
    tdf.rename(columns={0:'chrom',1:'start',2:'end'},inplace=True)
    tdf['em4-others']=-1*row['Average Value']
    tdf['FakeCell-others']=0.9
    outname=outdir+"/SM_"+str(index)
    tdfsm=tdf[['chrom','start','em4-others','FakeCell-others']]
    tdfsmpos=tdf[['chrom','start','end']]
    tdfsm.to_csv(outname,sep='\t',index=False)
    tdfsmpos.to_csv(outname+'pos',sep='\t',index=False,header=False)
    

