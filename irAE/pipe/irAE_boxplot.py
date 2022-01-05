#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import sys

infile=sys.argv[1] #'/Users/irffanalahi/Research/Research_update/SoftRD/largerEXP/BL22genepromdelta.7/Realdata/irAE/code_develop/rAAE_boxplots/try2/BL22_genepromSM_0.7.txt_TRAININGbestref.txt_result_dupindex_binnedstats.pkladjustedScore_minus_avg_CSxOut.txt_irAE_1.txt'

celltype='em4'



indf=pd.read_csv(infile,sep="\t",index_col=0)


indf.head()


# In[2]:


#indf.boxplot(by =celltype+"_real", column =[celltype], grid = False)


# In[3]:


sns.boxplot(x = celltype+"_real", y = celltype, data = indf)
plt.savefig(infile+'_boxplot.pdf')

