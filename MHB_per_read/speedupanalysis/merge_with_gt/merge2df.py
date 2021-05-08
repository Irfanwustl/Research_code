#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys

f1=sys.argv[1] #"/Users/irffanalahi/Research/weekly/for_3_24_21/ML/ML_postprocess/dataprepare/testdata/filnamerename/subtracttrainingdata/predict/onlypredictedfile/combine_cellproportion/mergewithgt/mel_dataset_cp2pos_cp1neg.txt_testsize_0.7_model_testfile_allfinal_lenrefCPG_subsetoffinal_cpg2_row_combinedfilename.txt_informative_meltumor_cpg2.txt_notraining.txt_predicted.txt_MEL_TUMOR_proportion.txt_merged.txt"
f2=sys.argv[2] #"/Users/irffanalahi/Research/weekly/for_3_24_21/ML/ML_postprocess/dataprepare/testdata/filnamerename/subtracttrainingdata/predict/onlypredictedfile/combine_cellproportion/mergewithgt/response.txt"

out=sys.argv[3]

f1df=pd.read_csv(f1,sep="\t",index_col=0)
f2df=pd.read_csv(f2,sep="\t",index_col=0)


# In[2]:


df_combined = pd.concat([f1df, f2df], axis=1)
df_combined.to_csv(out,sep="\t",na_rep="NA")

