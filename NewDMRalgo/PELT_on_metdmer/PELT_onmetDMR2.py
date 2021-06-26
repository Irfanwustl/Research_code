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

infile=sys.argv[1] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/DMRrelated/ITGAE_patternrecognition/changepointtest/preproocess_Develop/preprocess_ontopmetilene/Again/ITGAEp_cin_nr0.5_imputed_g1_CD8TIL_3_g2_others_36_default_ERICH1.txt" 
minCpG=int(sys.argv[2]) #3
penalty_value =float(sys.argv[3]) #3.5  #1 
percormetDMR=int(sys.argv[4])  #2 #### for parallal
outfile=sys.argv[5]  #infile+"_mincpg_"+str(minCpG)+"pelt.txt" 
outsegmentfile= sys.argv[6] #infile+"_mincpg_"+str(minCpG)+"pelt_seginfo.txt"

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
        self.dmrchrom=dmrchrom
        self.dmrstart=dmrstart
        self.dmrend=dmrend
        self.peltsegmentlist=peltsegmentlist
        self.fullDMRcondnumber=np.linalg.cond(self.underlyingdf,p=2)
        self.totalsegment=len(self.peltsegmentlist)-1
        self.metpeltsegmentDICT={'DMRchrom':self.dmrchrom,'DMRstart':self.dmrstart,'DMRend':self.dmrend,"totalPeltSegement":self.totalsegment,"conditionnumber":self.fullDMRcondnumber}
        self.metpeltsegmentDICTinfo=self.recordPeltDMR() #{'DMRchrom':self.dmrchrom,'DMRstart':self.dmrstart,'DMRend':self.dmrend,"PeltSegement":self.peltsegmentlist}
        
    def recordPeltDMR(self):
        underlyingdfavg=self.underlyingdf.mean(axis=0)
       
        underlyingdfmax=underlyingdfavg.max()
        underlyingdfmin=underlyingdfavg.min()
        
        outdict=defaultdict(list)
        prevend=self.dmrstart-1
        
        for peltsegment in self.peltsegmentlist:
            outdict['chrom'].append(peltsegment[0])
            outdict['start'].append(prevend+1)
            outdict['end'].append(peltsegment[2])
            
            
            corresunderlyingdfstart=prevend
            corresunderlyingdfend=peltsegment[2]
            corressdf=self.underlyingdf.loc[(peltsegment[0], corresunderlyingdfstart, corresunderlyingdfstart+2):(peltsegment[0], corresunderlyingdfend-2, corresunderlyingdfend), :]
            
            
            corresscondnumber=np.linalg.cond(corressdf,p=2)
            corressavgdiff=corressdf.mean(axis=0) 
            corressavgdict=corressavgdiff.to_dict()
            
            #####distances#########
            cosdistance=distance.cosine(corressavgdiff,underlyingdfavg)
            eucliddistance=distance.euclidean(corressavgdiff,underlyingdfavg)
            corrdistance=distance.correlation(corressavgdiff,underlyingdfavg)
            #####distances#########
            
            
            
            
            
           
           
            
            
            
            outdict['conditionnumber'].append(corresscondnumber)
            outdict['parentDMRconditionnumber'].append(self.fullDMRcondnumber)
            outdict['conditionnumber/parentDMRconditionnumber'].append(corresscondnumber/self.fullDMRcondnumber)
            
            outdict['parentDMRchrom'].append(self.dmrchrom)
            outdict['parentDMRstart'].append(self.dmrstart)
            outdict['parentDMRend'].append(self.dmrend)
            
            
            
            
            outdict['cos_distance'].append(cosdistance)
            outdict['euclid_distance'].append(eucliddistance)
            outdict['correlation_distance'].append(corrdistance)
            
            for key, value in corressavgdict.items():
                outdict[key].append(value)
            
            #print(outdict)
            #sys.exit(1)
            outdict['parentDMRmax'].append(underlyingdfmax)
            outdict['parentDMRmin'].append(underlyingdfmin)
            
            prevend=peltsegment[2]
        
        outdict=dict(outdict)
        if self.peltsegmentlist[len(self.peltsegmentlist)-1][2]!=self.dmrend:
            print(self.dmrchrom,self.dmrstart,self.dmrend)
            print("final pelt seg notin DMR end")
        return outdict
            


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
for resultobj in multiresult:
    allresultdictlist.append(resultobj.metpeltsegmentDICT)
    
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


dmrchrindex=columnnames.index('DMRchrom')
foroutsubdf=indfdropped.iloc[:,dmrchrindex:]
foroutsubdf=foroutsubdf.reset_index( drop=True)
foroutsubdf=foroutsubdf.drop_duplicates(keep='first')
#foroutsubdf.head()


# In[10]:


outdf=foroutsubdf.merge(allresultdf,how='inner',on=['DMRchrom','DMRstart','DMRend'])
outdf=outdf.rename(columns ={'DMRchrom':'chrom','DMRstart':'start','DMRend':'end'},errors='raise')
outdf.to_csv(outfile,sep="\t",index=False)


allresultsegmentinfodf.to_csv(outsegmentfile,sep="\t",index=False)

