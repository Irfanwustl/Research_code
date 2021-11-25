#!/usr/bin/env python
# coding: utf-8

# In[1]:


from collections import defaultdict
from operator import add
import pandas as pd
import pysam
import time
import sys
import numpy as np



bamfile =sys.argv[1] #'/Users/irffanalahi/Research/Research_code/gitignorefolder/MHB_per_read/softreadcounting/testtheidea/softRD_pileup/CD4allrange_NR_1000000_insilmix41_sorted'

score_matrix_file =sys.argv[2] #'/Users/irffanalahi/Research/Research_code/gitignorefolder/MHB_per_read/softreadcounting/testtheidea/softRD_pileup/BL14_all_matrixCin_nr0.4_imputed_rowmean.txt_bg_intesectedwith_BL14ateast.2DMRs.txt_othermean.txt'


outfile=sys.argv[3]

deltagreaterforpositive=0  ##############>0

deltasmallerfornegative=0 ############<0


mapping_quality=40
base_quality=20
maxpileupdepth=10000

score_matrix_df = pd.read_csv(score_matrix_file, sep='\t', index_col=['chrom','start'])

score_matrix_dict = score_matrix_df.to_dict(orient='index')


# In[2]:


input_bam = pysam.AlignmentFile(bamfile, 'rb')


# In[3]:


scorecolumns=score_matrix_df.columns
scoredict=defaultdict(list)
scorehyperdict=defaultdict(list)


# In[4]:


hypoCpGdict=defaultdict(list)
lenhypoCpGdict=defaultdict(list)
hyperCpGdict=defaultdict(list)
lenhyperCpGdict=defaultdict(list)


# In[5]:


