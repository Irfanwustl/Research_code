#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import pandas as pd
from collections import defaultdict
from sklearn import metrics
import numpy as np
import sys
import time
import os

start_time = time.time()

inbinfile=sys.argv[1] #'/Users/irffanalahi/Research/Research_update/SoftRD/reproduce_goodmelresult_withHardRC_new_implementation/AUC1fullcohort/BL22_TILAUC1_dummyfull.txt_result_dupindex_binnedstats.pkl'




outfile=sys.argv[2]


#######outfile=inbinfile


mincpgLIST=[1,2,3]

consideringALLheyper=True


inbindf=pd.read_pickle(inbinfile)



#scorecolumns=['CD4-others','CD8-others','nB-others','NK-others','Mn-others','mNeu-others','m8-others','DC-others','Eo-others','Tr-others','m4-others','Mg-others','Er-others','mB-others']


#13ctref
#scorecolumns=['CD4-others','CD8-others','nB-others','NK-others','PC-others','Mn-others','iDC-others','mDC-others','M1-others','M0-others','mN-others','M2-others','cB-others']


#BL22LTME
#scorecolumns=['NaiveCD4-others','NaiveCD8-others','nB-others','NK-others','PC-others','Mono-others','M0-others','M1-others','M2-others','iDC-others','mDC-others','PMN-others','cm8-others','em8-others','Eo-others','Tregs-others','em4-others','ed8-others','Mg-others','cm4-others','Er-others','mB-others','TIL-others','MelTumor-others']

#CD8TIL_mel_naiveMylid_activated
#scorecolumns=['CD8TIL-others','MelTumor-others','activated-others','NaiveMyloid-others']

#old 3 compartment LTME good SM
#scorecolumns=['PBL-others','TIL-others','MEL_TUMOR-others']


#em4_cm4
scorecolumns=['cm4-others','em4-others','Tcell-others']



inbindf=inbindf.reset_index()
inbindf.head()


# In[2]:


if consideringALLheyper==True:
    allassigned=inbindf.copy()


elif consideringALLheyper==False:
    allassigned=inbindf[inbindf['deltabasedfragassignment']!='NotAssigned'].copy()
    
else:
    print("wrong input")
    sys.exit(1)
#
allassigned.head()


# In[3]:


allassigned.loc[inbindf['deltabasedfragassignment']=='NotAssigned','deltabasedfragassignment']=allassigned.loc[inbindf['deltabasedfragassignment']=='NotAssigned','maxscoredCT_beforeCpGweight']


# In[4]:


allassigned['secondmaxScore']='Notassigned'
allassigned['secondmaxScoreCT']='Notassigned'
allassigned.head()


# In[5]:


grouped=allassigned.groupby('maxscoredCT')

for name, group in grouped:
    
    
    tempscorecolumns=scorecolumns.copy()
    
    tempscorecolumns.remove(name)
    
    allassigned.loc[group.index,'secondmaxScore']=group[tempscorecolumns].max(axis=1)
    allassigned.loc[group.index,'secondmaxScoreCT']=(group[tempscorecolumns]).idxmax(axis=1)


# In[6]:


allassigned['adjustedScore_minus']=allassigned['maxscore']-allassigned['secondmaxScore']
allassigned['adjustedScore_minus_avg']=(allassigned['maxscore']+(allassigned['maxscore']-allassigned['secondmaxScore']))/2
allassigned.head()


# In[7]:


allassigned.columns


# In[8]:


adjustedScore_minus0val=list(set(allassigned[allassigned['LENhypoCpG_BY_total_cpg']==0]['adjustedScore_minus'].tolist()))
if len(adjustedScore_minus0val)==0:
    pass
elif len(adjustedScore_minus0val)!=1 or adjustedScore_minus0val[0]!=0:
    print(adjustedScore_minus0val)
    sys.exit(1)
    


# In[9]:


adjustedScore_minus_avg0val=list(set(allassigned[allassigned['LENhypoCpG_BY_total_cpg']==0]['adjustedScore_minus_avg'].tolist()))


if len(adjustedScore_minus_avg0val)==0:
    pass

elif len(adjustedScore_minus_avg0val)!=1 or adjustedScore_minus_avg0val[0]!=0:
    print(adjustedScore_minus_avg0val)
    sys.exit(1)
    


# In[10]:


allassigned['LENhypoCpG_0.8']=0
allassigned.loc[allassigned['LENhypoCpG_BY_total_cpg']>=0.8,'LENhypoCpG_0.8']=allassigned.loc[allassigned['LENhypoCpG_BY_total_cpg']>=0.8,'LENhypoCpG']


# In[11]:


allassigned['LENhypoCpG_0.65']=0
allassigned.loc[allassigned['LENhypoCpG_BY_total_cpg']>=0.65,'LENhypoCpG_0.65']=allassigned.loc[allassigned['LENhypoCpG_BY_total_cpg']>=0.65,'LENhypoCpG']


# In[12]:


