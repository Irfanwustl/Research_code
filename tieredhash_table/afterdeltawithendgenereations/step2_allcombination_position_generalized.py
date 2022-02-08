#!/usr/bin/env python
# coding: utf-8

# In[1]:



import os
import glob
import pybedtools
import sys
import itertools


infolder=sys.argv[1] #'/Users/irffanalahi/Research/Research_update/SoftRD/hashtable_stats/B22withLTME/automate_v3_3steps/deltafolder_withend_allout'

outfolder=sys.argv[2] #'/Users/irffanalahi/Research/Research_update/SoftRD/hashtable_stats/B22withLTME/automate_v3_3steps/allcombination'



# In[2]:


def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))


# In[3]:


allfolders=listdir_nohidden(infolder)


# In[4]:




def runbedinter(combinations):
    for comb in combinations:
        lst_bedfiles = []
        lst_basenames = []
        for file in comb:
            lst_bedfiles.append(pybedtools.BedTool(file))
            lst_basenames.append(os.path.basename(file))
        
        for i in range(len(lst_bedfiles) - 1):
            if i == 0:
                inter = lst_bedfiles[0].intersect(lst_bedfiles[1], u=True, f=1, F=1)
            else:
                inter = inter.intersect(lst_bedfiles[i+1], u=True, f=1, F=1)
                
        outname = outfolder + '/' + '_int_'.join(lst_basenames)
        inter.moveto(outname)
            
            
           
        


# In[5]:

totalfolders=len(allfolders)
all_fol = []
for i in range(totalfolders):
    all_fol.append(listdir_nohidden(allfolders[i]))
    
all_fol_combs = list(itertools.product(*all_fol))
        
        
runbedinter(all_fol_combs)
        

   

