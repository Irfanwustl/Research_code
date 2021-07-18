#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys
import os.path

rowmeanfile=sys.argv[1] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/DMRrelated/ITGAE_patternrecognition/changepointtest/preproocess_Develop/ITGAEandERICH1_cin_nr0.5_imputed_rowmean.txt"

phenfile=sys.argv[2] #"/Users/irffanalahi/Research/Research_code/gitignorefolder/DMRrelated/ITGAE_patternrecognition/changepointtest/preproocess_Develop/LTMEourCD8TILLwithBLOURPBLPhenoClass.txt"

outfolder=sys.argv[3]


pheno=pd.read_csv(phenfile,sep="\t", header=None, index_col=0)

rowmeandf=pd.read_csv(rowmeanfile,sep="\t",index_col=0)


# In[2]:


def comparmentwisdiff():
    cells=(pheno.index).tolist()

    for celltype in cells:

        newdf=pd.DataFrame()
        for cell in cells:
            if cell!=celltype:
                tempdelta=celltype+"-"+cell
                newdf[tempdelta]=rowmeandf[celltype]-rowmeandf[cell]

        outfile=outfolder+"/"+os.path.basename(rowmeanfile)+"_compdeltafor_g1_"+celltype+".txt"
        newdf.to_csv(outfile,sep="\t")       


# In[3]:


comparmentwisdiff()


