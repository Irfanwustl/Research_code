#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys
import os
import sys
import time
start_time = time.time()
smfile=sys.argv[1] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/DMRrelated/diagnosis/AUCcolorcode/test2/Outreal_healthy/promdatareadyCD8TIL_all_matrixCin_nr0.5_imputed_g1_CD8_TIL_3_g2_others_9.txt_q0.05_diff0.1_hypo.txt_75percentile.txt_recordSM.txt"#sys.argv[1] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/DMRrelated/diagnosis/AUCcolorcode/test/PBLtilMel_meldiff-.7_other-.1_q0.00001_sorted4_1_singleCpG_final_recordSM.txt"
finalfile=sys.argv[2] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/DMRrelated/diagnosis/AUCcolorcode/test2/Outreal_healthy/totincludinghealthy_final_informative_row_combinedfilename.txt"#sys.argv[2] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/DMRrelated/diagnosis/AUCcolorcode/test/PBLtilmelq0.00001_sorted4_1_dropdup_model_data_bam_onlyregionIN_PBLtilMel_meldiff-.7_other-.1_q0.00001_sorted4_1_top_1000_bam_informative_cpg3_row_combinedfilename.txt"
outfolder=sys.argv[3] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/DMRrelated/diagnosis/AUCcolorcode/test2/Outreal_healthy/totwithhealthy_out"#sys.argv[3] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/DMRrelated/diagnosis/AUCcolorcode/test/outfinal"
mincpg=int(sys.argv[4]) #3
smdf=pd.read_csv(smfile,sep="\t")
finaldf=pd.read_csv(finalfile,sep="\t")

finaldf['acceptedCpG'] = finaldf.acceptedCpG.apply(lambda x: x[1:-1].split(','))
finaldf['notacceptedCpG'] = finaldf.notacceptedCpG.apply(lambda x: x[1:-1].split(','))
outfinal=finaldf.copy()
outfinal["DMRchr"]=-1
outfinal["DMRstart"]=-1
outfinal["DMRend"]=-1
outfinal.head()


# In[2]:



smdf['celltype']=smdf.celltype.apply(lambda x: x[1:-1])
celllist=list(set(smdf['celltype'].tolist()))

smdf=smdf.set_index(['DMRchr','DMRstart','DMRend','celltype'])


# In[3]:


filenames=list(set(outfinal['filename'].tolist()))
smpos=pd.DataFrame(index=smdf.index.copy(),columns=filenames)
smpos[:] = 0
smpos
smneg=smpos.copy()
smdf.reset_index(inplace=True)
smneg.head()


# In[4]:



def processSingleRow(onerow,colname):
    CpGlist=list(map(eval,onerow[colname]))
    chromlist=[]
    poslist=[]
    for cpg in CpGlist:
        tmp=cpg.split(":")
        chromlist.append(tmp[0])
        poslist.append(int(tmp[1]))
        
    
    
    chromlist=list(set(chromlist))
    if len(chromlist)!=1:
        print("many chromosome in a fragment??????? the output may be wrong")
        print(onerow)
    
    outchrom=chromlist[0]
    
    
    #poslist.sort()
    
    return outchrom,poslist


