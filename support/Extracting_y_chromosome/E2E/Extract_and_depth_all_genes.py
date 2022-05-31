#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import glob
import os
from collections import defaultdict
import sys

infolder=sys.argv[1] #'/Users/irffanalahi/Research/Research_update/Gender_analysis/for_igv/better_depth/chrY_pp_Y_depthfullinfo'
geneinfofile=sys.argv[2] #'/Users/irffanalahi/Research/Research_update/Gender_analysis/Extracting_SRY_gene/chrY_gene_1000_1000.txt'

geneinfodf=pd.read_csv(geneinfofile,sep='\t',header=None)
geneinfodf.head()


# In[2]:


genelist=geneinfodf[3].tolist()
#genelist


# In[3]:


def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))


# In[4]:


allfiles=listdir_nohidden(infolder)


# In[5]:


outdict = defaultdict(list)
outdictgenesize = defaultdict(list)



for infile in allfiles:
    indf=pd.read_csv(infile,sep='\t',header=None)
    for index, row in geneinfodf.iterrows():
        
 
        #print(type(row[0]),type(row[1]),type(row[2]))
        
        SRYdf=indf[(indf[0]==row[0]) & (indf[1]>=row[1]) & (indf[1]<=row[2])]
        
        gene_size=row[2]-row[1]

        if SRYdf.shape[0]==0:
            tempmedian=0
            normalizby_gene_size=0
        else:
            tempmedian=SRYdf[2].median()
            normalizby_gene_size=SRYdf[2].sum()/gene_size
            


        outdict[os.path.basename(infile)].append(tempmedian)
        outdictgenesize[os.path.basename(infile)].append(normalizby_gene_size)


# In[6]:


#outdict


# In[7]:


outdf=pd.DataFrame.from_dict(outdict,orient='index',columns=genelist)
outdf.to_csv(infolder+"_gene_depth.txt",sep='\t')

outdf_genesize=pd.DataFrame.from_dict(outdictgenesize,orient='index',columns=genelist)
outdf_genesize.to_csv(infolder+"_gene_depth_normalizbygenesize.txt",sep='\t')

