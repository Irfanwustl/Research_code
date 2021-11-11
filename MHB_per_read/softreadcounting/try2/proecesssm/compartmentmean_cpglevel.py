#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import re

import sys
biggerfile=sys.argv[1] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/metpostprocess/troubleshhoting/BLthirteen_all_matrixCin_nr0.5_imputed_rowmean_head1000.txt_bg_intersectedbg/BLthirteen_all_matrixCin_nr0.5_imputed_g1_M0_3_g2_others_36.txt_bg_cin.txt"
phenfile=sys.argv[2] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/metpostprocess/troubleshhoting/BL13PhenoClass.txt"
outfile=sys.argv[3]  #"/Users/irffanalahi/Research/Research_code/gitignorefolder/metpostprocess/troubleshhoting/out4.txt"
biggerdf=pd.read_csv(biggerfile,sep="\t",header=None,skiprows=1)
pheno=pd.read_csv(phenfile,sep="\t", header=None, index_col=0)

biggerdf.head()


# In[2]:


def headerfix(existingcolnames):

    m = re.search('g1_(.+?)_\d+_g2', biggerfile)
    if m:
        found = m.group(1)

    else:
        print("cell type not found", biggerfile)
        print("exiting")

        sys.exit(1)

    celltype = found
    
  
    
    
    newcolnames=["DMRchrom","DMRstart","DMRend","DMRname"]
    return celltype,newcolnames

def comparmentwisdiff(newdf,celltype):
    cells=(pheno.index).tolist()

    compartmendeltalist=[]
    for cell in cells:
        if cell!=celltype:
            tempdelta=celltype+"-"+cell
            newdf[tempdelta]=newdf[celltype]-newdf[cell]

            compartmendeltalist.append(tempdelta)




    newdf['maxCompartmentwisedelta']=newdf[compartmendeltalist].max(axis=1)
    newdf['minCompartmentwiseDelta']=newdf[compartmendeltalist].min(axis=1)







    return newdf


# In[3]:


with open (biggerfile) as f:
    line=f.readline()
    line=line.split("\n")
    colnames=line[0].split("\t")


# In[4]:


thatcell,furthercols=headerfix(colnames)
totalcols=colnames+furthercols




biggerdf.columns=totalcols

biggerdf.head()
biggerdf=biggerdf.drop(['shouldbechrom', 'pos'],axis=1)


# In[5]:








compartdf=comparmentwisdiff(biggerdf,thatcell)




duplicateRowsDF = compartdf[compartdf.duplicated(['chrom','start','end'])]

if duplicateRowsDF.shape[0]>0:
    print("Duplicate Rows:", duplicateRowsDF, sep='\n')

compartdf.to_csv(outfile,sep="\t",index=False)