for cindex, cpg_scores in score_matrix_dict.items():
    
    Refchrom=cindex[0]
    
    hypoFRAGset=set()
    hyperFRAGset=set()
 
    for pileupcolumn in input_bam.pileup(Refchrom, start=cindex[1],ignore_orphans=False,ignore_overlaps=False, stop=cindex[1]+2,truncate=True, max_depth=maxpileupdepth, min_mapping_quality=mapping_quality,min_base_quality=base_quality):
        
      
        
        ######sanity check depth
        #print(f"Coverage at CpG: {index} = {pileupcolumn.nsegments}")
        
        
        
        for pileupread in pileupcolumn.pileups:
            
          
         
        
            
            if not pileupread.is_del: # and not pileupread.is_refskip:



                

                #assert pileupread.alignment.is_paired is True
                #if pileupread.alignment.is_paired==False:
                 #   continue
                
                #assert pileupread.alignment.is_proper_pair is True
                #if pileupread.alignment.is_proper_pair==False:
                 #   continue
                
                #assert pileupread.alignment.is_qcfail is False
                #if pileupread.alignment.is_qcfail==True:
                 #   continue
                    
                #assert pileupread.alignment.is_unmapped is False
                
                
              
                    
                if pileupread.alignment.is_unmapped==True:
                    continue
                
                
                #assert pileupread.alignment.is_duplicate is False
                if pileupread.alignment.is_duplicate == True:
                    continue
                    
        
                    
                
                
                assert pileupread.alignment.has_tag("XB") or pileupread.alignment.has_tag("YD")


                if pileupread.alignment.has_tag("XB"): # gem3 / blueprint tag
                    xb_tag = pileupread.alignment.get_tag("XB") # XB:C = Forward / Reference was CG
                    # TODO: Double check one or two of these gem3 tags manually.
                    if xb_tag == "C":
                        bisulfite_parent_strand_is_reverse = False
                    elif xb_tag == "G": # XB:G = Reverse / Reference was GA
                        bisulfite_parent_strand_is_reverse = True
                elif pileupread.alignment.has_tag("YD"): # Biscuit tag
                    yd_tag = pileupread.alignment.get_tag("YD")
                    if yd_tag == "f": # Forward = C→T
                        bisulfite_parent_strand_is_reverse = False
                    elif yd_tag == "r": # Reverse = G→A
                        bisulfite_parent_strand_is_reverse = True
                
                #print(cpg_location[0], cpg_location[1])
                
                prefpos=pileupcolumn.reference_pos
                
              
                    
                    
                if (prefpos==cindex[1]) and (bisulfite_parent_strand_is_reverse == True):
                    continue
                if (prefpos==cindex[1]+1) and (bisulfite_parent_strand_is_reverse == False):
                    continue
                
                
                readbase = (pileupread.alignment.query_sequence[pileupread.query_position]).upper()
                
                
                
                
                
                Readname=pileupread.alignment.query_name
                
                
                    
               
                accpeted=0
        
        

        
               
                if bisulfite_parent_strand_is_reverse==False:
                    
                    if readbase=='T':
                        
                        if Readname in hypoFRAGset:
                            continue
                        else:
                            hypoFRAGset.add(Readname)
                        
                        
                        
                        accpeted=-1

                        if len(hypoCpGdict[Readname])==0:
                            hypoCpGdict[Readname]=[[Refchrom+":"+str(cindex[1])]]


                        elif len(hypoCpGdict[Readname])==1:

                            hypoCpGdict[Readname]=[hypoCpGdict[Readname][0]+[Refchrom+":"+str(cindex[1])]]

                        else:
                            print('prob in hypoCpGdict')
                            sys.exit(1)


                        if len(lenhypoCpGdict[Readname])==0:
                            lenhypoCpGdict[Readname]=[1]
                        elif len(lenhypoCpGdict[Readname])==1:
                            lenhypoCpGdict[Readname]=[lenhypoCpGdict[Readname][0]+1]
                        else:
                            print('prob in lenhypoCpGdict')
                            sys.exit(1)


                    elif readbase=='C':
                        accpeted=1
                        
                        if Readname in hyperFRAGset:
                            continue
                        else:
                            hyperFRAGset.add(Readname)
                        
                        
                        if len(hyperCpGdict[Readname])==0:
                            hyperCpGdict[Readname]=[[Refchrom+":"+str(cindex[1])]]

                        elif len(hyperCpGdict[Readname])==1:
                            hyperCpGdict[Readname]=[hyperCpGdict[Readname][0]+[Refchrom+":"+str(cindex[1])]]

                        else:

                            print('prob in hyperCpGdict')
                            sys.exit(1)

                        if len(lenhyperCpGdict[Readname])==0:
                            lenhyperCpGdict[Readname]=[1]
                        elif len(lenhyperCpGdict[Readname])==1:

                            lenhyperCpGdict[Readname]=[lenhyperCpGdict[Readname][0]+1]
                        else:
                            print('prob in lenhyperCpGdict')
                            sys.exit(1)

                        




                elif bisulfite_parent_strand_is_reverse==True:
                    if readbase=='A':
                        
                        if Readname in hypoFRAGset:
                            continue
                        else:
                            hypoFRAGset.add(Readname)
                        
                        
                        accpeted=-1

                        if len(hypoCpGdict[Readname])==0:
                            hypoCpGdict[Readname]=[[Refchrom+":"+str(cindex[1])]]

                        elif len(hypoCpGdict[Readname])==1:
                            hypoCpGdict[Readname]=[hypoCpGdict[Readname][0]+[Refchrom+":"+str(cindex[1])]]

                        else:
                            print('prob in hypoCpGdict')
                            sys.exit(1)



                        if len(lenhypoCpGdict[Readname])==0:
                            lenhypoCpGdict[Readname]=[1]
                        elif len(lenhypoCpGdict[Readname])==1:

                            lenhypoCpGdict[Readname]=[lenhypoCpGdict[Readname][0]+1]
                        else:
                            print('prob in lenhypoCpGdict')
                            sys.exit(1)
                    elif readbase=='G':
                        
                        accpeted=1
                        if Readname in hyperFRAGset:
                            continue
                        else:
                            hyperFRAGset.add(Readname)
                        
                        if len(hyperCpGdict[Readname])==0:
                            hyperCpGdict[Readname]=[[Refchrom+":"+str(cindex[1])]]

                        elif len(hyperCpGdict[Readname])==1:
                            hyperCpGdict[Readname]=[hyperCpGdict[Readname]+[Refchrom+":"+str(cindex[1])]]

                        else:

                            print('prob in hyperCpGdict')
                            sys.exit(1)

                        if len(lenhyperCpGdict[Readname])==0:
                            lenhyperCpGdict[Readname]=[1]
                        elif len(lenhyperCpGdict[Readname])==1:

                            lenhyperCpGdict[Readname]=[lenhyperCpGdict[Readname][0]+1]
                        else:
                            print('prob in lenhyperCpGdict')
                            sys.exit(1)
                    
                    
                 
                
               
                
                
                
                if accpeted==-1 :
                   
                    



                    smrow=list(cpg_scores.values())



                    smrow=np.array(smrow)


                    if len(scoredict[Readname])==0:
                            scoredict[Readname]=list(accpeted*smrow)
                    else:
                        scoredict[Readname]=list(np.array(scoredict[Readname])+(accpeted*smrow))
                
                elif accpeted==1 :
                    
                    smrow=list(cpg_scores.values())



                    smrow=np.array(smrow)


                    if len(scorehyperdict[Readname])==0:
                            scorehyperdict[Readname]=list(-1*smrow)
                    else:
                        scorehyperdict[Readname]=list(np.array(scorehyperdict[Readname])+(-1*smrow))

                
                
                    ''' not sure if i will use  Reference. For now: dont use reference 
                    if bisulfite_parent_strand_is_reverse==False:
                        reference_bp = pileupread.alignment.get_reference_sequence()[pileupcolumn.reference_pos-pileupread.alignment.reference_start].upper()
                        if reference_bp=='C':
                            print(prefpos)
                            print(pileupcolumn.reference_pos-pileupread.alignment.reference_start)
                            print(pileupread.alignment.get_aligned_pairs(with_seq=True))
                            sys.exit(1)
                    '''
   

    


