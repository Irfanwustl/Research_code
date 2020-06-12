#!/usr/bin/env python
# coding: utf-8

# In[1]:




import sys

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import ast
from sklearn.manifold import TSNE
import umap
import os.path


# In[2]:


import matplotlib as mpl


# In[3]:


dfname=sys.argv[1]#"all_matrix_intesectedwith_mdiff5_sorted_merged_only_cfd.txt_cyberin"#"CRC_and_healthy"#sys.argv[1]
outdir=sys.argv[2]
neddtotransposed=True #True/False
correspondingDict="CRC_Mel_and_healthy_dict.txt"#file with dict
whichdecomp="PCA" # PCA #tSNE #"UMAP"
CRC_tumor_ratio_dict="CRC_Mel_and_healthy_dict_crc_tumor_size_ratio.txt"


# In[4]:



############################# PCA ############################
def pca_comp(stdData):
	pca = PCA()
	principalComponents = pca.fit_transform(stdData)
	return principalComponents



####################tsne###############
def tsne_comp(stdData):
	tsne = TSNE(random_state=100)
	principalComponents = tsne.fit_transform(stdData)
	return principalComponents


####################umap###############
def umap_comp(stdData):
	um = umap.UMAP(random_state=100)
	principalComponents = um.fit_transform(stdData)
	return principalComponents


# In[5]:


import pandas as pd
pdData=pd.read_csv(dfname,sep="\t",index_col=0)
pdData



dfname=os.path.basename(dfname)
# In[6]:


if neddtotransposed==True:
    pdData=pdData.transpose()
    transfilename=outdir+"/"+dfname+"_transposed.txt"
    pdData.to_csv(transfilename,sep="\t",na_rep="NaN")


# In[7]:


file = open(correspondingDict, "r")
contents = file.read()
dictionary = ast.literal_eval(contents)

pdData["Target"] = pd.Series(dictionary)


# In[8]:


tumorratiofile = open(CRC_tumor_ratio_dict, "r")
content_tumorratio = tumorratiofile.read()
tumorratio_dictionary = ast.literal_eval(content_tumorratio)

pdData["TumorRatio"] = pd.Series(tumorratio_dictionary)


# In[9]:


#pdData


# In[10]:


pdData.loc[:, pdData.columns != "Target"]=pdData.groupby("Target").transform(lambda x: x.fillna(x.mean()))
#pdData


# In[11]:


Y=pdData["Target"].copy()
X=pdData.drop("Target",axis=1)
Xtumor=X["TumorRatio"].copy()
X=X.drop("TumorRatio",axis=1)

#X


# In[12]:


#Y


# In[13]:


#Xtumor


# In[14]:


from sklearn import preprocessing
label_changer = preprocessing.LabelEncoder()
Y_num=label_changer.fit_transform(Y)


# In[15]:


standardizedData= StandardScaler().fit_transform(X)


# In[16]:


standardizedData


# In[17]:


################# call decomposition ###########
if whichdecomp=="PCA":
	projected=pca_comp(standardizedData)
elif whichdecomp=="tSNE":
    projected=tsne_comp(standardizedData)
elif whichdecomp=="UMAP":
    projected=umap_comp(standardizedData)
else:
    print ("wrong reduction")


# In[18]:



############### draw ######################

import seaborn as sns; sns.set()
import numpy as np
import matplotlib.pyplot as plt
#get_ipython().run_line_magic('matplotlib', 'inline')
mpl.rcParams['figure.dpi']= 300

tumlist=Xtumor.tolist()
tumzz=[x*100 for x in tumlist]
tumzz=[x+10 for x in tumzz]

g=sns.scatterplot(x=projected[:, 0], y=projected[:, 1], hue=Y,edgecolor='none',size=tumzz)

g.legend(loc='center left', bbox_to_anchor=(1.02, 0.5), ncol=1)
plt.title(whichdecomp)

plt.xlabel('C1')
plt.ylabel('C2')


savename=outdir+"/"+dfname+"_"+whichdecomp+"_tumorratio.pdf"
plt.savefig(savename,dpi=300,bbox_inches="tight")



# In[19]:


mpl.rcParams['figure.dpi']= 300

#fig, ax = plt.subplots()
listttt=Xtumor.tolist()
zz=[x*100 for x in listttt]
zz=[x+10 for x in zz]
g=sns.scatterplot(x=projected[:, 0], y=projected[:, 1], hue=Y,edgecolor='none',size=zz)

g.legend(loc='center left', bbox_to_anchor=(1.25, 0.5), ncol=1)
plt.title(whichdecomp)

for i in range(projected[:, 0].shape[0]):
    
    g.text(projected[i, 0], projected[i, 1], X.index[i],fontsize=5)


plt.xlabel('C1')
plt.ylabel('C2')




savename_samplename=outdir+"/"+dfname+"_"+whichdecomp+"_tumorratio_sample_name.pdf"
plt.savefig(savename_samplename,dpi=300,bbox_inches="tight")






# In[20]:


'''

mpl.rcParams['figure.dpi']= 300
g=sns.scatterplot(x=projected[:, 0], y=projected[:, 1], hue=X.index,edgecolor='none')

g.legend(loc='center left', bbox_to_anchor=(1.25, 0.5), ncol=1)
plt.title(whichdecomp)

plt.xlabel('C1')
plt.ylabel('C2')
'''




