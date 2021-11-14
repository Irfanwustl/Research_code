#!/usr/bin/env python
# coding: utf-8

# In[1]:


###worksfor hypo only as calculated for 'confidence' 

import pandas as pd
from statistics import mean
import time
import numpy as np
from collections import defaultdict
import sys





smfile=sys.argv[1] #'/Users/irffanalahi/Research/Research_code/gitignorefolder/MHB_per_read/softreadcounting/testtheidea/try2/BL14_all_matrixCin_nr0.4_imputed_rowmean.txt_bg_intesectedwith_CD4DMRofBL14atleast.2SM_g1_CD4_3_g2_others_33_addedcol.txt'
finalfile=sys.argv[2] #'/Users/irffanalahi/Research/Research_code/gitignorefolder/MHB_per_read/softreadcounting/testtheidea/try2/CD4allrange_NR_1000000_insilmix60_sorted_howsm_single_mode_pp_masterdf.txt_rej-99999.0_mincpg1_rejmode_nov_final.txt'
outfile=sys.argv[3]

smdf=pd.read_csv(smfile,sep="\t",index_col=['chrom','start','end'])
finaldf=pd.read_csv(finalfile,sep="\t")
celltype=sys.argv[4]  #'CD4'
deltagreaterforpositive=float(sys.argv[5])  #0  ##############>0

allct=['CD4','CD8','nB','NK','Mn','mNeu','m8','DC','Eo','Tr','m4','Mg','Er','mB']

smdf.head()


# In[2]:


set(finaldf['finalrejectedfor'].tolist())


# In[3]:


finaldf=finaldf[(finaldf['finalacceptedfor']==celltype) | (finaldf['finalrejectedfor'].str.contains(celltype))]


# In[4]:


preveresult=finaldf[finaldf['finalacceptedfor']==celltype].shape[0]/finaldf.shape[0]
preveresult


# In[5]:


finaldf.shape


# In[6]:


finaldf.to_csv(outfile+"_informative.txt",sep="\t",index=False)


# In[7]:


finaldf.head()


# In[8]:


finaldf['acceptedCpG']=finaldf.acceptedCpG.apply(lambda x: x[1:-1].split(','))
finaldf['notacceptedCpG']=finaldf.notacceptedCpG.apply(lambda x: x[1:-1].split(','))
finaldf['mismatchCpG']=finaldf.mismatchCpG.apply(lambda x: x[1:-1].split(','))


# In[9]:







finaldf['#CpG']=-1

finaldf['deltabasedfragassignment']='NotAssigned'



# In[10]:


for ct in allct:
    finaldf[ct]='NotAssigned'
    #finaldf[ct+"_CW"]='NotAssigned'
finaldf.head()


# In[11]:


def processrowhelper(cpglist_fromprocessrow):
    
    indexlist=[]
    for cpg in cpglist_fromprocessrow:
        if not eval(cpg):
            continue
        
        chrom,start=eval(cpg).split(':')
        indexlist.append((chrom,int(start),int(start)+2))
    
     

    
    return indexlist


    
def deltacalculation(cpgsfordelta):
    
    ctwiseScore = defaultdict(list)
    for ct in allct:
        if ct==celltype:
            
           
            ctwiseScore[ct].append((cpgsfordelta.mean(axis=1)).sum())
           

        else:
            
    
            celltyperelatedcol=celltype+'-'+ct
            othercol=cpgsfordelta.columns.tolist()
            othercol.remove(celltyperelatedcol)
            
            otherctdf=cpgsfordelta[othercol]
            
            currentctdf=(cpgsfordelta[celltyperelatedcol]).to_frame(name=celltyperelatedcol)
            
            
  
            
            temp=otherctdf-currentctdf.values
            
            
            
            tempsum=(temp.mean(axis=1)).sum()
         
            
            ctwiseScore[ct].append(tempsum)
            
            
    ctwisescoredf=pd.DataFrame(ctwiseScore)
    return ctwisescoredf
        