# In[6]:





# In[7]:


scoredf=pd.DataFrame.from_dict(scoredict, orient='index',columns=scorecolumns)
scoredf.head()


# In[8]:


scorehyperdf=pd.DataFrame.from_dict(scorehyperdict, orient='index',columns=scorecolumns)
scorehyperdf.head()


# In[9]:


totalhyperdf=scorehyperdf[~scorehyperdf.index.isin(scoredf.index.tolist())]
totalhyperdf.head()


# In[10]:


scoredf.shape


# In[11]:


totalhyperdf.shape


# In[15]:


scoredf=pd.concat([scoredf,totalhyperdf],axis=0)
scoredf.shape


# In[17]:


if scoredf[scoredf.index.duplicated].shape[0]!=0:
    print("prob in generation of scoreDF")
    sys.exit(1)


# In[18]:


hypoCpGdf=pd.DataFrame.from_dict(hypoCpGdict, orient='index',columns=['hypoCpG'])
lenhypoCpGdf=pd.DataFrame.from_dict(lenhypoCpGdict, orient='index',columns=['LENhypoCpG'])
hyperCpGdf=pd.DataFrame.from_dict(hyperCpGdict, orient='index',columns=['hyperCpG'])
lenhyperCpGdf=pd.DataFrame.from_dict(lenhyperCpGdict,orient='index',columns=['LENhyperCpG'])

if hyperCpGdf.shape[0]!=lenhyperCpGdf.shape[0]:
    print("problem in hyper merging")
    sys.exit(1)
    
hyperinfo=pd.concat([hyperCpGdf,lenhyperCpGdf],axis=1)



if hypoCpGdf.shape[0]!=lenhypoCpGdf.shape[0]:
    print("problem in hyper merging")
    sys.exit(1)
    
