#!/usr/bin/env python
# coding: utf-8

# In[1]:


import ruptures as rpt  # our package
from ruptures.metrics import hausdorff
import pandas as pd
import concurrent.futures
import sys
infile=sys.argv[1] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/DMRrelated/ITGAE_patternrecognition/changepointtest/preproocess_Develop/preprocess_ontopmetilene/input_out_mincpg2_intersectedwith_paramA_short.txt_header/ITGAEp_cin_nr0.5_imputed_g1_CD8TIL_3_g2_others_36_default.txt"
minCpG=int(sys.argv[2]) #3
penalty_value = float(sys.argv[3]) #1 
percormetDMR=int(sys.argv[4])  #2 #### for parallal
outfile=sys.argv[5] #infile+"_mincpg_"+str(minCpG)+"pelt.txt"
outsegmentfile=sys.argv[6]

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
    def __init__(self,dmrchrom,dmrstart,dmrend,peltsegmentlist):
        self.dmrchrom=dmrchrom
        self.dmrstart=dmrstart
        self.dmrend=dmrend
        self.peltsegmentlist=peltsegmentlist
       
        self.totalsegment=len(self.peltsegmentlist)-1
        self.metpeltsegmentDICT={'DMRchrom':self.dmrchrom,'DMRstart':self.dmrstart,'DMRend':self.dmrend,"totalPeltSegement":self.totalsegment}
        self.metpeltsegmentDICTinfo={'DMRchrom':self.dmrchrom,'DMRstart':self.dmrstart,'DMRend':self.dmrend,"PeltSegement":self.peltsegmentlist}
        
        


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
        pr=PELT_result(DMR[0],DMR[1],DMR[2],(signal_pelt.index[forindexgenerate]).tolist())
    except: ### gives error if #cpg is smaller.thats why try-except commannd
        
        pr=PELT_result(DMR[0],DMR[1],DMR[2],[signal_pelt.index[len(signal_pelt.index)-1]])
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
allresultsegmentinfolist=[]
for resultobj in multiresult:
    allresultdictlist.append(resultobj.metpeltsegmentDICT)
    allresultsegmentinfolist.append(resultobj.metpeltsegmentDICTinfo)
    
allresultdf=pd.DataFrame(allresultdictlist)
allresultsegmentinfodf=pd.DataFrame(allresultsegmentinfolist)



# In[9]:


dmrchrindex=columnnames.index('DMRchrom')
foroutsubdf=indfdropped.iloc[:,dmrchrindex:]
foroutsubdf=foroutsubdf.reset_index( drop=True)
foroutsubdf=foroutsubdf.drop_duplicates(keep='first')
foroutsubdf.head()


# In[10]:


outdf=foroutsubdf.merge(allresultdf,how='inner',on=['DMRchrom','DMRstart','DMRend'])
outdf=outdf.rename(columns ={'DMRchrom':'chrom','DMRstart':'start','DMRend':'end'},errors='raise')
outdf.to_csv(outfile,sep="\t",index=False)


allresultsegmentinfodf.to_csv(outsegmentfile,sep="\t",index=False)