allassigned['LENhypoCpG_0.5']=0
allassigned.loc[allassigned['LENhypoCpG_BY_total_cpg']>=0.5,'LENhypoCpG_0.5']=allassigned.loc[allassigned['LENhypoCpG_BY_total_cpg']>=0.5,'LENhypoCpG']


# In[13]:


allassigned.head()


# In[14]:




def softRC (fgrouped,targetmincpg,cpgpatternratecolumn,fname,whichmethod):
    
    
    ctposscoredict= defaultdict(list)
    cttotalfragment=defaultdict(list)

    for score in scorecolumns:
        deltabasedfragassigned=fgrouped['deltabasedfragassignment'].tolist()
        if score in deltabasedfragassigned:

            #temp_posscore=fgrouped.loc[fgrouped['deltabasedfragassignment']==score,whichmethod].tolist()
            #positivefragments=fgrouped[(fgrouped['deltabasedfragassignment']==score) & (fgrouped[cpgpatternratecolumn]>=targetmincpg)].shape[0]


            totalfragments=fgrouped[(fgrouped['deltabasedfragassignment']==score) & (fgrouped['total_cpg']>=targetmincpg)].shape[0]

            temp_posscore=fgrouped.loc[(fgrouped['deltabasedfragassignment']==score) & (fgrouped[cpgpatternratecolumn]>=targetmincpg),whichmethod].tolist()

            temptotal_posscore=sum(temp_posscore)

        else:
            temptotal_posscore=0
            totalfragments=0


        ctname=score.replace('-others','')
        ctposscoredict[ctname].append(temptotal_posscore)
        cttotalfragment[ctname].append(totalfragments)

    ctposscoredf=pd.DataFrame.from_dict(ctposscoredict)
    ctposscoredf['Mixture']=fname

    cttotalfragmentDF=pd.DataFrame.from_dict(cttotalfragment)
    cttotalfragmentDF['Mixture']=fname



    return ctposscoredf,cttotalfragmentDF

    
  


# In[15]:


filegrouped=allassigned.groupby('filename')



for mincpg in mincpgLIST:
    allfileresultnopercent=[]
    
    allfileresultfiftypercent=[]

    allfileTOTActfragnopercent=[]
    allfileTOTActfragfiftypercent=[]
    
    
    for name, group in filegrouped:

        r1,r2=softRC(group,mincpg,'LENhypoCpG',name,'adjustedScore_minus_avg')

        allfileresultnopercent.append(r1)
        allfileTOTActfragnopercent.append(r2)



        r1,r2=softRC(group,mincpg,'LENhypoCpG_0.5',name,'adjustedScore_minus_avg')

        allfileresultfiftypercent.append(r1)
        allfileTOTActfragfiftypercent.append(r2)


        
        
        
     

    

    allfileresultnopercentDF=pd.concat(allfileresultnopercent)
    allfileresultnopercentDF.set_index('Mixture',inplace=True) 


    allfileresultfiftypercentDF=pd.concat(allfileresultfiftypercent)
    allfileresultfiftypercentDF.set_index('Mixture',inplace=True) 


    allfileTOTActfragnopercentDF=pd.concat(allfileTOTActfragnopercent)
    allfileTOTActfragfiftypercentDF=pd.concat(allfileTOTActfragfiftypercent)

    allfileTOTActfragnopercentDF.set_index('Mixture',inplace=True) 
    allfileTOTActfragfiftypercentDF.set_index('Mixture',inplace=True) 

    allfileTOTActfragnopercentDF.to_csv(outfile+"_NOpat"+"_cg"+str(mincpg)+"_totalctfrag.txt",sep="\t",na_rep='NA')      #####should be same as fifty percent
    allfileTOTActfragfiftypercentDF.to_csv(outfile+"_pat"+".5_cg"+str(mincpg)+"_totalctfrag.txt",sep="\t",na_rep='NA')



    
    
    
    

    allfileresultnopercentDF.to_csv(outfile+"_NOpat"+"_cg"+str(mincpg)+"_CSxOut.txt",sep="\t",na_rep='NA')
    
    allfileresultfiftypercentDF.to_csv(outfile+"_pat"+".5_cg"+str(mincpg)+"_CSxOut.txt",sep="\t",na_rep='NA')


    ###### we can also divide here###################



    divbyctfragnopercent=allfileresultnopercentDF/allfileTOTActfragnopercentDF

    divbyctfragfiftypercent=allfileresultfiftypercentDF/allfileTOTActfragfiftypercentDF


    divbyctfragnopercent.to_csv(outfile+"_NOpat"+"_cg"+str(mincpg)+"_divbyctfrag_CSxOut.txt",sep="\t",na_rep='NA')
    divbyctfragfiftypercent.to_csv(outfile+"_pat"+".5_cg"+str(mincpg)+"_divbyctfrag_CSxOut.txt",sep="\t",na_rep='NA')

    
    



#########output final pkl########
allassigned.to_pickle(outfile+"_FINAL_binnedstats.pkl")


# In[16]:


end_time = time.time()

time_elapsed = (end_time - start_time)

#print(time_elapsed)