def matchwithSM(fragCHROM,fragposlist,currentfilename,posneg):
    
    fragposlen=len(fragposlist)
    fragMINpos=min(fragposlist)
    fragMAXpos=max(fragposlist)
    
    
    
    correspondingDMR1=smdf[(smdf['DMRchr']==fragCHROM) & (smdf['DMRstart'] <= fragMINpos+1) & (smdf['DMRend'] >= fragMAXpos+1)]
    
    correspondingDMR2=smdf[(smdf['DMRchr']==fragCHROM) & (smdf['DMRstart'] >= fragMINpos+1) & (smdf['DMRend'] <= fragMAXpos+1)]
    
    correspondingDMR3=smdf[(smdf['DMRchr']==fragCHROM) & (smdf['DMRstart'] >= fragMINpos+1) & (smdf['DMRend'] >= fragMAXpos+1)]
    
    if correspondingDMR3.shape[0]>0:
       
        
        for index, row in correspondingDMR3.iterrows():
            fragposlist.append(row['DMRstart']-1)
            fragposlist.sort()
            
            foundindex=fragposlist.index(row['DMRstart']-1)
            if fragposlen - foundindex < mincpg+1:
                correspondingDMR3=correspondingDMR3.drop(index)
            
            fragposlist.remove(row['DMRstart']-1)
        
        
        
    
    correspondingDMR4=smdf[(smdf['DMRchr']==fragCHROM) & (smdf['DMRstart'] <= fragMINpos+1) & (smdf['DMRend'] <= fragMAXpos+1)]
    if correspondingDMR4.shape[0]>0:
        
        for index, row in correspondingDMR4.iterrows():
            fragposlist.append(row['DMRend']-1)
            
            fragposlist.sort()
            
            
            foundindex=fragposlist.index(row['DMRend']-1)
            
            ###was DMRend already in fragposlist? 
            if len(fragposlist)==set(fragposlist):
                cutoff=mincpg
            else:
                cutoff=mincpg-1
            
            if foundindex < mincpg-1: 
                correspondingDMR4=correspondingDMR4.drop(index)
            
            fragposlist.remove(row['DMRend']-1)
   
    correspondingDMR=pd.concat([correspondingDMR1,correspondingDMR2,correspondingDMR3,correspondingDMR4],axis=0)
    correspondingDMR = correspondingDMR.drop_duplicates()
 
    correspondingDMR=correspondingDMR.set_index(['DMRchr','DMRstart','DMRend','celltype'])
   
    
    for index, row in correspondingDMR.iterrows():
        if posneg=="pos":
            smpos.at[index,currentfilename]=smpos.at[index,currentfilename]+1
        elif posneg=="neg":
           
            smneg.at[index,currentfilename]=smneg.at[index,currentfilename]+1
            
    

            
    
   


# In[5]:



for index, row in finaldf.iterrows():
    if row['finalacceptedfor']!="notdetermined" or row['finalrejectedfor']!="notdetermined":
        tempfilename=row['filename']
        if row['finalacceptedfor']!="notdetermined":
            currentchrom,currentposlist=processSingleRow(row,'acceptedCpG')
            matchwithSM(currentchrom,currentposlist,tempfilename,'pos')
            
            



            


        else:
            currentchrom,currentposlist=processSingleRow(row,'notacceptedCpG')
            matchwithSM(currentchrom,currentposlist,tempfilename,'neg')


# In[6]:


smpos.to_csv(outfolder+"/smpos.txt",sep="\t")
smneg.to_csv(outfolder+"/smneg.txt",sep="\t")


# In[7]:


smposAndsmneg=smpos+smneg
smposAndsmneg.to_csv(outfolder+"/smposANDsmneg.txt",sep="\t")


# In[8]:


smposAndsmneg.replace(0, 1,inplace=True)
prop=smpos/smposAndsmneg

prop.to_csv(outfolder+"/prop.txt",sep="\t")


# In[9]:


prop.head()


# In[10]:


for cell in celllist:
    cellfolder=outfolder+"/"+cell
    os.makedirs(cellfolder)  ##########################################################################


# In[11]:



for index, row in prop.iterrows():
    indexstr=list(map(str,index))
    tempname='_'.join(indexstr)
    tempname=cellfolder+"/"+tempname+".txt"
    row=row.reset_index()
    
    rowdf=pd.DataFrame({"Mixture":row.iloc[:,0],index[3]:row.iloc[:,1]})
    
    
    #print(rowdf.columns[1])
    #rowdf.rename(columns={rowdf.columns[0]:"Mixture",rowdf.columns[1]:index[3]},inplace=True, errors='raise')
    #print(rowdf)
   
    #print(rowdf.iloc[:,2])
    rowdf.to_csv(tempname,sep="\t",index=False,na_rep='NA')
print("--- %s seconds ---" % (time.time() - start_time))

