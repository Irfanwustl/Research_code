#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats.mstats import pearsonr, spearmanr
import sys

# In[2]:


file =sys.argv[1] #'/Users/irffanalahi/Research/Research_update/SoftRD/largerEXP/BL22_tiered_rankedidea/cellular_fraction/perctcorr/maxscore_relative/flexible_cross_correlation/Previous_method_TieredV1_NOPC_toy.txt'

outfile=sys.argv[2]

#Cytof
orderedcells=['NaiveCD4','cm4', 'em4','Tregs','NK','Mono','NaiveCD8','cm8','em8','ed8', 'nB','mB']

#Flow
#orderedcells=['NaiveCD4','cm4', 'em4','Tregs','NK','Mono', 'nB','mB']
data = pd.read_csv(file, sep='\t', index_col=0)
df = pd.DataFrame(data)

df.fillna(0,inplace=True)

if df.shape[0]==0:
    sys.exit()

# In[3]:


gt = []
est = []
for col in df.columns:
    if '_real' in col:
        gt.append(col[:-5])
    else:
        est.append(col)
        
cells = list(set(gt) & set(est))

if len(cells)==0:
    sys.exit()


# In[4]:


pearson_dic = {}
spearman_dic = {}
for cell in cells:
    cell_arr = np.array(df[cell])
    pearson_dic[cell] = []
    spearman_dic[cell] = []
    for cell_real in cells:
        cell_real_arr = np.array(df[cell_real + '_real'])
        pearson_corr = pearsonr(cell_arr, cell_real_arr)[0]
        spearman_corr = spearmanr(cell_arr, cell_real_arr)[0]
        pearson_dic[cell].append(pearson_corr)
        spearman_dic[cell].append(spearman_corr)
        
df_pearson = pd.DataFrame.from_dict(pearson_dic, orient='index', columns=cells)
df_spearman = pd.DataFrame.from_dict(spearman_dic, orient='index', columns=cells)


# In[5]:


standardnamedict={"NaiveCD4": "Naive CD4 T", "NaiveCD8": "Naive CD8 T","CD4": "Naive CD4", "CD8": "Naive CD8","mB":"Memory B",'Mn':'Mono','CD14':'Mono','CD19':'B Cell','nB':'Naive B','PC':'PC','cm8':'CD8 TCM','em8':'CD8 TEM','m8':'CD8 memory','ed8':'CD8 TEMRA','cm4':'CD4 TCM','em4':'CD4 TEM','m4':'CD4 memory','mNeu':'PMN','Eo':'Eosinophil','Tr':'Tregs','Mg':'Megakaryocyte','Er':'Erythrocyte'}


# In[6]:


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


# In[7]:


common_cells=intersection(orderedcells, df_pearson.columns)
if len(common_cells)>0:
    df_pearson=df_pearson.reindex(orderedcells).dropna(how='all')
    df_pearson=df_pearson.reindex(orderedcells,axis=1).dropna(how='all', axis=1)

    df_spearman=df_spearman.reindex(orderedcells).dropna(how='all')
    df_spearman=df_spearman.reindex(orderedcells,axis=1).dropna(how='all', axis=1)





df_pearson.rename(columns=standardnamedict,inplace=True)
df_pearson.rename(index=standardnamedict,inplace=True)

df_spearman.rename(columns=standardnamedict,inplace=True)
df_spearman.rename(index=standardnamedict,inplace=True)

df_pearson.head()


# In[8]:


df_pearson.to_csv(outfile + '_pearson.txt', sep='\t')
df_spearman.to_csv(outfile + '_spearman.txt', sep='\t')


# In[9]:


fig, ax = plt.subplots(1, 1, figsize=(13, 8))

sns.heatmap(df_pearson, cmap='viridis', annot=True,annot_kws={"size": 10}, ax=ax, vmin=-1, vmax=1)
ax.set_xlabel('Ground Truth', fontsize=22)
ax.set_ylabel('Read Counting', fontsize=22)
ax.set_title('Pearson Correlation', fontsize=18)

ax.set_xticklabels(ax.get_xmajorticklabels(), fontsize = 12,rotation=90)
ax.set_yticklabels(ax.get_ymajorticklabels(), fontsize = 12,rotation=0)


plt.savefig(outfile + '_crosscorrelation_pearson.pdf', bbox_inches='tight')


# In[10]:


fig2, ax2 = plt.subplots(1, 1, figsize=(15, 10))

sns.heatmap(df_spearman, cmap='viridis', annot=True,annot_kws={"size": 10}, ax=ax2, vmin=-1, vmax=1)
ax2.set_xlabel('Ground Truth', fontsize=22)
ax2.set_ylabel('Read Counting', fontsize=22)
ax2.set_title('Spearman Correlation', fontsize=18)

ax2.set_xticklabels(ax2.get_xmajorticklabels(), fontsize = 12,rotation=90)
ax2.set_yticklabels(ax2.get_ymajorticklabels(), fontsize = 12,rotation=0)

plt.savefig(outfile + '_crosscorrelation_spearman.pdf', bbox_inches='tight')


# In[ ]:




