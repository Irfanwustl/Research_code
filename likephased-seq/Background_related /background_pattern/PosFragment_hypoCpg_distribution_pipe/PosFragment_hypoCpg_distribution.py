#!/usr/bin/env python
# coding: utf-8

# In[1]:



import glob
import pandas as pd
from collections import Counter
from statistics import mean
import sys



infolder=sys.argv[1] #"/Users/irffanalahi/Research/Research_update/in-silico/background_pattern/readnumber_1000000/mincpg3/somefinalfiles"
allfiles=glob.glob(infolder+"/*.txt")
celltype='mNeu'
outfile=infolder+"_acceptedCpG_length"


# In[2]:


def adjustrowlength(arow,colname,cloname_length):
    new_length=arow[cloname_length]

    if arow[cloname_length]==1 and eval(arow[colname][0])=="":
     
        new_length= 0
    return new_length


# In[3]:



TPdflist=[]
FPdflist=[]


for infile in allfiles:
    indf=pd.read_csv(infile,sep="\t")
    indf['acceptedCpG']=indf.acceptedCpG.apply(lambda x: x[1:-1].split(','))
    indf['notacceptedCpG']=indf.notacceptedCpG.apply(lambda x: x[1:-1].split(','))
    indf['mismatchCpG']=indf.mismatchCpG.apply(lambda x: x[1:-1].split(','))
    
    indf['acceptedCpG_length']=indf['acceptedCpG'].str.len()
    indf['notacceptedCpG_length']=indf['notacceptedCpG'].str.len()
    indf['mismatchCpG_length']=indf['mismatchCpG'].str.len()
    
    
    accepteddf=(indf[indf['finalacceptedfor']==celltype]).copy()
    
    
    
    for index, nrow in accepteddf.iterrows():
        correctedacceptedCpGlength=adjustrowlength(nrow,'acceptedCpG','acceptedCpG_length')
        correctednotacceptedCpG_length=adjustrowlength(nrow,'notacceptedCpG','notacceptedCpG_length')
        correctedmismatchCpG_length=adjustrowlength(nrow,'mismatchCpG','mismatchCpG_length')
        
        accepteddf.loc[index,'acceptedCpG_length']=correctedacceptedCpGlength
        accepteddf.loc[index,'notacceptedCpG_length']=correctednotacceptedCpG_length
        accepteddf.loc[index,'mismatchCpG_length']=correctedmismatchCpG_length
        
    
    
    TPdf=accepteddf[accepteddf['ReadName'].str.contains(celltype)]

    FPdf=accepteddf[~accepteddf['ReadName'].str.contains(celltype)]
    
    
    TPdflist.append(TPdf)
    FPdflist.append(FPdf)
    

    


# In[4]:


outTPdf=pd.concat(TPdflist)
outFPdf=pd.concat(FPdflist)



# In[5]:


#outTPdf['acceptedCpG_length'].plot.kde()


# In[6]:


#outFPdf['acceptedCpG_length'].plot.kde()


# In[7]:


#print(outTPdf.shape)
#print(outFPdf.shape)


# In[8]:


outTPdf.to_csv(outfile+"_TP.txt",sep="\t",index=False)
outFPdf.to_csv(outfile+"_FP.txt",sep="\t",index=False)

outFPdf_sample=outFPdf.sample(n=outTPdf.shape[0])


outFPdf_sample.to_csv(outfile+"_FP_downsampled.txt",sep="\t",index=False)


# In[9]:


import seaborn as sns
import matplotlib.pyplot as plt


fig2 = plt.figure()


sns.kdeplot(outTPdf['acceptedCpG_length'],label='TP_fragment', shade=True,color='green')
sns.kdeplot(outFPdf_sample['acceptedCpG_length'],label='FP_fragment', shade=True,color='red')

fig2.savefig(outfile+'FPsowsampled_kde.pdf',dpi=300, bbox_inches='tight')

plt.close(fig2)




fig = plt.figure()


sns.kdeplot(outTPdf['acceptedCpG_length'],label='TP_fragment', shade=True,color='green')
sns.kdeplot(outFPdf['acceptedCpG_length'],label='FP_fragment', shade=True,color='red')

fig.savefig(outfile+'_kde.pdf',dpi=300, bbox_inches='tight')

plt.close(fig)





# In[12]:

'''
outTPdf['acceptedCpG_length'].hist()


# In[11]:


outFPdf['acceptedCpG_length'].hist()


# In[14]:


plt.hist(outTPdf['acceptedCpG_length'], alpha=0.5, label='TP_fragment')
plt.hist(outFPdf['acceptedCpG_length'], alpha=0.5, label='FP_fragment')
plt.legend(loc='upper right')


# In[ ]:
'''




