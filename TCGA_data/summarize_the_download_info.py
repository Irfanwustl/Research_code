#!/usr/bin/env python
# coding: utf-8

# In[1]:


import glob
import os
import pandas as pd
import shutil
import sys

# In[2]:


downloadedDir=sys.argv[1] #'/Users/irffanalahi/Desktop/noneed/TCGA'
outdir=downloadedDir+"_all_info"
os.makedirs(outdir)


# In[3]:


def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))


# In[4]:


downloadedDirfiles=listdir_nohidden(downloadedDir)
downloadedDirfiles


# In[5]:


alldirs=[]
for adriname in downloadedDirfiles:
    if os.path.isdir(adriname):
        alldirs.append(adriname)
alldirs


# In[6]:


for adir in alldirs:
    infoname=adir+"/"+os.path.basename(adir)+".txt"
    if os.path.exists(infoname)==True:
        shutil.copy(infoname, outdir+"/"+os.path.basename(adir)+".txt")


# In[7]:


files = glob.glob(outdir+'/*.txt')
filesdf=[pd.read_csv(fp,sep="\t") for fp in files]


# In[8]:


df_combined = pd.concat(filesdf, axis=0)
df_combined.head()


# In[9]:


df_combined_rename=df_combined.copy()


# In[10]:


df_combined_rename.rename(columns={"cases.0.disease_type": "Disease type", "cases.0.primary_site": "Primary site",'cases.0.project.project_id':'Project','cases.0.samples.0.sample_type':'Sample type','cases.0.submitter_id':'Submitter id','file_name':'File name','id':'File UUID'},inplace=True)
df_combined_rename.head()


# In[11]:


grouped=df_combined_rename.groupby('Project')


# In[12]:


from collections import defaultdict

summarydict=defaultdict(list)

for name, group in grouped:
    normal=group[group['Sample type']=='Solid Tissue Normal'].shape[0]
    tumor=group.shape[0]-normal
    summarydict['Project'].append(name)
    summarydict['Normal'].append(normal)
    summarydict['Tumor'].append(tumor)
    
    


# In[13]:


summarydf=pd.DataFrame.from_dict(summarydict)
summarydf


# In[14]:


outexcel=df_combined_rename.drop(['Disease type','Submitter id'],axis=1)
outexcel=outexcel[['Project','Primary site','Sample type','File name','File UUID']]
outexcel.head()


# In[15]:



with pd.ExcelWriter(outdir+'.xlsx') as writer:  
    outexcel.to_excel(writer, sheet_name='Sheet_1',index=False)
    summarydf.to_excel(writer, sheet_name='summary',index=False)


# In[16]:


df_combined.to_excel(outdir+"_rawinfo.xlsx",index=False)

