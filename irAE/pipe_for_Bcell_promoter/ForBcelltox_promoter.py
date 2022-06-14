#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import sys

gtfile='/Users/irffanalahi/Research/Research_update/GENE/Someresults/Bcell_toxicity/downstream/ALL_tox_gt.txt'

gtdf=pd.read_csv(gtfile,sep='\t',index_col=0)
gtdf.head()


# In[2]:


gtdf=gtdf[gtdf['Toxicity'].notna()]
gtdf.head()


# In[3]:


gtdf.shape


# In[4]:


promoter_avg_file=sys.argv[1] #'/Users/irffanalahi/Research/Research_update/GENE/Someresults/Bcell_toxicity/downstream/fresh_boxplots/melanoma_bg_BS_all_matrix_intesectedwith_Bcell_toxicity_promoter_singleValue.txt_Bcell_toxicity_promoter_singleValue.txt_prepared_NAhandled_forregression/IL10.txt_median.txt'
promoter_avg_df=pd.read_csv(promoter_avg_file,sep='\t',index_col=0)

promoter_avg_df.head()


# In[5]:


if 'mean' in promoter_avg_df.columns[0]:
    genename=promoter_avg_df.columns[0].replace('_mean','')
    
    txttoadd='mean'
elif 'median' in promoter_avg_df.columns[0]:
    genename=promoter_avg_df.columns[0].replace('_median','')
    txttoadd='median'


# In[6]:


promoter_avg_df['1-'+txttoadd+' promoter methylation']=1-promoter_avg_df[promoter_avg_df.columns[0]]


# In[7]:


promoter_avg_df.shape


# In[8]:


merged=promoter_avg_df.merge(gtdf,left_index=True, right_index=True)

merged.shape


# In[9]:


merged.head()


# In[10]:


#merged.boxplot(by ='Toxicity', column =['1-avg promoter methylation'], grid = False)


# In[11]:


ax = sns.boxplot(x="Toxicity", y='1-'+txttoadd+' promoter methylation', data=merged,color='white')
ax = sns.stripplot(x="Toxicity", y='1-'+txttoadd+' promoter methylation', data=merged)
plt.title(genename+" promoter")
plt.savefig(promoter_avg_file+".pdf")

