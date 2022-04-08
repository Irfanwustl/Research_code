#!/usr/bin/env python
# coding: utf-8

# In[15]:


import pandas as pd
import sys
infile=sys.argv[1] #'SM/NaiveCD4_CpGdelta_info_faster.txt_5000_forheatunderlyingdata_ranked.txt'
outfile=sys.argv[2]   #infile+"_SM.txt"
indf=pd.read_csv(infile,sep='\t')
file_name=infile.split('/')[-1]
ct=file_name.split('_')[0]

indf.head()


# In[2]:


outdf=(indf[['chrom','start','Average delta']]).copy()
outdf['Average delta']=-1*outdf['Average delta']



outdf.rename(columns={'Average delta':ct+'-others'},inplace=True)
outdf.head()


# In[3]:

##BL22_withEPCAM
#total_compartments=['chrom','start','NaiveCD4-others','NaiveCD8-others','nB-others','NK-others','PC-others','Mono-others','M0-others','M1-others','M2-others','iDC-others','mDC-others','PMN-others','cm8-others','em8-others','Eo-others','Tregs-others','em4-others','ed8-others','Mg-others','cm4-others','Er-others','mB-others','EPCAM-others']

##BL22_withCD8TIL
total_compartments=['chrom','start','NaiveCD4-others','NaiveCD8-others','nB-others','NK-others','PC-others','Mono-others','M0-others','M1-others','M2-others','iDC-others','mDC-others','PMN-others','cm8-others','em8-others','Eo-others','Tregs-others','em4-others','ed8-others','Mg-others','cm4-others','Er-others','mB-others','CD8TIL-others']

finalcompartmentshouldbe=len(total_compartments)
total_compartments_set=set(total_compartments)


# In[4]:


indfcolumns=set(outdf.columns.tolist())


# In[5]:


missingcols=total_compartments_set-indfcolumns
missingcolslist=list(missingcols)
missingcolslist


# In[6]:


for micol in missingcolslist:
    outdf[micol]=0.9


# In[7]:


if outdf.shape[1]!=finalcompartmentshouldbe:
    print(infile)
    print("error. Exiting")
    sys.exit(1)


# In[8]:


outdf=outdf[total_compartments]
outdf.head()


# In[9]:


outdf.to_csv(outfile,sep="\t",index=False)


# In[ ]:




