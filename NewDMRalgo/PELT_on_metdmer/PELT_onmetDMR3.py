#!/usr/bin/env python
# coding: utf-8

# In[1]:


import ruptures as rpt  # our package
from ruptures.metrics import hausdorff
import pandas as pd
import concurrent.futures
import sys
from collections import defaultdict
from scipy.spatial import distance
import numpy as np
import copy

infile=sys.argv[1] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/DMRrelated/ITGAE_patternrecognition/changepointtest/preproocess_Develop/preprocess_ontopmetilene/Again/betweenchildrencorr/combinebaddistance/BluOurPBLOurCD8til_wg_all_matrixCin_nr0.5_imputed_g1_CD8TIL_3_g2_others_36.txt_q0.00001_diff0.1_hypo.txt_subset_PELT_childcorr1.txt"  
minCpG=int(sys.argv[2]) #3
penalty_value =float(sys.argv[3]) #1 
percormetDMR=int(sys.argv[4])  #2 #### for parallal
outfile=sys.argv[5] #infile+"_mincpg_"+str(minCpG)+"pelt.txt" 
outsegmentfile=sys.argv[6] #infile+"_mincpg_"+str(minCpG)+"pelt_seginfo.txt" #sys.argv[6]
combinedoutfile=sys.argv[7] #infile+"_mincpg_"+str(minCpG)+"pelt_combined.txt" 
combinedoutsegmentfile=sys.argv[8] #infile+"_mincpg_"+str(minCpG)+"pelt_combined_seginfo.txt" 

indf=pd.read_csv(infile,sep="\t",low_memory=False,index_col=[0,1,2])

indf.head()


# In[2]:



indfdropped=indf#.drop(['chrom','start','end'],axis=1)
columnnames=(indfdropped.columns).tolist()
indfdropped.head()


# In[3]:


def segment_generator():
    
    segmentlist=[]
    
    qindex=columnnames.index('q')

    subdf=indfdropped.iloc[:,:qindex]
   
    grouped=subdf.groupby(['DMRchrom','DMRstart','DMRend'])
    for name, group in grouped:
        subgroup=group.drop(["DMRchrom","DMRstart","DMRend"],axis=1)
        segmentlist.append((name,subgroup))
    
  
    
    return segmentlist


# In[4]:


