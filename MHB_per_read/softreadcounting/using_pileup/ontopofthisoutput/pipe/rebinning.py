#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from collections import defaultdict

import sys

infile=sys.argv[1] #'/Users/irffanalahi/Research/Research_code/gitignorefolder/MHB_per_read/softreadcounting/testtheidea/softRD_pileup/cd4bams_softRDpileup/CD4allrange_NR_1000000_insilmix41_sorted_binnedstats.txt'
outfile=sys.argv[2]


indf=pd.read_csv(infile,sep="\t",index_col=0)

scorecolumns=['CD4-others','CD8-others','nB-others','NK-others','Mn-others','mNeu-others','m8-others','DC-others','Eo-others','Tr-others','m4-others','Mg-others','Er-others','mB-others']


scorethresh=1.5

indf.head()


# In[2]:


outdfcpgweighted=indf[indf['maxscore']>scorethresh]
outdfcpgweighted.head()


# In[3]:


ctposscoredict= defaultdict(list)
ctposfragdict= defaultdict(list)
for score in scorecolumns:
    deltabasedfragassigned=outdfcpgweighted['deltabasedfragassignment'].tolist()
    if score in deltabasedfragassigned:
        temp_posscore=outdfcpgweighted.loc[outdfcpgweighted['deltabasedfragassignment']==score,'maxscore'].tolist()
        temptotal_posscore=sum(temp_posscore)
        temp_posfrag=len(temp_posscore)
    
    else:
        temptotal_posscore=0
        temp_posfrag=0
        
    ctname=score.replace('-others','')
    
    ctposscoredict[ctname].append(temptotal_posscore)

    ctposfragdict[ctname].append(temp_posfrag)


# In[4]:


ctposscoredf=pd.DataFrame.from_dict(ctposscoredict)
ctposfragdf=pd.DataFrame.from_dict(ctposfragdict)
ctposscoredf.head()


# In[ ]:


ctposscoredf.to_csv(outfile+"_posscore.txt",sep="\t",index=False)
ctposfragdf.to_csv(outfile+"_posfrag.txt",sep="\t",index=False)

