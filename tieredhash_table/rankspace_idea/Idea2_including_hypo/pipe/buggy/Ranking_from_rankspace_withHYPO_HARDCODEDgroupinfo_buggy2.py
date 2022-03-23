#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import seaborn as sns
import sys
#get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt


##towards_rankspace output##

infile=sys.argv[1] #'deltainfofolder_betaInfo/Tregs_CpGdelta_info_faster_head1000.txt'
outname=sys.argv[2] #infile


groupinfo=['Tcell','Myloid','PMNlike','Bcell']

howmanytop=int(sys.argv[3])   #1000



indf=pd.read_csv(infile,sep='\t')
indf.set_index(['chrom','start','end'],inplace=True)
indf.head()


# In[2]:


indf=indf[indf['maxdelta']<0]
indf.head()


# In[3]:


incolnames=(indf.columns).tolist()
scorcols=[s for s in incolnames if '-' in s]
scorcols


# In[4]:


indf.columns


# In[5]:


colforneg=scorcols+['maxdelta', 'mindelta','Avgdelta']
colforneg


# In[6]:


indf[colforneg]=-1*indf[colforneg]
indf.head()


# In[7]:


indf.rename(columns={'maxdelta':'Minimum delta','mindelta':'Maximum delta','Avgdelta':'Average delta'},inplace=True)
indf.head()


# In[8]:


indf['(Minimum delta+Average delta)/2']=(indf['Minimum delta']+indf['Average delta'])/2
indf.head()


# In[9]:


outdf=indf.sort_values('(Minimum delta+Average delta)/2',ascending=False)
outdf.head()


# In[10]:


outdf=outdf.sort_values('Minimum delta',ascending=False)
outdf.reset_index(inplace=True)
outdf.reset_index(inplace=True)
outdf.head()


# In[11]:


outdf.rename(columns={'index':'Minimum delta rank'},inplace=True)
outdf.set_index(['chrom','start','end'],inplace=True)
outdf.head()


# In[12]:


outdf=outdf.sort_values('Average delta',ascending=False)
outdf.reset_index(inplace=True)
outdf.reset_index(inplace=True)
outdf.rename(columns={'index':'Average delta rank'},inplace=True)
outdf.set_index(['chrom','start','end'],inplace=True)
outdf.head()


# In[13]:


outdf['(Minimum delta rank+Average delta rank)/2']=(outdf['Minimum delta rank']+outdf['Average delta rank'])/2
outdf=outdf.sort_values('(Minimum delta rank+Average delta rank)/2')
outdf.head()


# In[14]:


####find out group delta####

outgroupcols=[]
for gr in groupinfo:
     outgroupcols=outgroupcols+[s for s in scorcols if gr in s]

#print(outgroupcols)
owngroupcols=list(set(scorcols)-set(outgroupcols))
#print(owngroupcols)


# In[15]:


outdf['OwnGroup_avg_delta']=outdf[owngroupcols].mean(axis=1)
outdf['OtherGroup_avg_delta']=outdf[outgroupcols].mean(axis=1)
outdf=outdf.sort_values('OwnGroup_avg_delta',ascending=False)
outdf.reset_index(inplace=True)
outdf.reset_index(inplace=True)
outdf.rename(columns={'index':'OwnGroup_avg_delta rank'},inplace=True)
outdf.set_index(['chrom','start','end'],inplace=True)
outdf.head()


# In[16]:


outdf=outdf.sort_values('OtherGroup_avg_delta',ascending=False)
outdf.reset_index(inplace=True)
outdf.reset_index(inplace=True)
outdf.rename(columns={'index':'OtherGroup_avg_delta rank'},inplace=True)
outdf.set_index(['chrom','start','end'],inplace=True)
outdf.head()


# In[17]:


outdf['(OwnGroup_avg_delta rank+OtherGroup_avg_delta rank)/2']=(outdf['OwnGroup_avg_delta rank']+outdf['OtherGroup_avg_delta rank'])/2
outdf['(OwnGroup_avg_delta rank+Average delta rank)/2']=(outdf['OwnGroup_avg_delta rank']+outdf['Average delta rank'])/2