class PELT_result:
    def __init__(self,underlyingdf,dmrchrom,dmrstart,dmrend,peltsegmentlist):
        self.underlyingdf=underlyingdf
        self.underlyingdf_index=self.underlyingdf.index
        self.corrdistcutoff=0.1
        
        self.dmrchrom=dmrchrom
        self.dmrstart=dmrstart
        self.dmrend=dmrend
        self.peltsegmentlist=peltsegmentlist
        self.fullDMRcondnumber=np.linalg.cond(self.underlyingdf,p=2)
        self.totalsegment=len(self.peltsegmentlist)-1
        self.metpeltsegmentDICT={'DMRchrom':self.dmrchrom,'DMRstart':self.dmrstart,'DMRend':self.dmrend,"totalPeltSegement":self.totalsegment,"conditionnumber":self.fullDMRcondnumber}
        self.metpeltsegmentDICTinfo,self.metpeltcombinedsegmentDICTinfo=self.recordPeltDMR() #{'DMRchrom':self.dmrchrom,'DMRstart':self.dmrstart,'DMRend':self.dmrend,"PeltSegement":self.peltsegmentlist}
        
    def recordPeltDMR(self):
        underlyingdfavg=self.underlyingdf.mean(axis=0)
       
        underlyingdfmax=underlyingdfavg.max()
        underlyingdfmin=underlyingdfavg.min()
        
        
        
        prevcorressavgdiff=pd.Series(dtype='float64')
        
        outdict=defaultdict(list)
        nextstartloc=self.underlyingdf_index.get_loc((self.dmrchrom,self.dmrstart-1,self.dmrstart+1))
        prevend=self.dmrstart-1
        
       
        for peltsegment in self.peltsegmentlist:
            
            
            currentstartindex=self.underlyingdf_index[nextstartloc]
            nextstartloc=self.underlyingdf_index.get_loc(peltsegment)
            currentendindex=self.underlyingdf_index[nextstartloc-1]
            
            if peltsegment == self.peltsegmentlist[-1]:
                currentendindex=self.underlyingdf_index[nextstartloc]
            
           
            
            outdict['chrom'].append(currentstartindex[0])
            outdict['start'].append(currentstartindex[1]+1)
            outdict['end'].append(currentendindex[2])
            
            
          
            corressdf=self.underlyingdf.loc[currentstartindex:currentendindex, :]
            
          
           
            
            corresscondnumber=np.linalg.cond(corressdf,p=2)
            corressavgdiff=corressdf.mean(axis=0) 
            corressavgdict=corressavgdiff.to_dict()
            
            #####distances#########
            cosdistance=distance.cosine(corressavgdiff,underlyingdfavg)
            eucliddistance=distance.euclidean(corressavgdiff,underlyingdfavg)
            corrdistance=distance.correlation(corressavgdiff,underlyingdfavg)
            
            ####between children####
           
            if prevcorressavgdiff.empty:
                childrencosdistance=99999
                childreneucliddistance=99999
                childrencorrdistance=99999
            else:
                childrencosdistance=distance.cosine(corressavgdiff,prevcorressavgdiff)
                childreneucliddistance=distance.euclidean(corressavgdiff,prevcorressavgdiff)
                childrencorrdistance=distance.correlation(corressavgdiff,prevcorressavgdiff)
            
            #####distances#########
            
            
            
            
            
            outdict['numofcpg'].append(corressdf.shape[0])
            
            
            
            outdict['conditionnumber'].append(corresscondnumber)
            outdict['parentDMRconditionnumber'].append(self.fullDMRcondnumber)
            outdict['conditionnumber/parentDMRconditionnumber'].append(corresscondnumber/self.fullDMRcondnumber)
            
            outdict['parentDMRchrom'].append(self.dmrchrom)
            outdict['parentDMRstart'].append(self.dmrstart)
            outdict['parentDMRend'].append(self.dmrend)
            
            outdict['parentnumofcpg'].append((self.underlyingdf).shape[0])
            
            
            
            
            outdict['cos_distance'].append(cosdistance)
            outdict['euclid_distance'].append(eucliddistance)
            outdict['correlation_distance'].append(corrdistance)
            
            
            outdict['prevchild_cos_distance'].append(childrencosdistance)
            outdict['prevchild_euclid_distance'].append(childreneucliddistance)
            outdict['prevchild_correlation_distance'].append(childrencorrdistance)
            
            for key, value in corressavgdict.items():
                outdict[key].append(value)
            
            #print(outdict)
            #sys.exit(1)
            outdict['parentDMRmax'].append(underlyingdfmax)
            outdict['parentDMRmin'].append(underlyingdfmin)
            
            prevend=peltsegment[2]
            
            prevcorressavgdiff=corressavgdiff
        
        outdict=dict(outdict)
        if self.peltsegmentlist[len(self.peltsegmentlist)-1][2]!=self.dmrend:
            print(self.dmrchrom,self.dmrstart,self.dmrend)
            print("final pelt seg notin DMR end")
        
       
      
        outdictcopy=copy.deepcopy(outdict)
        combdf=self.combinedbadDMR(outdictcopy,underlyingdfavg)
        
     
        return outdict,combdf
    
    
    
    def combinedbadDMR(self,firstpassdict,parentdfavg):
   
        firstpassdf=pd.DataFrame.from_dict(firstpassdict)
        
        while True:
            
            smallestcorrdis=firstpassdf['prevchild_correlation_distance'].min()
            
           
            
            if smallestcorrdis>=self.corrdistcutoff:
                break
            smallestcorrdisindex=firstpassdf[['prevchild_correlation_distance']].idxmin()
            
           
            #####combine####
            combinedchrom=(firstpassdf.iloc[smallestcorrdisindex]['chrom']).values[0]
        
           
            combinedstartIndex=(combinedchrom,(firstpassdf.iloc[smallestcorrdisindex-1]['start']).values[0]-1,(firstpassdf.iloc[smallestcorrdisindex-1]['start']).values[0]+1)
            combinedendIndex=(combinedchrom,(firstpassdf.iloc[smallestcorrdisindex]['end']).values[0]-2,(firstpassdf.iloc[smallestcorrdisindex]['end']).values[0])
            
            combineddf=self.underlyingdf.loc[combinedstartIndex:combinedendIndex,:]
            
            
            combineddfavgdiff=combineddf.mean(axis=0)
            
           
            combinedcosdistance=99999
            combinedeucliddistance=99999
            combinedcorrdistance=99999
            combinedcondnumber=(firstpassdf.loc[smallestcorrdisindex,'parentDMRconditionnumber']).values[0]
            
            combinedPARENTcos_distance=distance.cosine(combineddfavgdiff,parentdfavg)
            combinedPARENTeuclid_distance=distance.euclidean(combineddfavgdiff,parentdfavg)
            combinedPARENTcorrelation_distance=distance.correlation(combineddfavgdiff,parentdfavg)
           # print(combineddf)
              
                
           
      
  
            
            
            if smallestcorrdisindex.values[0]+1 <firstpassdf.shape[0]:
                
                adjacentnextlocstartindex=(combinedchrom,(firstpassdf.iloc[smallestcorrdisindex+1]['start']).values[0]-1,(firstpassdf.iloc[smallestcorrdisindex+1]['start']).values[0]+1)
                adjacentnextlocendindex=(combinedchrom,(firstpassdf.iloc[smallestcorrdisindex+1]['end']).values[0]-2,(firstpassdf.iloc[smallestcorrdisindex+1]['end']).values[0])
             
                
                adjacentnextdf=self.underlyingdf.loc[adjacentnextlocstartindex:adjacentnextlocendindex,:]
                adjacentnextdfavgdiff=adjacentnextdf.mean(axis=0)
                
                
                adjacentnextcosdistance=distance.cosine(combineddfavgdiff,adjacentnextdfavgdiff)
                adjacentnexteucliddistance=distance.euclidean(combineddfavgdiff,adjacentnextdfavgdiff)
                adjacentnextcorrdistance=distance.correlation(combineddfavgdiff,adjacentnextdfavgdiff)
                
                firstpassdf.loc[smallestcorrdisindex+1,'prevchild_cos_distance']=adjacentnextcosdistance
                firstpassdf.loc[smallestcorrdisindex+1,'prevchild_euclid_distance']=adjacentnexteucliddistance
                firstpassdf.loc[smallestcorrdisindex+1,'prevchild_correlation_distance']=adjacentnextcorrdistance
             ############################################ 
           
            if smallestcorrdisindex.values[0]-2 >=0:
                
             
                adjacentprevlocstartindex=(combinedchrom,(firstpassdf.iloc[smallestcorrdisindex-2]['start']).values[0]-1,(firstpassdf.iloc[smallestcorrdisindex-2]['start']).values[0]+1)
                adjacentprevlocendindex=(combinedchrom,(firstpassdf.iloc[smallestcorrdisindex-2]['end']).values[0]-2,(firstpassdf.iloc[smallestcorrdisindex-2]['end']).values[0])
               
                
                adjacentprevdf=self.underlyingdf.loc[adjacentprevlocstartindex:adjacentprevlocendindex,:]
                adjacentprevdfavgdiff=adjacentprevdf.mean(axis=0)
                
                combinedcosdistance=distance.cosine(combineddfavgdiff,adjacentprevdfavgdiff)
                combinedeucliddistance=distance.euclidean(combineddfavgdiff,adjacentprevdfavgdiff)
                combinedcorrdistance=distance.correlation(combineddfavgdiff,adjacentprevdfavgdiff)
                
                combinedcondnumber=np.linalg.cond(combineddf,p=2)
                

                
                
            ######
            #######start here from morning############
            
            firstpassdf.loc[smallestcorrdisindex,'start']=(firstpassdf.iloc[smallestcorrdisindex-1]['start']).values[0]
            firstpassdf.loc[smallestcorrdisindex,'numofcpg']=combineddf.shape[0]
            firstpassdf.loc[smallestcorrdisindex,'conditionnumber']=combinedcondnumber
            firstpassdf.loc[smallestcorrdisindex,'conditionnumber/parentDMRconditionnumber']=combinedcondnumber/(firstpassdf.loc[smallestcorrdisindex,'parentDMRconditionnumber']).values[0]
            firstpassdf.loc[smallestcorrdisindex,'prevchild_cos_distance']=combinedcosdistance
            firstpassdf.loc[smallestcorrdisindex,'prevchild_euclid_distance']=combinedeucliddistance
            firstpassdf.loc[smallestcorrdisindex,'prevchild_correlation_distance']=combinedcorrdistance
            
            firstpassdf.loc[smallestcorrdisindex,'cos_distance']=combinedPARENTcos_distance
            firstpassdf.loc[smallestcorrdisindex,'euclid_distance']=combinedPARENTeuclid_distance
            firstpassdf.loc[smallestcorrdisindex,'correlation_distance']=combinedPARENTcorrelation_distance
            
        
         
            for ci in combineddfavgdiff.index:
                firstpassdf.loc[smallestcorrdisindex,ci]=combineddfavgdiff[ci]            

            firstpassdf.drop([smallestcorrdisindex.values[0]-1],inplace=True)
            
     
           
            firstpassdf.reset_index(inplace=True,drop=True)
        
        
        return firstpassdf
        
            
       
           
 
        
        


# In[5]:


def get_pelt_result(signal_pelttuple):
    DMR=signal_pelttuple[0]
    signal_pelt=signal_pelttuple[1]
    try:
        algo_python = rpt.Pelt(model="rbf", jump=1, min_size=minCpG).fit(signal_pelt)
        bkps_python = algo_python.predict(pen=penalty_value)
        forindexgenerate=bkps_python
        if forindexgenerate[-1]==len(signal_pelt.index):
            forindexgenerate[-1]=forindexgenerate[-1]-1
     
        pr=PELT_result(signal_pelt,DMR[0],DMR[1],DMR[2],(signal_pelt.index[forindexgenerate]).tolist())
    except: ### gives error if #cpg is smaller.thats why try-except commannd
  
        pr=PELT_result(signal_pelt,DMR[0],DMR[1],DMR[2],[signal_pelt.index[len(signal_pelt.index)-1]])
    return pr

def run_get_pelt_result(signalchunks):
    signalchunksresult=[]
    for signalchunk in signalchunks:
        signalchunksresult.append(get_pelt_result(signalchunk))
    return signalchunksresult


# In[6]:


signallist=segment_generator()
chunks = [signallist[x:x+percormetDMR] for x in range(0, len(signallist), percormetDMR)]

print(len(chunks))


