#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys
import os
import sys
smfile=sys.argv[1] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/DMRrelated/diagnosis/AUCcolorcode/test/PBLtilMel_meldiff-.7_other-.1_q0.00001_sorted4_1_singleCpG_final_recordSM.txt"
finalfile=sys.argv[2] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/DMRrelated/diagnosis/AUCcolorcode/test/PBLtilmelq0.00001_sorted4_1_dropdup_model_data_bam_onlyregionIN_PBLtilMel_meldiff-.7_other-.1_q0.00001_sorted4_1_top_1000_bam_informative_cpg3_row_combinedfilename.txt"
outfolder=sys.argv[3] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/DMRrelated/diagnosis/AUCcolorcode/test/outfinal"
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
for cell in celllist:
    cellfolder=outfolder+"/"+cell
    os.makedirs(cellfolder)


# In[3]:


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
    
    minpos=min(poslist)
    maxpos=max(poslist)

    
    return outchrom,minpos,maxpos
        
def matchwithSM(fragCHROM,fragMINpos,fragMAXpos):
    correspondingDMR=smdf[(smdf['DMRchr']==fragCHROM) & (smdf['DMRstart'] <= fragMINpos+1) & (smdf['DMRend'] >= fragMAXpos)]
   
    
    if correspondingDMR.shape[0]==0:
        print("correspondingDMR.shape[0]==0")
        print(fragCHROM,fragMINpos,fragMAXpos)
        return -1,-1,-1
        #sys.exit(1)
    
    correspondingDMRchr=correspondingDMR['DMRchr'].tolist()[0]
    correspondingDMRstart=correspondingDMR['DMRstart'].tolist()[0]
    correspondingDMRend=correspondingDMR['DMRend'].tolist()[0]
    
    
    return correspondingDMRchr,correspondingDMRstart,correspondingDMRend
    
    
    
    
    
        


# In[4]:


for index, row in finaldf.iterrows():
    if row['finalacceptedfor']!="notdetermined" or row['finalrejectedfor']!="notdetermined":
        if row['finalacceptedfor']!="notdetermined":
            currentchrom,currentminpos,currentmaxpos=processSingleRow(row,'acceptedCpG')
            
            



            


        else:
            currentchrom,currentminpos,currentmaxpos=processSingleRow(row,'notacceptedCpG')

     

        currentDMRchr,currentDMRstart,currentDMRend=matchwithSM(currentchrom,currentminpos,currentmaxpos)
    
    if currentDMRchr!=-1:    
        outfinal.loc[index,"DMRchr"]=currentDMRchr
        outfinal.loc[index,"DMRstart"]=currentDMRstart
        outfinal.loc[index,"DMRend"]=currentDMRend

outfinal.head()
        


# In[5]:


smgrouped=smdf.groupby(['celltype'])
for name, group in smgrouped:
  
    DMRgrouped=group.groupby(['DMRchr','DMRstart','DMRend'])
    for DMRname,DMRgroup  in DMRgrouped:
        
        tempoutfinal=outfinal[(outfinal['DMRchr']==DMRname[0]) & (outfinal['DMRstart']==DMRname[1]) & (outfinal['DMRend']==DMRname[2])]
        mixturegrouped=tempoutfinal.groupby('filename')
        
        mixlist=[]
        proportionlist=[]
        for mixture,mixturegroup in mixturegrouped:
            mixlist.append(mixture)
            mixturegrouppos=mixturegroup[mixturegroup['finalacceptedfor']==name].shape[0]
            
            mixturegroupneg=mixturegroup[mixturegroup['finalrejectedfor']==name].shape[0]
            
            
            
            if mixturegrouppos+mixturegroupneg !=0:
                prop=1*mixturegrouppos/(mixturegrouppos+mixturegroupneg)
            elif mixturegrouppos==0:
                prop=0
            
            else:
                print("errorr in prop")
                sys.exit(1)
            
            proportionlist.append(prop)
        
        
        outdf=pd.DataFrame({"Mixture":mixlist,name:proportionlist})
        outname=outfolder+"/"+name+"/"+str(DMRname[0])+"_"+str(DMRname[1])+"_"+str(DMRname[2])+".txt"
        
        outdf.to_csv(outname,sep="\t",index=False)
        
        
            
            
        
        
    

