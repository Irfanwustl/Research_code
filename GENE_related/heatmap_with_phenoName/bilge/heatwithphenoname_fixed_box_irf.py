#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import seaborn as sns; sns.set()
import numpy as np
import matplotlib.pyplot as plt
import sys


heatfile=sys.argv[1] #'BL22LTMEtraining_all_matrix_interwith_oldSMtil'
phenfile='MajorLineage_PHENOCLASS.txt'


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
plt.title(heatfile, fontsize=25, pad=300)
ymax, ymin = aaa.get_ylim()
for idx in idx_lst:
    aaa.axvline(x=idx, ymin=ymin, ymax=ymax, lw=4, color='orange')
for i, col in enumerate(phendf_T.columns):
    aaa.annotate(col, xy=(label_lst[i], 0.0), xytext=(0.0, 10), textcoords='offset points', fontsize=20, ha='center',rotation=90)
plt.savefig(heatfile + '.pdf', bbox_inches='tight')


phendf_T = phendf.transpose()
cells = list(phendf_T.columns)
cols = list(heatdf.columns)
cell_arrs = {}
max_len = 0
for cell in cells:
    cell_arrs[cell] = []
    locs = np.array(phendf_T[cell])
    idx = np.where(locs==1)[0]
    for i in idx:
        col = cols[i]
        cell_arrs[cell] += list(heatdf[col])
    if len(cell_arrs[cell]) > max_len:
        max_len = len(cell_arrs[cell])
        
for cell in cell_arrs:
    if len(cell_arrs[cell]) != max_len:
        cell_arrs[cell].extend([np.nan]*(max_len-len(cell_arrs[cell])))
        
box_df = pd.DataFrame.from_dict(cell_arrs)
fig, ax = plt.subplots(1, 1, figsize=(35, 10))
c = 'black'
ax = sns.boxplot(data=box_df, ax=ax, color='black')
plt.setp(ax.artists, edgecolor = 'k', facecolor='w')
plt.setp(ax.lines, color='k')
plt.xticks(rotation=90)
ax.tick_params(labelsize=18)
plt.savefig(heatfile + '_boxplot.pdf', bbox_inches='tight')

fig, ax = plt.subplots(1, 1, figsize=(35, 10))
ax = sns.boxplot(data=box_df, ax=ax, color='black')
plt.setp(ax.artists, edgecolor = 'k', facecolor='w')
plt.setp(ax.lines, color='k')
plt.xticks(rotation=90)
ax.tick_params(labelsize=18)
ax.invert_yaxis()
plt.savefig(heatfile + '_boxplot_inverted.pdf', bbox_inches='tight')

box_df.to_csv(heatfile + '_boxplot.txt',sep='\t',index=False)
(box_df.mean()).to_csv(heatfile + '_boxplotmean.txt',sep='\t')


