#!/usr/bin/env python
# coding: utf-8

# In[1]:


### question
#1: can extraction label be anything?
####
#todo: fix read number
###

import glob
import os
import subprocess
import sys
import pandas as pd


bamfolder=sys.argv[1] #'/Users/irffanalahi/Research/Research_code/support/MGI_automation/toydata/bamfolder'

outfile=sys.argv[2]


extraction_label='auto'







# In[2]:


def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))



####readnumber Extraction########

readnumberfolder=bamfolder+'_ReadNumber/Readnumber'

allreadnumberfiles=listdir_nohidden(readnumberfolder)

allreadnumberfilesList=[]

for fp in allreadnumberfiles:
    tmpdf=pd.read_csv(fp,sep="\t",header=None,names=['total_read'])
    tmpdf['filename']=os.path.basename(fp)
    allreadnumberfilesList.append(tmpdf)
allreadnumberfilesListDF = pd.concat(allreadnumberfilesList, axis=0)

# In[3]:


allbamfolder=listdir_nohidden(bamfolder)
allbamfolder


# In[4]:



commandlist=[]
for abam in allbamfolder:
    str0='\n\n\n#################################################\n'
    source=os.path.basename(abam)
    str1='genome individual create --taxon=1653198737 --name='+source+'\n'
    sample_name=source+'-'+extraction_label
    str2='genome sample create --source='+source+' --extraction-label='+extraction_label+' --name='+sample_name+'\n'
    library_name=sample_name+'-'+'library'
    str3='genome library create --name='+library_name+' --sample='+sample_name+'   --bisulfite-conversion=STANDARD \n'
    
    
    
    
    currentbam=glob.glob(abam+'/*.bam')
    if len(currentbam)!=1:
        print('multiple bams in bam folder. EXITING')
        sys.exit(1)
    currentbam=currentbam[0]
    
    
   
    readnumber=(allreadnumberfilesListDF[allreadnumberfilesListDF['filename']==source]['total_read']).tolist()
    if len(readnumber)!=1:
        print(source)
        print('Error in read number. EXITING')
        sys.exit(1)
    readnumber=readnumber[0]

  
    
    str4='genome instrument-data import trusted-data --analysis-project=17eb4eea6cb344f889c546a3a5f7c686 --import-source-name=Chaudhuri_WGBS  --library='+library_name+'   --source-directory='+abam+'  --import-format=bam --read-count='+str(readnumber)+'\n'
    
    
    
    fullcommand=str0+str1+str2+str3+str4
    
    commandlist.append(fullcommand)
    
    
    
    
    


# In[5]:


with open(outfile, 'w') as f:
    for item in commandlist:
        f.write("%s" % item)

