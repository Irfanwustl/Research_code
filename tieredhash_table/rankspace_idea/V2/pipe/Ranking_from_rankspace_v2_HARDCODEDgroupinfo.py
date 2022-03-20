#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import seaborn as sns
import sys
#get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt


##towards_rankspace output##

infile= sys.argv[1] #'Tregs_CpGdelta_info_faster_head_1000.txt'
outname=infile


groupinfo=['Tcell','Myloid','PMNlike','Bcell']

howmanytop=int(sys.argv[2])



indf=pd.read_csv(infile,sep='\t')
indf.set_index(['chrom','start','end'],inplace=True)
indf.head()


# In[2]:


indf=indf[indf['maxdelta']<0]
indf.head()


# In[3]:


indf=-1*indf
indf.head()


# In[4]:


indf.rename(columns={'maxdelta':'Minimum delta','mindelta':'Maximum delta','Avgdelta':'Average delta'},inplace=True)
indf.head()


# In[5]:


indf['(Minimum delta+Average delta)/2']=(indf['Minimum delta']+indf['Average delta'])/2
indf.head()


# In[6]:


outdf=indf.sort_values('(Minimum delta+Average delta)/2',ascending=False)
outdf.head()


# In[7]:


outdfcolnames=(outdf.columns).tolist()
scorcols=[s for s in outdfcolnames if '-' in s]
scorcols


# In[8]:


def renamect(act):
    if act=='CD4':
        return 'Naive CD4 T'
    if act=='CD8':
        return 'Naive CD8 T'

    if act=='NaiveCD4':
        return 'Naive CD4 T'
    if act=='NaiveCD8':
        return 'Naive CD8 T'
    if act=='Tr':
        return 'Tregs'
    if act=='mB':
        return 'Memory B'
    if act=='nB':
        return 'Naive B'
    if act=='m4':
        return 'Memory CD4 T'
    if act=='m8':
        return 'Memory CD8 T'
    if act=='Mn':
        return 'Mono'


    if act=='em8':
        return 'CD8 TEM'
    if act=='cm8':
        return 'CD8 TCM'

    if act=='em4':
        return 'CD4 TEM'
    if act=='cm4':
        return 'CD4 TCM'


    if act=='ed8':
        return 'CD8 TEMRA'

    if act=='PC':
        return 'PC'

    if act=='M0':
        return 'Macrophage (M0)'

    if act=='M1':
        return 'Macrophage (M1)'

    if act=='M2':
        return 'Macrophage (M2)'
    if act=='Eo':
        return 'Eosinophil'

    if act=='Mg':
        return 'Megakaryocyte'




    return act


# In[9]:



newscorecols=[]
score_rename_dict={}
for score in scorcols:
    scoreplit=score.split("-")
    c1=renamect(scoreplit[0])
    c2=renamect(scoreplit[1])
  
    newscorename=c1+"-"+c2
    score_rename_dict[score]=newscorename
    
    newscorecols.append(newscorename)
    
score_rename_dict    


# In[10]:


outdf.rename(columns=score_rename_dict,inplace=True)
outdf.head()


# In[11]:


outdfforheat=outdf.copy()
if outdfforheat.shape[0]>howmanytop:
    outdfforheat=outdfforheat.head(n=howmanytop)


# In[12]:


outdf=outdf.sort_values('Minimum delta',ascending=False)
outdf.reset_index(inplace=True)
outdf.reset_index(inplace=True)
outdf.head()


# In[13]:


outdf.rename(columns={'index':'Minimum delta rank'},inplace=True)
outdf.set_index(['chrom','start','end'],inplace=True)
outdf.head()


# In[14]:


outdf=outdf.sort_values('Average delta',ascending=False)
outdf.reset_index(inplace=True)
outdf.reset_index(inplace=True)
outdf.rename(columns={'index':'Average delta rank'},inplace=True)
outdf.set_index(['chrom','start','end'],inplace=True)
outdf.head()


# In[15]:


outdf['(Minimum delta rank+Average delta rank)/2']=(outdf['Minimum delta rank']+outdf['Average delta rank'])/2
outdf=outdf.sort_values('(Minimum delta rank+Average delta rank)/2')
outdf.head()


# In[16]:


####find out group delta####
newscorecols
groupinfo
outgroupcols=[]
for gr in groupinfo:
     outgroupcols=outgroupcols+[s for s in newscorecols if gr in s]

#print(outgroupcols)
owngroupcols=list(set(newscorecols)-set(outgroupcols))
#print(owngroupcols)


# In[17]:


outdf['OwnGroup_avg_delta']=outdf[owngroupcols].mean(axis=1)
outdf['OtherGroup_avg_delta']=outdf[outgroupcols].mean(axis=1)
outdf=outdf.sort_values('OwnGroup_avg_delta',ascending=False)
outdf.reset_index(inplace=True)
outdf.reset_index(inplace=True)
outdf.rename(columns={'index':'OwnGroup_avg_delta rank'},inplace=True)
outdf.set_index(['chrom','start','end'],inplace=True)
outdf.head()


# In[18]:


outdf=outdf.sort_values('OtherGroup_avg_delta',ascending=False)
outdf.reset_index(inplace=True)
outdf.reset_index(inplace=True)
outdf.rename(columns={'index':'OtherGroup_avg_delta rank'},inplace=True)
outdf.set_index(['chrom','start','end'],inplace=True)
outdf.head()


# In[19]:


outdf['(OwnGroup_avg_delta rank+OtherGroup_avg_delta rank)/2']=(outdf['OwnGroup_avg_delta rank']+outdf['OtherGroup_avg_delta rank'])/2
outdf['(OwnGroup_avg_delta rank+Average delta rank)/2']=(outdf['OwnGroup_avg_delta rank']+outdf['Average delta rank'])/2

outdf.head()


# In[20]:


outdfv2=outdf.sort_values('(OwnGroup_avg_delta rank+OtherGroup_avg_delta rank)/2')
outdfv2.head()


# In[21]:


outdfv3=outdf.sort_values('(OwnGroup_avg_delta rank+Average delta rank)/2')
outdfv3.head()


# In[22]:


outdftopv2=outdfv2.copy()
if outdftopv2.shape[0]>howmanytop:
    outdftopv2=outdftopv2.head(n=howmanytop)
outdftopv3=outdfv3.copy()
if outdftopv3.shape[0]>howmanytop:
    outdftopv3=outdftopv3.head(n=howmanytop)


# In[23]:



outdf.reset_index(inplace=True)
outdftopv2.reset_index(inplace=True)
outdftopv3.reset_index(inplace=True)
outdf.to_csv(outname+"_fullinfo.txt",sep='\t',index=False)
outdftopv2.to_csv(outname+"_V2_rankedtop"+str(howmanytop)+".txt",sep='\t',index=False)
outdftopv3.to_csv(outname+"_V3_rankedtop"+str(howmanytop)+".txt",sep='\t',index=False)


outdftopv2[['chrom','start','end']].to_csv(outname+"_V2_rankedtop"+str(howmanytop)+"_pos",sep='\t',index=False,header=False)
outdftopv3[['chrom','start','end']].to_csv(outname+"_V3_rankedtop"+str(howmanytop)+"_pos",sep='\t',index=False,header=False)

