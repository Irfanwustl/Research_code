#!/usr/bin/env python
# coding: utf-8

# In[1]:


from scipy.stats import pearsonr
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
#get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:

import sys
filename=sys.argv[1] #"/Users/irffanalahi/Research/weekly/for_10_15_20/friday_morning/Analysis/codedevelop/corr/plot/atleast2cpg.txt_ABSreadcount_divisionedNormalized.txt_CSxOut.txt_bulk_pbmc_gt_scaled.txt_onefile"

df=pd.read_csv(filename,sep="\t")

x=  'ground_truth'
y='predicted'
celltype="celltype" #"Cell Type" #"celltype"



xyfixed_lim=False

only_scatter=False


# In[3]:


##### beautification ####
if celltype=="celltype":
    df=df.rename(columns = {"celltype":"Cell Type"})
    celltype="Cell Type"

if x== "ground_truth":
    df=df.rename(columns = {"ground_truth":"Ground Truth"})
    x="Ground Truth"
if y== 'predicted':
    df=df.rename(columns = {"predicted":"Predicted"})
    y="Predicted"
    

####df[celltype] = df[celltype].replace(['CD1hgcc9'],'B Chcxell') #### to test the following will be ignored if there is no such cell type

df[celltype] = df[celltype].replace(['CD4'],'CD4 T')
df[celltype] = df[celltype].replace(['CD8'],'CD8 T')
df[celltype] = df[celltype].replace(['CD14'],'Mono')
df[celltype] = df[celltype].replace(['CD19'],'B Cell')





# In[4]:


df.corr()


# In[5]:


corr = pearsonr(df[x], df[y])

#corr = [np.round(c, 5) for c in corr]
#print(corr)
text='r = %s \nP = %s' % (format(corr[0], '.3f'), format(corr[1], ".3e") )


# In[6]:


sns.set(style="ticks",font_scale=1.5)
if xyfixed_lim==True:
    plt.xlim([0, 0.8])
    plt.ylim([0, 0.8])

g=sns.scatterplot(df[x], df[y],hue=df[celltype],edgecolor='none')
g.legend(loc='center left', bbox_to_anchor=(1.02, 0.5), ncol=1)

if only_scatter==False:
    ax=sns.regplot(df[x], df[y],scatter=False)




    anc = AnchoredText(text, loc="upper left", frameon=False,prop=dict(fontstyle="italic"))
    ax.add_artist(anc)


#default 12
plt.rcParams["axes.labelsize"] = 14
plt.rcParams['font.family']='sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']




#hfont = {'fontname':'Helvetica'}
#plt.title('title',**hfont)

savename=filename+"_"+x+"_"+y+".pdf"
plt.savefig(savename,dpi=300,bbox_inches="tight")
#plt.show()
#sns.jointplot(data=df, x=x, y=y, kind='reg', hue=df[celltype])