hypoinfo=pd.concat([hypoCpGdf,lenhypoCpGdf],axis=1)

    
    
outdf=scoredf.merge(hypoinfo,left_index=True,right_index=True,how='left')
    
outdf=outdf.merge(hyperinfo,left_index=True,right_index=True,how='left')


if scoredf.shape[0]!=outdf.shape[0]:
    print("somehow wrong")
    sys.exit(1)


# In[19]:


outdf['LENhyperCpG'].fillna(0, inplace=True)
outdf.head()


# In[20]:


outdf['LENhypoCpG'].fillna(0, inplace=True)
outdf.head()


# In[21]:


outdf['total_cpg']=outdf['LENhypoCpG']+outdf['LENhyperCpG']

outdf['LENhypoCpG_BY_total_cpg']=outdf['LENhypoCpG']/outdf['total_cpg']

max_value = outdf['LENhypoCpG_BY_total_cpg'].max()
min_value=outdf['LENhypoCpG_BY_total_cpg'].min()

if max_value >1 or min_value<0:
    print('max,min error')
    sys.exit(1)

outdf.head()


# In[22]:


outdf['maxscoredCT_beforeCpGweight']=(outdf[scorecolumns]).idxmax(axis=1)
outdf.head()


# In[23]:


outdf['maxscore_beforeCpGweight']=outdf[scorecolumns].max(axis=1)
outdf.head()


# In[24]:


outdfcpgweighted=outdf.copy()


# In[25]:


for scolumn in scorecolumns:
    outdfcpgweighted[scolumn]=outdfcpgweighted[scolumn]*outdfcpgweighted['LENhypoCpG_BY_total_cpg']


# In[26]:


outdfcpgweighted.head()


# In[27]:


outdf.head()


# In[28]:


outdfcpgweighted['maxscoredCT']=(outdfcpgweighted[scorecolumns]).idxmax(axis=1)
outdfcpgweighted.head()


# In[29]:


outdfcpgweighted['maxscore']=outdfcpgweighted[scorecolumns].max(axis=1)
outdfcpgweighted.head()


# In[30]:


outdfcpgweighted['deltabasedfragassignment']='NotAssigned'
outdfcpgweighted.loc[outdfcpgweighted['maxscore']>deltagreaterforpositive,'deltabasedfragassignment']=outdfcpgweighted.loc[outdfcpgweighted['maxscore']>deltagreaterforpositive,'maxscoredCT']
outdfcpgweighted.head()


# In[31]:


ctposscoredict= defaultdict(list)
ctposfragdict= defaultdict(list)
for score in scorecolumns:
    deltabasedfragassigned=outdfcpgweighted['deltabasedfragassignment'].tolist()
    if score in deltabasedfragassigned:
        temp_posscore=outdfcpgweighted.loc[outdfcpgweighted['deltabasedfragassignment']==score,'maxscore'].tolist()
        temptotal_posscore=sum(temp_posscore)
        temp_posfrag=len(temp_posscore)
    
    else:
        temptotal_posscore=0
        temp_posfrag=0
        
    ctname=score.replace('-others','')
    
    ctposscoredict[ctname].append(temptotal_posscore)

    ctposfragdict[ctname].append(temp_posfrag)


# In[32]:


ctposscoredf=pd.DataFrame.from_dict(ctposscoredict)
ctposfragdf=pd.DataFrame.from_dict(ctposfragdict)
ctposscoredf.head()


# In[33]:


ctposscoredf.to_csv(outfile+"_posscore.txt",sep="\t",index=False)
ctposfragdf.to_csv(outfile+"_posfrag.txt",sep="\t",index=False)


# In[34]:



outdf.to_csv(outfile+"_rawscoreStats.txt",sep="\t")
outdfcpgweighted.to_csv(outfile+"_binnedstats.txt",sep="\t")


# In[35]:


hyperinfo.to_csv(outfile+"_exclusivehyperinfo.txt",sep="\t")


# In[36]:




