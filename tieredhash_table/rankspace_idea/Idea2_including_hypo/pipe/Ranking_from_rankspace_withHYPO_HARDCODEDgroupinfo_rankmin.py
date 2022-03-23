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


outdf=indf.copy()


# In[10]:


outdf['Minimum delta rank']=outdf['Minimum delta'].rank(method='min',ascending=False)


# In[11]:


outdf['Average delta rank']=outdf['Average delta'].rank(method='min',ascending=False)


# In[12]:


outdf['(Minimum delta rank+Average delta rank)/2']=(outdf['Minimum delta rank']+outdf['Average delta rank'])/2


# In[13]:


####find out group delta####

outgroupcols=[]
for gr in groupinfo:
     outgroupcols=outgroupcols+[s for s in scorcols if gr in s]

#print(outgroupcols)
owngroupcols=list(set(scorcols)-set(outgroupcols))
#print(owngroupcols)


# In[14]:


outdf['OwnGroup_avg_delta']=outdf[owngroupcols].mean(axis=1)
outdf['OtherGroup_avg_delta']=outdf[outgroupcols].mean(axis=1)


# In[15]:


outdf['OwnGroup_avg_delta rank']=outdf['OwnGroup_avg_delta'].rank(method='min',ascending=False)


# In[16]:


outdf['OtherGroup_avg_delta rank']=outdf['OtherGroup_avg_delta'].rank(method='min',ascending=False)


# In[17]:


outdf['(OwnGroup_avg_delta rank+OtherGroup_avg_delta rank)/2']=(outdf['OwnGroup_avg_delta rank']+outdf['OtherGroup_avg_delta rank'])/2
outdf['(OwnGroup_avg_delta rank+Average delta rank)/2']=(outdf['OwnGroup_avg_delta rank']+outdf['Average delta rank'])/2

outdf.head()


# In[18]:


scorcols
currentCttoconsider=list(set([i.split('-', 1)[0] for i in scorcols]))
if len(currentCttoconsider)!=1:
    print('error')
    sys.exit(1)
currentCttoconsider=currentCttoconsider[0]
currentCttoconsider


# In[19]:


outdf['Methylation rank']=outdf[currentCttoconsider].rank(method='min')
outdf.head()


# In[20]:


outdf['(Methylation rank+OtherGroup_avg_delta rank+OwnGroup_avg_delta rank)/3']=(outdf['Methylation rank']+outdf['OtherGroup_avg_delta rank']+outdf['OwnGroup_avg_delta rank'])/3

outdf['(Methylation rank+Average delta rank+OwnGroup_avg_delta rank)/3']=(outdf['Methylation rank']+outdf['Average delta rank']+outdf['OwnGroup_avg_delta rank'])/3

outdf['(Methylation rank+Average delta rank+Minimum delta rank)/3']=(outdf['Methylation rank']+outdf['Average delta rank']+outdf['Minimum delta rank'])/3


# In[21]:



outdfv1=outdf.sort_values('(Minimum delta rank+Average delta rank)/2')
outdfv2=outdf.sort_values('(OwnGroup_avg_delta rank+OtherGroup_avg_delta rank)/2')
outdfv3=outdf.sort_values('(OwnGroup_avg_delta rank+Average delta rank)/2')




outdfv2hyporanked=outdf.sort_values('(Methylation rank+OtherGroup_avg_delta rank+OwnGroup_avg_delta rank)/3')
outdfv1hyporanked=outdf.sort_values('(Methylation rank+Average delta rank+Minimum delta rank)/3')

outdfv3hyporanked=outdf.sort_values('(Methylation rank+Average delta rank+OwnGroup_avg_delta rank)/3')


# In[22]:



  
outdfv1top=outdfv1.head(n=howmanytop)
outdfv2top=outdfv2.head(n=howmanytop)
outdfv3top=outdfv3.head(n=howmanytop)






outdfv1hyporankedtop=outdfv1hyporanked.head(n=howmanytop)
outdfv2hyporankedtop=outdfv2hyporanked.head(n=howmanytop)
outdfv3hyporankedtop=outdfv3hyporanked.head(n=howmanytop)




# In[23]:



outdf.reset_index(inplace=True)
outdfv1top.reset_index(inplace=True)
outdfv2top.reset_index(inplace=True)
outdfv3top.reset_index(inplace=True)


outdfv2hyporankedtop.reset_index(inplace=True)
outdfv3hyporankedtop.reset_index(inplace=True)
outdfv1hyporankedtop.reset_index(inplace=True)

outdf.to_csv(outname+"_fullinfo.txt",sep='\t',index=False)


outdfv1top.to_csv(outname+"_V1_rankedtop"+str(howmanytop)+".txt",sep='\t',index=False)

outdfv2top.to_csv(outname+"_V2_rankedtop"+str(howmanytop)+".txt",sep='\t',index=False)

outdfv3top.to_csv(outname+"_V3_rankedtop"+str(howmanytop)+".txt",sep='\t',index=False)

outdfv1top[['chrom','start','end']].to_csv(outname+"_V1_rankedtop"+str(howmanytop)+"_pos",sep='\t',index=False,header=False)

outdfv2top[['chrom','start','end']].to_csv(outname+"_V2_rankedtop"+str(howmanytop)+"_pos",sep='\t',index=False,header=False)

outdfv3top[['chrom','start','end']].to_csv(outname+"_V3_rankedtop"+str(howmanytop)+"_pos",sep='\t',index=False,header=False)



outdfv2hyporankedtop.to_csv(outname+"_V2hypo_rankedtop"+str(howmanytop)+".txt",sep='\t',index=False)

outdfv3hyporankedtop.to_csv(outname+"_V3hypo_rankedtop"+str(howmanytop)+".txt",sep='\t',index=False)

outdfv1hyporankedtop.to_csv(outname+"_V1hypo_rankedtop"+str(howmanytop)+".txt",sep='\t',index=False)




outdfv2hyporankedtop[['chrom','start','end']].to_csv(outname+"_V2hypo_rankedtop"+str(howmanytop)+"_pos",sep='\t',index=False,header=False)
outdfv3hyporankedtop[['chrom','start','end']].to_csv(outname+"_V3hypo_rankedtop"+str(howmanytop)+"_pos",sep='\t',index=False,header=False)
outdfv1hyporankedtop[['chrom','start','end']].to_csv(outname+"_V1hypo_rankedtop"+str(howmanytop)+"_pos",sep='\t',index=False,header=False)