def processrow(aindex,arow):
   
    notacceptedCpGList=arow['notacceptedCpG']
    acceptedCpGList=arow['acceptedCpG']
    
    
    
    
    accindex=processrowhelper(acceptedCpGList)
    
    
    ACCscore=pd.DataFrame(0,index=[0],columns=allct)
    
    
    
    if len(accindex)>0:
        corresACCcpgs=(smdf.loc[accindex])*-1 
        ACCscore=deltacalculation(corresACCcpgs)
    

  
    
    rejindex=processrowhelper(notacceptedCpGList)
    
    REJscore=pd.DataFrame(0,index=[0],columns=allct)
    
    
    
    if len(rejindex)>0:
        corresREJcpgs=smdf.loc[rejindex]
        
        REJscore=deltacalculation(corresREJcpgs)
    

    
    finalscore=ACCscore+REJscore
    if finalscore.shape[0]!=1:
        print('something wrong')
        sys.exit(1)
    
    finaldf.loc[index,allct]=finalscore.iloc[0]
 
    
    totalcpgs=len(accindex)+len(rejindex)
    
    finaldf.loc[index,'#CpG']=totalcpgs
    
    


# In[12]:


smdfcols=smdf.columns.tolist()
smdf=smdf[smdfcols[smdfcols.index('DMRname')+1:smdfcols.index('maxCompartmentwisedelta')]]
smdf.head()


# In[13]:


for index, row in finaldf.iterrows():
    

    processrow(index, row)
   
    
    


# In[14]:


finaldf['maxscoredCT']=(finaldf[allct].astype(float)).idxmax(axis=1)
finaldf.head()


# In[15]:


finaldf.to_csv(outfile+"_softRD.txt",sep="\t",index=False)


# In[16]:


finaldf=finaldf[finaldf['#CpG']>0]

finaldf.loc[finaldf[celltype]>deltagreaterforpositive,'deltabasedfragassignment']=finaldf.loc[finaldf[celltype]>deltagreaterforpositive,'maxscoredCT']

finaldf.loc[finaldf[celltype]<=deltagreaterforpositive,'deltabasedfragassignment']='Rejeceted'+'_'+celltype



# In[17]:


allacceptedDelta=finaldf.loc[finaldf['deltabasedfragassignment']==celltype,celltype].sum()
rejectedalldelta=finaldf.loc[finaldf['deltabasedfragassignment']=='Rejeceted'+'_'+celltype,celltype].sum()
deltabasedresult=allacceptedDelta/(allacceptedDelta+abs(rejectedalldelta))


# In[18]:


allaccfrag=finaldf[finaldf['deltabasedfragassignment']==celltype].shape[0]
allrejfrag=finaldf[finaldf['deltabasedfragassignment']=='Rejeceted'+'_'+celltype].shape[0]
fragresult=allaccfrag/(allaccfrag+allrejfrag)


# In[19]:


allacccpgnumber=finaldf.loc[finaldf['deltabasedfragassignment']==celltype,"#CpG"].sum()
allREJcpgnumber=finaldf.loc[finaldf['deltabasedfragassignment']=='Rejeceted'+'_'+celltype,"#CpG"].sum()

cpgweightedresult=allacccpgnumber/(allacccpgnumber+allREJcpgnumber)


# In[20]:


deltaweightedbycpgResult=allacceptedDelta/(allacccpgnumber+allREJcpgnumber)


# In[21]:


resultdf=pd.DataFrame({'deltabasedresult':[deltabasedresult],'deltaweightedbycpgResult':[deltaweightedbycpgResult],'fragresult':[fragresult],'cpgweightedFRAGresult':cpgweightedresult})
resultdf.to_csv(outfile+"_softRD_result.txt",sep="\t",index=False)


# In[22]:


finaldf.to_csv(outfile+"_softRDnozeroCpG.txt",sep="\t",index=False)



