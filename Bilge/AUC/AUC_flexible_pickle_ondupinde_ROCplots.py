#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from collections import defaultdict
from sklearn import metrics
import numpy as np
import sys
import time
import matplotlib.pyplot as plt


start_time = time.time()

inbinfile=sys.argv[1] #'/Users/irffanalahi/Research/Research_code/gitignorefolder/MHB_per_read/softreadcounting/testtheidea/softRD_pileup/CD4mixture_output_81205_sorted_softMultiprocessing_binnedstats.pkl'

outfile=inbinfile


consideringALLheyper=True


inbindf=pd.read_pickle(inbinfile)



###BL22###
scorecolumns=['NaiveCD4-others','cm4-others','em4-others','Tregs-others','NaiveCD8-others','cm8-others','em8-others','ed8-others','nB-others','mB-others','NK-others','PC-others','Mono-others','Eo-others','M0-others','M1-others','M2-others','iDC-others','mDC-others','PMN-others','Mg-others','Er-others']


###BL14###
#scorecolumns=['CD4-others','CD8-others','nB-others','NK-others','Mn-others','mNeu-others','m8-others','DC-others','Eo-others','Tr-others','m4-others','Mg-others','Er-others','mB-others']

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


allassigned['LENhypoCpG_0.5']=0
allassigned.loc[allassigned['LENhypoCpG_BY_total_cpg']>=0.5,'LENhypoCpG_0.5']=allassigned.loc[allassigned['LENhypoCpG_BY_total_cpg']>=0.5,'LENhypoCpG']


# In[12]:

def renamect(act):
    if act=='CD4':
        return 'Naive CD4 T'
    if act=='CD8':
        return 'Naive CD8 T'

    if act=='NaiveCD4':
        return 'Naive CD4 T'
    if act=='NaiveCD8':
        return 'Naive CD8 T'
    if act=='Tr':
        return 'Tregs'
    if act=='mB':
        return 'Memory B'
    if act=='nB':
        return 'Naive B'
    if act=='m4':
        return 'Memory CD4 T'
    if act=='m8':
        return 'Memory CD8 T'
    if act=='Mn':
        return 'Monocytes'


    if act=='em8':
        return 'CD8 TEM'
    if act=='cm8':
        return 'CD8 TCM'

    if act=='em4':
        return 'CD4 TEM'
    if act=='cm4':
        return 'CD4 TCM'


    if act=='ed8':
        return 'CD8 TEMRA'

    if act=='PC':
        return 'Plasma'

    if act=='M0':
        return 'Macs_M0'

    if act=='M1':
        return 'Macs_M1'

    if act=='M2':
        return 'Macs_M2'
    if act=='Eo':
        return 'Eos'

    if act=='Mg':
        return 'MK'




    return act


colorlist=['khaki','darkgoldenrod',]

def calculate_metrics(currentgroup,currentmethods):
    pred_lst = []
    y_lst = []
    fpr_lst = []
    tpr_lst = []
    for name, group in currentgroup:
   
        celltype=name.replace('-others','')




        y=(group['index'].str.contains(celltype)).astype(int) 
        y_lst += list(y)

        for method in currentmethods:

            pred=(group[method]).to_numpy()
            pred_lst += list(pred)



            fpr, tpr, thresholds=metrics.roc_curve(y,pred,pos_label=1)
            fpr_lst.append(fpr)
            tpr_lst.append(tpr)


            tempAUC=metrics.auc(fpr, tpr)

          

            plt.plot(fpr,tpr,label=renamect(celltype)+', auc=%s' % (format(tempAUC, '.3f')),color='khaki')

            celltypeAUC[celltype]=celltypeAUC[celltype]+[tempAUC]

            optimal_idx = np.argmax(tpr - fpr)
            optimal_threshold = thresholds[optimal_idx]
            celltypeoptcutpoint[celltype]=celltypeoptcutpoint[celltype]+[optimal_threshold]
            
    
    fpr_mic, tpr_mic, _ = metrics.roc_curve(y_lst, pred_lst)
    roc_auc_mic = metrics.auc(fpr_mic, tpr_mic)
    plt.plot(fpr_mic,tpr_mic,label='Micro Average, auc=%s' % (format(roc_auc_mic, '.3f')), ls=':', lw = 3, c='r')
    all_fpr = np.unique(np.concatenate(fpr_lst))
    mean_tpr = np.zeros_like(all_fpr)
    for i in range(len(fpr_lst)):
        mean_tpr += np.interp(all_fpr, fpr_lst[i], tpr_lst[i])
        
    mean_tpr /= len(fpr_lst)
    roc_auc_mac = metrics.auc(all_fpr,mean_tpr)
    plt.plot(all_fpr,mean_tpr,label='Macro Average, auc=%s' % (format(roc_auc_mac, '.3f')), ls=':', lw = 3, c='b')
    plt.plot([0, 1], [0, 1], color="gray", linestyle="--")
    plt.legend(loc=(1.04,0))
    plt.savefig(outfile+"_Allheyper"+str(consideringALLheyper)+"_ROC.pdf",bbox_inches = "tight")

# In[13]:





celltypeAUC=defaultdict(list)
celltypeoptcutpoint=defaultdict(list)
allassignedgrouped=allassigned.groupby('deltabasedfragassignment')
new_groups = []
for name in scorecolumns:
    new_groups.append((name, allassignedgrouped.get_group(name)))

methods=['adjustedScore_minus_avg']

#methods=['maxscore','adjustedScore_minus','adjustedScore_minus_avg','LENhypoCpG','LENhypoCpG_0.5','LENhypoCpG_0.8']

calculate_metrics(new_groups,methods)



# In[14]:


celltypeAUCdf=pd.DataFrame.from_dict(celltypeAUC, orient='index',columns=methods)
celltypeAUCdf.index.name = 'Celltype'
celltypeAUCdf.head()


# In[15]:


celltypeoptcutpointdf=pd.DataFrame.from_dict(celltypeoptcutpoint, orient='index',columns=methods)
celltypeoptcutpointdf.index.name = 'Celltype'
celltypeoptcutpointdf.head()


# In[16]:


import seaborn as sns
import matplotlib.pyplot as plt
ax = sns.heatmap(celltypeAUCdf, annot=True,cmap='viridis')
plt.savefig(outfile+"_Allheyper"+str(consideringALLheyper)+"_AUC.pdf",bbox_inches = "tight")


# In[17]:


celltypeAUCdf.to_csv(outfile+"_Allhyper"+str(consideringALLheyper)+"_AUC.txt",sep="\t")
celltypeoptcutpointdf.to_csv(outfile+"_Allhyper"+str(consideringALLheyper)+"_Cutpoint.txt",sep="\t")


# In[18]:


end_time = time.time()

time_elapsed = (end_time - start_time)

print(time_elapsed)

