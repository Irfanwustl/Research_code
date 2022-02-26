#!/usr/bin/env python
# coding: utf-8

# In[1]:




import pandas as pd
import concurrent.futures
import os
import sys
import time

reffile=sys.argv[1] #'promdataready_all_matrix_head.txt'
phenfile=sys.argv[2] #'pbl_PHENOCLASS.txt'
compartmentfile=sys.argv[3]  #'pbl_PHENOCLASS_compartment.txt'
Replicate_With_value=1 ### at least this many replicates must have values

outfolder=sys.argv[4] 

maxworkerhere=int(sys.argv[5])

start_time = time.time()


refdf=pd.read_csv(reffile,sep="\t")
refdf.set_index(['chrom','start','end'], inplace=True)
phendf=pd.read_csv(phenfile,sep="\t",header=None,index_col=0)
compartmentdf=pd.read_csv(compartmentfile,sep="\t",header=None,index_col=0)


# In[2]:


naindex=refdf.isna() 


# In[3]:


def NaHandle(listoflistofindeces): #class1indices,class2indices
    
    allnoselindex=[]   
    
    for currentclassindeces in listoflistofindeces:
       
        currentclassindecesTOTAL=sum(currentclassindeces)
        currentclassindecescutoff=currentclassindecesTOTAL-Replicate_With_value
        tmp=naindex.iloc[:, currentclassindeces]
        tmpsum=tmp.sum(axis=1)
        tmpsumselectedindex=tmpsum[tmpsum>currentclassindecescutoff].index
        allnoselindex.append(tmpsumselectedindex.tolist())
    
    allnoselindex = [x for sublist in allnoselindex for x in sublist]

    allnoselindex=list(set(allnoselindex))

    NAoutdf = refdf[~refdf.index.isin(allnoselindex)]
    
    #NAoutdf.to_csv('testNA.txt',sep='\t')
    #sys.exit(1)
    
    return NAoutdf

    

def rowmeanANDothermean(outdffrom_NaHandle,profileclassindices,compartmentaginstindices,profileclassname,compartmentagainstname):
    
    
    profilemean=outdffrom_NaHandle.iloc[:, profileclassindices].mean(axis=1)
    profilemeantempdf=profilemean.to_frame(profileclassname)
    
    compareagainstmean=outdffrom_NaHandle.iloc[:, compartmentaginstindices].mean(axis=1)
    compareagainstmeantempdf=compareagainstmean.to_frame(compartmentagainstname)
    
    rowmeandf=pd.concat([profilemeantempdf,compareagainstmeantempdf],axis=1)
    
    
    
    #rowmeandf.to_csv('testRowMean.txt',sep='\t')

    
    rowmeandf[profileclassname+"-others"]=rowmeandf[profileclassname]-rowmeandf[compartmentagainstname]
    rowmeandf[compartmentagainstname+"-others"]=rowmeandf[compartmentagainstname]-rowmeandf[profileclassname]
    
    rowmeandf=rowmeandf[[profileclassname+"-others",compartmentagainstname+"-others"]]
    rowmeandf.to_csv(outfolder+"/"+profileclassname+"/g1_"+profileclassname+"_g2_"+compartmentagainstname,sep='\t')
    


# In[4]:


def coreAlgo(class1indices,class2indices,class1name,class2name):
    ###nahandle
    NAresult=NaHandle([class1indices,class2indices])
    
    ##delta calculation
    rowmeanANDothermean(NAresult,class1indices,class2indices,class1name,class2name)
   


# In[5]:


with concurrent.futures.ProcessPoolExecutor(max_workers=maxworkerhere) as executor:

    for i in range(phendf.shape[0]):
        classes = phendf.iloc[i, :]
        class1 = (classes == 1).tolist()
        allclass2 = (classes == 2).tolist()

        nowprofilethiscell=phendf.index[i]
        os.mkdir(outfolder+'/'+nowprofilethiscell)#######################
        for j in range(compartmentdf.shape[0]):
            compartmentclasses = compartmentdf.iloc[j, :]

            ###find compartment class memeber###
            compartmentclass1=(compartmentclasses==1).tolist()

            ###find which files to compare against from this compartment ######## 
            compare_against_from_this_compartment=[allclass2 and compartmentclass1 for allclass2, compartmentclass1 in zip(allclass2, compartmentclass1)]

            check_own_group=[class1 and compartmentclass1 for class1, compartmentclass1 in zip(class1, compartmentclass1)]

            if True in check_own_group:


                '''
                print("now======",nowprofilethiscell)


                print(class1)
                print(allclass2)
                print(check_own_group)
                print(compare_against_from_this_compartment)
                '''




                for k in range(phendf.shape[0]):
                    other_classes = phendf.iloc[k, :]
                    other_class1=(other_classes == 1).tolist()
                    is_it_in_own_group=[other_class1 and compare_against_from_this_compartment for other_class1, compare_against_from_this_compartment in zip(other_class1, compare_against_from_this_compartment)]


                    if True in is_it_in_own_group:
                        #print('found.......')

                        #print(phendf.index[k])
                        #print(is_it_in_own_group)
                        #sys.exit(1)


                        
                        #coreAlgo(class1,other_class1,nowprofilethiscell,phendf.index[k])
                        executor.submit(coreAlgo,class1,other_class1,nowprofilethiscell,phendf.index[k])



# In[6]:


print('finished')

end_time = time.time()

time_elapsed = (end_time - start_time)

print(time_elapsed)

