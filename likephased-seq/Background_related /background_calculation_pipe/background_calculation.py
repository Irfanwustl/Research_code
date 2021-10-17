import pandas as pd
import os
from collections import defaultdict

def decode_files(infile, celltype):
    sample_name = os.path.basename(infile.split('_sorted')[0])
    mincpg = int((infile.split('_mincpg')[1]).split('_')[0])
    
    row = defaultdict(list)

    row['Mixture']=[sample_name]
    row['mincpg']=[mincpg]
    '''
    row.append(sample_name)
    row.append(mincpg)
    '''
    
    indf = pd.read_csv(infile, sep="\t")
    


    #######################
    totalreadlist=indf['ReadName'].tolist()
    totalreadCT=len([i for i in totalreadlist if celltype in i]) 
    totalreadnonCT=len([i for i in totalreadlist if celltype not in i])
    row['totalreadCT']=[totalreadCT]
    row['totalreadnonCT']=[totalreadnonCT]
    ######################
    
    accepteddf = indf[indf['finalacceptedfor'] == celltype]
    rejecteddf = indf[indf['finalrejectedfor'].str.contains(celltype)]
    
    acc_rname = accepteddf['ReadName'].tolist()
    acceptedtrueCTcount = len([i for i in acc_rname if celltype in i]) 
    acceptedfalseCTcount = len(acc_rname) - acceptedtrueCTcount
    
    row['acceptedtrueCTcount']=[acceptedtrueCTcount]
    row['acceptedfalseCTcount']=[acceptedfalseCTcount]
    '''
    row.append(acceptedtrueCTcount)
    row.append(acceptedfalseCTcount)
    '''
    
    acc_ratio = -1.0
    if acceptedtrueCTcount + acceptedfalseCTcount != 0.0:
        acc_ratio = acceptedtrueCTcount / (acceptedtrueCTcount + acceptedfalseCTcount)
    
    row['true_pos/all_pos']=[acc_ratio]
    #row.append(acc_ratio)
    
    rej_rname = rejecteddf['ReadName'].tolist()
    rejectedtrueCTcount = len([i for i in rej_rname if celltype not in i]) 
    rejectedfalseCTcount = len(rej_rname) - rejectedtrueCTcount
    
    row['rejectedtrueCTcount']=[rejectedtrueCTcount]
    row['rejectedfalseCTcount']=[rejectedfalseCTcount]
    '''
    row.append(rejectedtrueCTcount)
    row.append(rejectedfalseCTcount)
    '''
    
    rej_ratio = -1.0
    if rejectedtrueCTcount + rejectedfalseCTcount != 0.0:
        rej_ratio = rejectedtrueCTcount / (rejectedtrueCTcount + rejectedfalseCTcount)
    
    
    row['true_neg/all_neg']=[rej_ratio]
    #row.append(rej_ratio)
    
    tempdf=pd.DataFrame.from_dict(row)

    #tempdf = pd.DataFrame(columns=cols)
    #tempdf.loc[len(tempdf)] = row
    
    return tempdf
