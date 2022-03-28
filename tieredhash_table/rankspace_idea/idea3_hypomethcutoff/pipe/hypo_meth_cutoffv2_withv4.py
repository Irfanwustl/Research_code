#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import math
import sys
infile=sys.argv[1] #'NaiveCD4_CpGdelta_info_faster.txt_fullinfo_head1000.txt'
outname=sys.argv[2]
indf=pd.read_csv(infile,sep='\t')
howmanytop=int(sys.argv[3])
maxhypo=[.1,1.5,.2,.3,1]
indf.head()


# In[2]:


indf.columns


# In[3]:


incolnames=(indf.columns).tolist()
scorcols=[s for s in incolnames if '-' in s]
scorcols


# In[4]:


indf['secondMinimumDelta']=math.inf


# In[5]:


indf.head()


# In[6]:


for index, row in indf.iterrows():
    currentlist=set((row[scorcols]).tolist())
    secondmin=sorted(currentlist)[1]
    
    indf.loc[index,'secondMinimumDelta']=secondmin
  


# In[7]:


indf.head()


# In[8]:


indf['secondMinimumDelta rank']=indf['secondMinimumDelta'].rank(method='dense',ascending=False)


# In[9]:


indf['(Minimum delta rank+secondMinimumDelta rank+Average delta rank)/3']=(indf['Minimum delta rank']+indf['secondMinimumDelta rank']+indf['Average delta rank'])/3
indf.head()


# In[10]:


scorcols
currentCttoconsider=list(set([i.split('-', 1)[0] for i in scorcols]))
if len(currentCttoconsider)!=1:
    print('error')
    sys.exit(1)
currentCttoconsider=currentCttoconsider[0]
currentCttoconsider


# In[11]:


def savedifferentversion(currentdf,version):

    for mh in maxhypo:
        temp=currentdf[currentdf[currentCttoconsider]<=mh]
        temptop=temp.head(n=howmanytop)


        tempoutname=outname+"_"+version+"_maxhypo_"+str(mh)+"_top_"+str(howmanytop)

        temptop.to_csv(tempoutname,sep='\t',index=False)
        temptop[['chrom','start','end']].to_csv(tempoutname+"_pos",sep='\t',index=False,header=False)


# In[12]:


outdfv1=indf.sort_values('(Minimum delta rank+Average delta rank)/2')
outdfv2=indf.sort_values('(OwnGroup_avg_delta rank+OtherGroup_avg_delta rank)/2')

outdfv4=indf.sort_values('(Minimum delta rank+secondMinimumDelta rank+Average delta rank)/3')

savedifferentversion(outdfv1,'v1')
savedifferentversion(outdfv2,'v2')

savedifferentversion(outdfv4,'v4')


indf.to_csv(outname+"_finalallinfowithV4.txt",sep='\t',index=False)

