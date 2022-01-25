#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas  as  pd
import re
import sys
import seaborn as sns; sns.set()
#get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import time
start_time = time.time()

infile=sys.argv[1] #'/Users/irffanalahi/Research/Research_code/gitignorefolder/MHB_per_read/softreadcounting/downstream/hashtablestats/test_CD8TIL_cpgnumber.txt'

columnofinterest=sys.argv[2] #'CD8TIL'

####the pattern must be just upto the number####
heatxaxis='naiveMyloidPateintCD14_CD8TILCD8TIL_'
heatyaxis='activatedPatientTcell_CD8TILCD8TIL_' 


indf=pd.read_csv(infile,sep='\t',index_col=0)
indf.head()


# In[2]:


def findoutvalue(fname, pattern):

   
    m = re.search(pattern+'(.+?)_', fname) 
    
    if m:
        found = m.group(1)
        

    else:
        print("not found=",fname)
        print("exiting")

        sys.exit(1)
    value=float(found)
    return value
    


# In[3]:


outindex=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
outcols=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]

'''
for index, row in indf.iterrows():
   
    tempval=findoutvalue(index,heatxaxis)
    outcols.append(-1*tempval)

    
    tempval2=findoutvalue(index,heatyaxis)
    outindex.append(-1*tempval2)

'''

outcols=list(set(outcols))
outcols.sort()

outindex=list(set(outindex))
outindex.sort()


    


# In[4]:


outdf = pd.DataFrame(index = outindex,columns =outcols)
outdf.head()


# In[5]:


for index, row in indf.iterrows():
    tempcol=-1*findoutvalue(index,heatxaxis)
    tempindex=-1*findoutvalue(index,heatyaxis)
    outdf.loc[tempindex,tempcol]=row[columnofinterest]
  
    


# In[6]:


outdf.dtypes


# In[7]:


outdf = outdf.astype(float)


# In[8]:


outdf.to_csv(infile+'_'+columnofinterest+'_summaryforheat.txt',sep='\t')


# In[9]:

plt.figure(figsize=(10,8))
mycmap = plt.cm.viridis
mycmap.set_bad("dimgrey")
aaa=sns.heatmap(outdf, cmap=mycmap,annot=True,fmt='.2f')
#aaa.invert_yaxis()
plt.ylabel(heatyaxis)
plt.xlabel(heatxaxis)

heatname=infile+'_'+columnofinterest+".pdf"
plt.savefig(heatname,bbox_inches = "tight")
#plt.show()


# In[10]:


end_time = time.time()

time_elapsed = (end_time - start_time)

print(time_elapsed)

