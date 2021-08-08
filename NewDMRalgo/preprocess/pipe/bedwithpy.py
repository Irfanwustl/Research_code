#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import glob
import re
import sys
import os
import subprocess
compdelta=sys.argv[1] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/DMRrelated/ITGAE_patternrecognition/changepointtest/preproocess_Develop/e2e/ITGAEandERICH1_cin_nr0.5_imputed_rowmean.txt_compdeltafor_bg"
metout=sys.argv[2] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/DMRrelated/ITGAE_patternrecognition/changepointtest/preproocess_Develop/e2e/input_out_mincpg2toy"
outfolder=sys.argv[3] #metout+"_intersected"


# In[2]:


compdeltafilelist=glob.glob(compdelta+"/*.txt")
metoutlfilelist=glob.glob(metout+"/*.txt")


# In[3]:


#print(compdeltafilelist)
#print(metoutlfilelist)


# In[4]:


filepairs=[]
for cmpdeltafile in compdeltafilelist:
    
    cmpdeltafilebase=os.path.basename(cmpdeltafile)

    m = re.search('g1_(.+?).txt', cmpdeltafilebase)
    if m:
        found = m.group(1)

    else:
        print("cell type not found", cmpdeltafilebase)
        print("exiting")
        sys.exit(1)
 
    for metoutfile in metoutlfilelist:
        metoutfilebase=os.path.basename(metoutfile)
     
        mm=re.search('g1_(.+?)_\d+_g2', metoutfilebase)
        if mm:
            found2 = mm.group(1)

        else:
            print("cell type not found",  metoutfilebase)
            print("exiting")
            sys.exit(1)
       
        if found==found2:
            outfilename=outfolder+"/"+metoutfilebase
            with open(outfilename, "w") as outfile:
    
                subprocess.run(['bedtools','intersect','-wa','-wb','-a',cmpdeltafile,'-b',metoutfile,'-header'],stdout=outfile)
                filepairs.append((cmpdeltafile,metoutfile))
               
            
    

