#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys
infile=sys.argv[1]  #'/Users/irffanalahi/Research/Research_update/for_backgroundcalculation/noEPCAMbgrolled_head/BS-Seq_07-no-spike.bedgraph_rolled.bedgraph'


outfile=sys.argv[2]



howmanySM=int(sys.argv[3]) #3



celltype='EPCAM-others'

totalcpg=int(sys.argv[4])

avgdelta=float(sys.argv[5])


indf=pd.read_csv(infile,sep='\t',header=None)

indf.head()


# In[2]:


indf.rename(columns={0: 'chrom', 1: 'start',2:'end'},inplace=True)

indf[celltype]=avgdelta
indf['FakeCell-others']=0.9
indfrequiredcols=indf[['chrom','start',celltype,'FakeCell-others']].copy()
indfrequiredcols.head()


# In[3]:


for i in range(howmanySM):
    tempsm=indfrequiredcols.sample(n=totalcpg)
    tempsm.to_csv(outfile+"_randomSM_"+str(i)+".txt",sep='\t',index=False)
    

