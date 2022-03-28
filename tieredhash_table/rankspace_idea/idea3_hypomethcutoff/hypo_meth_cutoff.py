#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys
infile=sys.argv[1] #'NaiveCD4_CpGdelta_info_faster.txt_fullinfo_head1000.txt'
outname=infile
indf=pd.read_csv(infile,sep='\t')
howmanytop=int(sys.argv[2])  #100
maxhypo=[.1,.2,.3]
indf.head()


# In[2]:


indf.columns


# In[3]:


incolnames=(indf.columns).tolist()
scorcols=[s for s in incolnames if '-' in s]
scorcols


# In[4]:


scorcols
currentCttoconsider=list(set([i.split('-', 1)[0] for i in scorcols]))
if len(currentCttoconsider)!=1:
    print('error')
    sys.exit(1)
currentCttoconsider=currentCttoconsider[0]
currentCttoconsider


# In[5]:


def savedifferentversion(currentdf,version):

    for mh in maxhypo:
        temp=currentdf[currentdf[currentCttoconsider]<=mh]
        temptop=temp.head(n=howmanytop)


        tempoutname=outname+"_"+version+"_maxhypo_"+str(mh)+"_top_"+str(howmanytop)

        temptop.to_csv(tempoutname,sep='\t',index=False)
        temptop[['chrom','start','end']].to_csv(tempoutname+"_pos",sep='\t',index=False,header=False)


# In[6]:


outdfv1=indf.sort_values('(Minimum delta rank+Average delta rank)/2')
outdfv2=indf.sort_values('(OwnGroup_avg_delta rank+OtherGroup_avg_delta rank)/2')

savedifferentversion(outdfv1,'v1')
savedifferentversion(outdfv2,'v2')

