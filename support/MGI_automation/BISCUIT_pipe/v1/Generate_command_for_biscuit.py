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


bamfolder=sys.argv[1] #'/Users/irffanalahi/Research/Research_code/support/MGI_automation/toydata/bamfolder'

outfile=sys.argv[2]


extraction_label='auto'



# In[2]:


def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))


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
    
    samtools_result = subprocess.Popen(['samtools', 'view','-c',currentbam], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stdout,stderr= samtools_result.communicate()
   
    readnumber=stdout.split()[0].decode()
  
    
    str4='genome instrument-data import trusted-data --analysis-project=17eb4eea6cb344f889c546a3a5f7c686 --import-source-name=Chaudhuri_WGBS  --library='+library_name+'   --source-directory='+abam+'  --import-format=bam --read-count='+readnumber+'\n'
    
    
    
    fullcommand=str0+str1+str2+str3+str4
    
    commandlist.append(fullcommand)
    
    
    
    
    


# In[5]:


with open(outfile, 'w') as f:
    for item in commandlist:
        f.write("%s" % item)

