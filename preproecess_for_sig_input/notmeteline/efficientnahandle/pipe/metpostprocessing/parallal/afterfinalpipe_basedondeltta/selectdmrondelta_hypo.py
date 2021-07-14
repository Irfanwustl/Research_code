#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import glob
import numpy as np
import os
import sys


metfolder=sys.argv[1]# "data_addedcol"
qcutoff=float(sys.argv[2]) #0.5#0.00001

qcol="q"
deltacol="maxCompartmentwisedelta"

deltastart=-0.1
deltaend=-1
deltagap=-.1


# In[2]:


totalnum=int(abs((deltaend-deltastart))*10+1)

deltalist=(np.linspace(deltastart, deltaend, num=totalnum,retstep=deltagap)[0]).tolist()

deltalist=[ round(elem, 2) for elem in deltalist ]

print(deltalist)


# In[3]:


allmetfile=glob.glob(metfolder+"/*.txt")


# In[4]:


for tmpdelta in deltalist:
    tmpoutdir=metfolder+"_"+qcol+str(qcutoff)+"_"+deltacol+str(tmpdelta)
    os.makedirs(metfolder+"_"+qcol+str(qcutoff)+"_"+deltacol+str(tmpdelta))
    for tmpmetfile in allmetfile:
        tmpmetdf=pd.read_csv(tmpmetfile,sep="\t")
        tmpoutdf=tmpmetdf.loc[(tmpmetdf[qcol]<=qcutoff) & (tmpmetdf[deltacol]<=tmpdelta)]
        if tmpoutdf.shape[0]!=0:
            tmpoutdf.to_csv(tmpoutdir+"/"+os.path.basename(tmpmetfile),sep="\t",index=False)
       
    

