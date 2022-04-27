#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import glob
import os
import sys
import shutil
infofile=sys.argv[1] #'/Users/irffanalahi/Research/Research_update/opensource_data/ENCODE/downloadtest/?status=released&internal_tags=ENTEx&assay_title=WGBS&type=Experiment&files.analyses.status=released&files.preferred_default=true.txt'


indir=sys.argv[2] #'/Users/irffanalahi/Research/Research_update/opensource_data/ENCODE/downloadtest/formapping'

outdir=indir+"_renamed"

os.mkdir(outdir)

infodf=pd.read_csv(infofile,sep='\t')
infodf.head()


# In[2]:


def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))


# In[3]:


allfiles=listdir_nohidden(indir)


# In[4]:


for afile in allfiles:
    corresrow=infodf[infodf['File accession']==os.path.basename(afile).split('.')[0]]
    if corresrow.shape[0]==0:
        print(afile)
        print("NOT found. But not exiting")
        continue
    
    termname=corresrow['Biosample term name'].tolist()
    if len(termname)!=1:
        print(afile)
        print('len(termname)!=1')
        sys.exit(1)
    termname=termname[0].replace(" ", "_")
    
    newname=termname+"_"+os.path.basename(afile)
    shutil.copy(afile,outdir+"/"+newname)
 

