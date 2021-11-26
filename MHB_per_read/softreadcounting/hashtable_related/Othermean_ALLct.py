#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import re

import sys

import time
start_time = time.time()


biggerfile=sys.argv[1] #'/Users/irffanalahi/Research/Research_code/gitignorefolder/MHB_per_read/softreadcounting/testtheidea/veryefficient/BL14_all_matrixCin_nr0.4_imputed_rowmean.txt_bg_intesectedwith_BL14mNeuDMRs_CW.7.txt'
phenfile=sys.argv[2] #'/Users/irffanalahi/Research/Research_code/gitignorefolder/MHB_per_read/softreadcounting/testtheidea/try2/preparesm/BL14_PhenoClass.txt'
outfile=biggerfile+"_othermean.txt"
newcolnames=[]
biggerdf=pd.read_csv(biggerfile,sep="\t",header=None,skiprows=1)
pheno=pd.read_csv(phenfile,sep="\t", header=None, index_col=0)
biggerdf.head()


# In[2]:


with open (biggerfile) as f:
    line=f.readline()
    line=line.split("\n")
    colnames=line[0].split("\t")


# In[3]:


totalcols=colnames+newcolnames


# In[4]:


biggerdf.columns=totalcols


biggerdf=biggerdf.set_index(['chrom','start','end'])
biggerdf.head()


# In[5]:


allct=pheno.index.tolist()
allct


# In[6]:


biggerdf=biggerdf[allct]
biggerdf.head()


# In[7]:



deltacols=[]
for ct in allct:


    restct=allct.copy()
    restct.remove(ct)
    
    if len(restct)!=len(allct)-1:
        print("problem")
        sys.exit(1)
    
    
    
    tempcol=ct+"-others"
    
    deltacols.append(tempcol)
    biggerdf[tempcol]=biggerdf[ct]-biggerdf[restct].mean(axis=1)


# In[8]:


biggerdf=biggerdf[deltacols]

biggerdf.to_csv(outfile+"_withend.txt",sep="\t")


biggerdf=biggerdf.reset_index()
biggerdf.head()


# In[9]:


biggerdf=biggerdf.drop(['end'],axis=1)
biggerdf.head()





# In[10]:



biggerdf=biggerdf.set_index(['chrom','start'])




# In[11]:


dup=biggerdf[biggerdf.index.duplicated()]
if dup.shape[0]!=0:
    print(dup)
    print('dup why??')
    


# In[12]:


biggerdf.to_csv(outfile,sep="\t")



end_time = time.time()

time_elapsed = (end_time - start_time)

print(time_elapsed)



