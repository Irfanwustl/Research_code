#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

import sys

import ast
from collections import defaultdict 


# In[2]:


def generateSummary(allmatgdf,sdict,outfilename):
    
   
    geneWiseGroup=allmatgdf.groupby(allmatgdf.iloc[:,-1])
    
    dflist=[]
    for celltype in sdict: 
 
        currentcol=intersection(allmatgdf.columns,sdict[celltype])
        
        temp=geneWiseGroup[currentcol].mean().mean(axis=1)
        
        tempdf=temp.to_frame()
        tempdf.index.name = "Gene"
        tempdf.columns =[celltype]
        
        dflist.append(tempdf)
        
       
        
    
    
    outdf=dflist[0]
    i=1 
    while i < len(dflist):
        outdf=pd.merge(outdf,dflist[i],left_index=True,right_index=True)
        i=i+1
    
    outdf.to_csv(outfilename,sep="\t")
   
    
   


# In[3]:


def group_dict(indict):
     
    # Grouping dictionary keys by value 
    res = defaultdict(list) 
    for key, val in sorted(indict.items()): 
        res[val].append(key) 
    return dict(res)
    # printing result  
    


# In[4]:


def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 


# In[5]:


allmatwithgene=sys.argv[1]


corresdict=sys.argv[2]

outfile=sys.argv[3]


allmatwithgenedf=pd.read_csv(allmatwithgene,sep="\t")



file = open(corresdict, "r")
contents = file.read()
smdict = ast.literal_eval(contents)

groupedDict=group_dict(smdict)



generateSummary(allmatwithgenedf,groupedDict,outfile)

