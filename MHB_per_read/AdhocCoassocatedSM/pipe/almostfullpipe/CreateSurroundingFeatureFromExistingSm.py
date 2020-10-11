#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:

import sys
smfile=sys.argv[1] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/MHB_per_read/moretest/create_surrounding_feature/data/blleuko450kg50_hypo.txt"#"/Users/irffanalahi/Research/weekly/for_10_8_20/my/adhocSM/OnlyWGBSList/smbluWGBSCD4CD8g50_hypo.txt"
radius=int(sys.argv[2]) #150

outname=sys.argv[3] #smfile+"_radius_"+str(radius)+"bp.txt"
smdf=pd.read_csv(smfile,sep="\t")
smdf.head()


# In[3]:


result=[]
for cpg in smdf.iloc[:, 0]:
    chrom,pos=cpg.split(":")
    start=int(pos)-radius
    end=int(pos)+radius
    
    tempdict={"chrom":chrom,"start":start,"end":end}
    
    result.append(tempdict)
    


# In[4]:


outdf=pd.DataFrame(result)
outdf.head()


# In[5]:


outdf.to_csv(outname,sep="\t",header=False,index=False)
#print("done")