# In[7]:


multiresult = []

with concurrent.futures.ProcessPoolExecutor() as executor:
    processlist=[]
    for chunk in chunks:
   
        processlist.append(executor.submit(run_get_pelt_result,chunk))
        #algo_python = rpt.Pelt(model="rbf", jump=1, min_size=minCpG).fit(signal)  # written in pure python
    for process in concurrent.futures.as_completed(processlist):
        multiresult=multiresult+process.result()


# In[8]:



allresultdictlist=[]
allresultsegmentinfolist=defaultdict(list)
allresultcombinedsegmentinfodflist=[]
for resultobj in multiresult:
    allresultdictlist.append(resultobj.metpeltsegmentDICT)
    
    allresultcombinedsegmentinfodflist.append(resultobj.metpeltcombinedsegmentDICTinfo)
    
    for key, value in resultobj.metpeltsegmentDICTinfo.items():
        allresultsegmentinfolist[key].append(value)
    
    
allresultdf=pd.DataFrame(allresultdictlist)
allresultsegmentinfolist=dict(allresultsegmentinfolist)

anotherdict={}
for key , value in allresultsegmentinfolist.items():
   
    anotherdict[key]=[x for sublist in value for x in sublist]
    
    
allresultsegmentinfolist=anotherdict

allresultsegmentinfodf=pd.DataFrame.from_dict(allresultsegmentinfolist)


diffcellcolumns=columnnames[:columnnames.index('DMRchrom')]

allresultsegmentinfodf['PELTmax']=allresultsegmentinfodf[diffcellcolumns].max(axis=1)
allresultsegmentinfodf['PELTmin']=allresultsegmentinfodf[diffcellcolumns].min(axis=1)


allresultsegmentinfodf['PELTmax-parentDMRmax']=allresultsegmentinfodf['PELTmax']-allresultsegmentinfodf['parentDMRmax']
allresultsegmentinfodf['PELTmin-parentDMRmin']=allresultsegmentinfodf['PELTmin']-allresultsegmentinfodf['parentDMRmin']


# In[9]:



allresultcombinedsegmentinfodf=pd.concat(allresultcombinedsegmentinfodflist, axis=0)
allresultcombinedsegmentinfodf['PELTmax']=allresultcombinedsegmentinfodf[diffcellcolumns].max(axis=1)
allresultcombinedsegmentinfodf['PELTmin']=allresultcombinedsegmentinfodf[diffcellcolumns].min(axis=1)
allresultcombinedsegmentinfodf['PELTmax-parentDMRmax']=allresultcombinedsegmentinfodf['PELTmax']-allresultcombinedsegmentinfodf['parentDMRmax']
allresultcombinedsegmentinfodf['PELTmin-parentDMRmin']=allresultcombinedsegmentinfodf['PELTmin']-allresultcombinedsegmentinfodf['parentDMRmin']


# In[10]:


dmrchrindex=columnnames.index('DMRchrom')
foroutsubdf=indfdropped.iloc[:,dmrchrindex:]
foroutsubdf=foroutsubdf.reset_index( drop=True)
foroutsubdf=foroutsubdf.drop_duplicates(keep='first')
#foroutsubdf.head()


# In[11]:


outdf=foroutsubdf.merge(allresultdf,how='inner',on=['DMRchrom','DMRstart','DMRend'])
outdf=outdf.rename(columns ={'DMRchrom':'chrom','DMRstart':'start','DMRend':'end'},errors='raise')
outdf.to_csv(outfile,sep="\t",index=False)


allresultsegmentinfodf.to_csv(outsegmentfile,sep="\t",index=False)


# In[12]:


outdfcombined=outdf.copy()
allresultcombinedsegmentinfodfgrouped=allresultcombinedsegmentinfodf.groupby(['parentDMRchrom','parentDMRstart','parentDMRend'])

for name, group in allresultcombinedsegmentinfodfgrouped:
    
    outdfcombined.loc[(outdfcombined['chrom']==name[0]) & (outdfcombined['start']==name[1]) & (outdfcombined['end']==name[2]),'totalPeltSegement']=group.shape[0]-1
outdfcombined.to_csv(combinedoutfile,sep="\t",index=False)
allresultcombinedsegmentinfodf.to_csv(combinedoutsegmentfile,sep="\t",index=False)