outdf.head()


# In[18]:


outdfv3=outdf.sort_values('(OwnGroup_avg_delta rank+Average delta rank)/2')
outdfv3.head()


# In[19]:


scorcols
currentCttoconsider=list(set([i.split('-', 1)[0] for i in scorcols]))
if len(currentCttoconsider)!=1:
    print('error')
    sys.exit(1)
currentCttoconsider=currentCttoconsider[0]
currentCttoconsider


# In[20]:


outdf=outdf.sort_values(currentCttoconsider)
outdf.reset_index(inplace=True)
outdf.reset_index(inplace=True)
outdf.rename(columns={'index':'Methylation rank'},inplace=True)
outdf.set_index(['chrom','start','end'],inplace=True)
outdf.head()


# In[21]:


outdf['(Methylation rank+OtherGroup_avg_delta rank+OwnGroup_avg_delta rank)/3']=(outdf['Methylation rank']+outdf['OtherGroup_avg_delta rank']+outdf['OwnGroup_avg_delta rank'])/3

outdf['(Methylation rank+Average delta rank+OwnGroup_avg_delta rank)/3']=(outdf['Methylation rank']+outdf['Average delta rank']+outdf['OwnGroup_avg_delta rank'])/3

outdf['(Methylation rank+Average delta rank+Minimum delta rank)/3']=(outdf['Methylation rank']+outdf['Average delta rank']+outdf['Minimum delta rank'])/3


# In[22]:


outdfv2hyporanked=outdf.sort_values('(Methylation rank+OtherGroup_avg_delta rank+OwnGroup_avg_delta rank)/3')
outdfv1hyporanked=outdf.sort_values('(Methylation rank+Average delta rank+Minimum delta rank)/3')

outdfv3hyporanked=outdf.sort_values('(Methylation rank+Average delta rank+OwnGroup_avg_delta rank)/3')


# In[23]:


outdfv2hyporankedtop=outdfv2hyporanked.copy()
if outdfv2hyporanked.shape[0]>howmanytop:
    outdfv2hyporankedtop=outdfv2hyporanked.head(n=howmanytop)

    
outdfv3hyporankedtop=outdfv3hyporanked.copy()  
if outdfv3hyporanked.shape[0]>howmanytop:
    outdfv3hyporankedtop=outdfv3hyporanked.head(n=howmanytop)

outdfv1hyporankedtop=outdfv1hyporanked.copy()  
if outdfv1hyporanked.shape[0]>howmanytop:
    outdfv1hyporankedtop=outdfv1hyporanked.head(n=howmanytop)


# In[24]:



outdf.reset_index(inplace=True)
outdfv2hyporankedtop.reset_index(inplace=True)
outdfv3hyporankedtop.reset_index(inplace=True)
outdfv1hyporankedtop.reset_index(inplace=True)

outdf.to_csv(outname+"_fullinfo.txt",sep='\t',index=False)


outdfv2hyporankedtop.to_csv(outname+"_V2hypo_rankedtop"+str(howmanytop)+".txt",sep='\t',index=False)

outdfv3hyporankedtop.to_csv(outname+"_V3hypo_rankedtop"+str(howmanytop)+".txt",sep='\t',index=False)

outdfv1hyporankedtop.to_csv(outname+"_V1hypo_rankedtop"+str(howmanytop)+".txt",sep='\t',index=False)




outdfv2hyporankedtop[['chrom','start','end']].to_csv(outname+"_V2hypo_rankedtop"+str(howmanytop)+"_pos",sep='\t',index=False,header=False)
outdfv3hyporankedtop[['chrom','start','end']].to_csv(outname+"_V3hypo_rankedtop"+str(howmanytop)+"_pos",sep='\t',index=False,header=False)
outdfv1hyporankedtop[['chrom','start','end']].to_csv(outname+"_V1hypo_rankedtop"+str(howmanytop)+"_pos",sep='\t',index=False,header=False)



