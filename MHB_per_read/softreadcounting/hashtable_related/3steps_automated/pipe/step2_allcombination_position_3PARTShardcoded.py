#!/usr/bin/env python
# coding: utf-8

# In[1]:



import os
import glob
import pybedtools
import sys


infolder=sys.argv[1] #'/Users/irffanalahi/Research/Research_update/SoftRD/hashtable_stats/B22withLTME/automate_v3_3steps/deltafolder_withend_allout'

outfolder=sys.argv[2] #'/Users/irffanalahi/Research/Research_update/SoftRD/hashtable_stats/B22withLTME/automate_v3_3steps/allcombination'



# In[2]:


def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))


# In[3]:


allfolders=listdir_nohidden(infolder)


# In[4]:




def runbedinter(filelist1,filelist2,filelist3):
    for  f1 in filelist1:
        for f2 in filelist2:
            for f3 in filelist3:
                f1bed=pybedtools.BedTool(f1)
                f2bed=pybedtools.BedTool(f2)
                f3bed=pybedtools.BedTool(f3)
                f1intf2=f1bed.intersect(f2bed,u=True,f=1,F=1)

                f1intf2intf3=f1intf2.intersect(f3bed,u=True,f=1,F=1)
                
                f1base=os.path.basename(f1)
                f2base=os.path.basename(f2)
                f3base=os.path.basename(f3)
                
                outname=outfolder+'/'+f1base+'_int_'+f2base+'_int_'+f3base
                
                
               
                
                f1intf2intf3.moveto(outname)
            
            
           
        


# In[5]:


totalfolders=len(allfolders)

if totalfolders!=3:
    print('totalfolders!=3. EXITING')
    sys.exit(1)


tempfilelist1=listdir_nohidden(allfolders[0])
    
   
    

tempfilelist2=listdir_nohidden(allfolders[1])


tempfilelist3=listdir_nohidden(allfolders[2])
        
        
runbedinter(tempfilelist1,tempfilelist2,tempfilelist3)
        

   

