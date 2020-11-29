#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from collections import defaultdict
import sys


# In[2]:


finalfile=sys.argv[1] #"/Users/irffanalahi/Research/weekly/for_11_18_20/adjust_ref/afteradjustingref/downstream/abs/fidelity_test/sm1002adjusted/BULK-PBMC-1389.bg_howsm_single_mode_pp_masterdf.txt_rej-99999.0_mincpg3_rejmode_nov_final.txt"
sm=sys.argv[2] #"/Users/irffanalahi/Research/weekly/for_11_18_20/adjust_ref/afteradjustingref/downstream/abs/fidelity_test/sm1002adjusted/blwithneu_hypo_stat.txt_0.01_2_g100.txtWithSurrounding.txt_1cpgnc.txt_twoadjusted.txt"
#celllist=["'CD14'","'CD19'","'CD4'","'CD8'","'CD56'","'Neu'","'EPCAM'"] 

finaldf=pd.read_csv(finalfile,sep="\t")
finaldf['acceptedCpG'] = finaldf.acceptedCpG.apply(lambda x: x[1:-1].split(','))
finaldf['CheckedCpG'] = finaldf.CheckedCpG.apply(lambda x: x[1:-1].split(','))

smdf=pd.read_csv(sm,sep="\t")
smdf['celltype']=smdf.celltype.apply(lambda x: x[1:-1].split(','))
finaldf.head()


# In[3]:


smdf.head()


# In[4]:


celllist=(smdf['celltype']).tolist()
celllist=[x for sublist in celllist for x in sublist]
celllist=list(set(celllist))
print(celllist)


# In[5]:


def countacccpg(sdf,df,cells):
    out={}
    for cell in cells:
        celldf=df[df['finalacceptedfor']==cell]
        
        correscpg=(celldf['acceptedCpG']).tolist()
        
        correscpg = [x for sublist in correscpg for x in sublist]
        
        correscpg = [i for i in correscpg if i] 
        
        correscpg=list(map(eval,correscpg))
        
        correscpgunique=list(set(correscpg))
        uniquelen=len(correscpgunique)
        
        #print(cell)
        #print(correscpgunique)
       
        out[cell]=uniquelen
    return out
    


# In[6]:


def countcheckedCpG(sdf,df):
    allcheckedCpG=df['CheckedCpG']
    allcheckedCpG = [x for sublist in allcheckedCpG for x in sublist]
    allcheckedCpG=[i for i in allcheckedCpG if i] 
    allcheckedCpG=list(map(eval,allcheckedCpG))
   
    allcheckedCpG=list(set(allcheckedCpG))
   


    outdict=defaultdict(list)

    for cpg in allcheckedCpG:
        chrom,start=cpg.split(":")
        
        
        fromsm=sdf[(sdf['chrom']==chrom) & (sdf['start']==int(start))]
        if fromsm.shape[0]!=1:
            print("error. Exiting")
            sys.exit(1)
        
        celltype=fromsm['celltype']
        celltype=[x for sublist in celltype for x in sublist]
        if len(celltype)!=1:
            print("wrong.Exiting")
            sys.exit(1)
        outdict[celltype[0]].append(cpg)
        
    
    outdict=dict(outdict)
    outdictlen={}
    
    for k in outdict:
        outdictlen[k]=len(outdict[k])
    
    return outdictlen
    
    
        


# In[7]:


acccpg=countacccpg(smdf,finaldf,celllist)

with open(finalfile+"_acccpgCount.txt", 'w') as f:
    print(acccpg, file=f)

print(acccpg)


# In[8]:


checkedcpg=countcheckedCpG(smdf,finaldf)

with open(finalfile+"_checkedcpgCount.txt", 'w') as f:
    print(checkedcpg, file=f)

print(checkedcpg)

