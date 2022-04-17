#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import seaborn as sns; sns.set()

import matplotlib.pyplot as plt
import sys
import os


heatfile=sys.argv[1] #'BL22LTMEtraining_all_matrix_interwith_oldSMtil'
phenfile='BL22LTME_CD8TIL_Phenoclass.txt_ctrename_withMELtumor_withpatientpblCRCgbioWB_moregranularALTTIL_ordered.txt'


heatdf=pd.read_csv(heatfile,sep="\t",index_col=0) ##################
heatdf.head()


# In[4]:


phendf=pd.read_csv(phenfile,sep="\t",index_col=0,header=None)
phendf.head()


# In[9]:


plt.figure(figsize=(35,10))
mycmap = plt.cm.viridis
mycmap.set_bad("dimgrey")

aaa=sns.heatmap(heatdf, cmap=mycmap)
cell_ticks = aaa.get_xticks()
phendf_T = phendf.transpose()
idx_lst = []
label_lst = []
for col in phendf_T.columns:
    col_vals = list(phendf_T[col])
    col_vals.reverse()
    idx = col_vals.index(1)
    count = col_vals.count(1)
    real_idx = len(col_vals) - idx - 1
    if count % 2 == 0:
        idx1 = real_idx - int(count / 2)
        idx2 = idx1 + 1
        label_lst.append((cell_ticks[idx1] + cell_ticks[idx2]) / 2)
    else:
        count -= 1
        count /= 2
        label_lst.append(cell_ticks[real_idx - int(count)])
    idx_lst.append(len(col_vals) - idx)
idx_lst = idx_lst[:-1]

plt.yticks(rotation=0)
plt.title(os.path.basename(heatfile).split('_')[0].split('.')[0], fontsize=35,pad=300)
ymax, ymin = aaa.get_ylim()
for idx in idx_lst:
    aaa.axvline(x=idx, ymin=ymin, ymax=ymax, lw=4, color='orange')
for i, col in enumerate(phendf_T.columns):
    aaa.annotate(col, xy=(label_lst[i], 0.0), xytext=(0.0, 10), textcoords='offset points', fontsize=20, ha='center',rotation=90)
plt.savefig(heatfile + '.pdf', bbox_inches='tight')


# In[ ]:





# In[ ]:




