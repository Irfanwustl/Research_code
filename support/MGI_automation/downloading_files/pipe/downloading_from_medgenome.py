#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import sys

medgenomesite=sys.argv[1] #'https://portal-us.medgenome.com/P2003825_04222022/FASTQ' ###without backslash
username=sys.argv[2] #'P2003825_04222022'
password=sys.argv[3] #'t^8s368cK!@%'
infile=sys.argv[4] #'md5sum.txt'

wheretodownload=sys.argv[5]

os.makedirs(wheretodownload)

fastqdownloadfolder=wheretodownload+'/FASTQ'
os.makedirs(fastqdownloadfolder)
logfolder=wheretodownload+'/logs'
os.makedirs(logfolder)



indf=pd.read_csv(infile,header=None, delimiter=r"\s+")
indf.head()


# In[2]:


allfiles=indf[1].tolist()
len(allfiles)


# In[3]:



commandlist=['set +H \n']

for afile in allfiles:
    tempcommand="bsub -M 48000000 -R 'select[mem>48000] rusage[mem=48000]' -oo " +logfolder+'/'+afile+".log -q general -a 'docker(irfanwustl/insilico_mix)'  wget -P "+fastqdownloadfolder+'  --no-directories --user='+username+' --password='+password+' --recursive --no-parent --continue --no-check-certificate -e robots=off ' +medgenomesite+'/'+afile+" \n"
    commandlist.append(tempcommand)
    


# In[4]:


commandlist


# In[5]:


with open(wheretodownload+"/medgenome_download.sh", 'w') as f:
    for item in commandlist:
        f.write("%s" % item)

