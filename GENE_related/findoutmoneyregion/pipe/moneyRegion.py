#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import sys
infile=sys.argv[1] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/DMRrelated/diagnosis/genomic_feature_allwithheader/PBLtilMel_meldiff-.7_other-.1_q0.00001_sorted4_1_genomic_feature_bilge_celltypeseperated/MEL_TUMOR/promdataready_all_matrixCin_nr0.5_imputed_g1_MEL_TUMOR_3_g2_others_15.txt_q0.01_diff0.7_hypo.txt_intron_genecode_v36_modified.txt_canonical.txt_proteinCodingGene.txt_method1.txt.txt"

outfile=sys.argv[2]  #infile+".pdf"

indf=pd.read_csv(infile,sep="\t")

diffcol='diff' #'maxCompartmentwisedelta'


diffrange=[-.1,-.3,-.5,-.7,-0.8,-0.85,-.9]


indf.head()


# In[2]:


set(indf['direction'].tolist())


# In[3]:


indfposdirection=indf[indf['direction']=='+']
indfnegdirection=indf[indf['direction']=='-']


# In[4]:


#indfposdirection['transcriptno'].plot.kde()


# In[5]:


indfposdirection.shape


# In[6]:


fig, ax = plt.subplots()
indfposdirection['transcriptno'].value_counts().plot(ax=ax, kind='bar')


# In[7]:


fig, ax = plt.subplots(2, len(diffrange), figsize=(10*len(diffrange), 10*2))

for i in range(len(diffrange)):
    indfposdirection_new = indfposdirection[indfposdirection[diffcol] < diffrange[i]]
    if len(indfposdirection_new) != 0:
        indfposdirection_new['transcriptno'].value_counts().plot(ax=ax[0][i], kind='bar')
    ax[0][i].set_title(diffcol + ' = ' + str(diffrange[i]))
    if i == 0:
        ax[0][i].set_ylabel('Positive Direction', fontsize=20)
    
for i in range(len(diffrange)):
    indfnegdirection_new = indfnegdirection[indfnegdirection[diffcol] < diffrange[i]]
    if len(indfnegdirection_new) != 0:
        indfnegdirection_new['transcriptno'].value_counts().plot(ax=ax[1][i], kind='bar')
    ax[1][i].set_title(diffcol + ' = ' + str(diffrange[i]))
    if i == 0:
        ax[1][i].set_ylabel('Negative Direction', fontsize=20)


# In[8]:


fig.savefig(outfile, dpi=300, bbox_inches='tight')


# In[ ]:




