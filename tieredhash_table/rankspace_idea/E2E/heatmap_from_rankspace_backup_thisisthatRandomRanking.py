#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import seaborn as sns
import sys
#get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt


##towards_rankspace output##

infile=sys.argv[1]  #'tr_sub_CpGdelta_info.txt'
outname=infile

howmanytop=int(sys.argv[2]) #1000

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


mycmap = plt.cm.viridis
mycmap.set_bad("dimgrey")
aaa=sns.heatmap(outdfforheat, cmap=mycmap,vmin=0, vmax=1,yticklabels=False)

aaa.xaxis.tick_top()

aaa.set_xticklabels(aaa.get_xticklabels(),rotation = 90)

cbar = aaa.collections[0].colorbar#.set_label('# of contacts', horizontalalignment='left')
cbar.ax.set_title('delta')
heatname=outname+"_"+str(howmanytop)+"_heat"+".pdf"
plt.savefig(heatname,bbox_inches = "tight")


# In[13]:


outdf=outdf.sort_values('Minimum delta',ascending=False)
outdf.reset_index(inplace=True)
outdf.reset_index(inplace=True)
outdf.head()


# In[14]:


outdf.rename(columns={'index':'Minimum delta rank'},inplace=True)
outdf.set_index(['chrom','start','end'],inplace=True)
outdf.head()


# In[15]:


outdf=outdf.sort_values('Average delta',ascending=False)
outdf.reset_index(inplace=True)
outdf.reset_index(inplace=True)
outdf.rename(columns={'index':'Average delta rank'},inplace=True)
outdf.set_index(['chrom','start','end'],inplace=True)
outdf.head()


# In[16]:


outdf['(Minimum delta rank+Average delta rank)/2']=(outdf['Minimum delta rank']+outdf['Average delta rank'])/2
outdf=outdf.sort_values('(Minimum delta rank+Average delta rank)/2')
outdf.head()


# In[17]:


outdfforheatRANKED=outdf.copy()
if outdfforheatRANKED.shape[0]>howmanytop:
    outdfforheatRANKED=outdfforheatRANKED.head(n=howmanytop)


# In[18]:



aaa=sns.heatmap(outdfforheatRANKED[newscorecols],vmin=0, vmax=1, cmap=mycmap,yticklabels=False) #vmin=0, vmax=1,

aaa.xaxis.tick_top()

aaa.set_xticklabels(aaa.get_xticklabels(),rotation = 90)

cbar = aaa.collections[0].colorbar#.set_label('# of contacts', horizontalalignment='left')
cbar.ax.set_title('delta')
heatname=outname+"_"+str(howmanytop)+"_heat_RANKED"+".pdf"
plt.savefig(heatname,bbox_inches = "tight")


# In[19]:



outdf.reset_index(inplace=True)
outdfforheat.reset_index(inplace=True)
outdfforheatRANKED.reset_index(inplace=True)
outdf.to_csv(outname+"_forheatfullinfo.txt",sep='\t',index=False)
outdfforheat.to_csv(outname+"_"+str(howmanytop)+"_forheatunderlyingdata.txt",sep='\t',index=False)

outdfforheatRANKED.to_csv(outname+"_"+str(howmanytop)+"_forheatunderlyingdata_ranked.txt",sep='\t',index=False)
outdfforheatRANKED[['chrom','start','end']].to_csv(outname+"_"+str(howmanytop)+"_forheatunderlyingdata_ranked_pos.txt",sep='\t',index=False,header=False)

