


import sys

import os.path
from os import path

import pandas as pd




def cal_corr(col1,col2,meth):
	correlation = col1.corr(col2,method=meth)
	return correlation




healthy_info_file="healthy_samples_used_in_recordPerf.py.txt" ####### must be this name

cutoff=0.0012


sig=sys.argv[1]

combine_csx=pd.read_csv(sys.argv[2],sep="\t")

merged_with_groundtruth=pd.read_csv(sys.argv[3],sep="\t")

masterperf=sys.argv[4]


if path.exists(masterperf):
	masterperfdf=pd.read_csv(masterperf,sep="\t")
else:
	masterperfdf=pd.DataFrame(columns=['SM','TIL_pear','EPCAM_pear','TIL_spear','EPCAM_spear','number_of_TIL_detected_in_patients','number_of_EPCAM_detected_in_patients','number_of_EPCAM_or_TIL_detected_in_patient','number_of_TIL_detected_in_healthy','number_of_EPCAM_detected_in_healthy','number_of_EPCAM_or_TIL_detected_in_healthy'])


############## count#########################################

with open(healthy_info_file) as f:
    healthySamples = f.readlines()
#remove whitespace characters like `\n` at the end of each line
healthySamples = [x.strip() for x in healthySamples] 



combine_csx_patients=combine_csx[~combine_csx['Mixture'].isin(healthySamples)]

combine_csx_healthy=combine_csx[combine_csx['Mixture'].isin(healthySamples)]



combine_csx_patients_tilcount=len(combine_csx_patients[combine_csx_patients['TIL']>cutoff])
combine_csx_patients_EPCAMcount=len(combine_csx_patients[combine_csx_patients['EPCAM']>cutoff])
combine_csx_patients_til_or_EPCAMcount=len(combine_csx_patients[(combine_csx_patients['TIL']>cutoff) | (combine_csx_patients['EPCAM']>cutoff)])




combine_csx_healthy_tilcount=len(combine_csx_healthy[combine_csx_healthy['TIL']>cutoff])
combine_csx_healthy_EPCAMcount=len(combine_csx_healthy[combine_csx_healthy['EPCAM']>cutoff])
combine_csx_healthy_til_or_EPCAMcount=len(combine_csx_healthy[(combine_csx_healthy['TIL']>cutoff) | (combine_csx_healthy['EPCAM']>cutoff)])




############## correlation #########################################

TIL_pear=cal_corr(merged_with_groundtruth['TIL'],merged_with_groundtruth['tsize_sld_mul_rnacd45'],'pearson')
TIL_spear=cal_corr(merged_with_groundtruth['TIL'],merged_with_groundtruth['tsize_sld_mul_rnacd45'],'spearman')

EPCAM_pear=cal_corr(merged_with_groundtruth['EPCAM'],merged_with_groundtruth['tsize_sld_mul_rnaepcam'],'pearson')
EPCAM_spear=cal_corr(merged_with_groundtruth['EPCAM'],merged_with_groundtruth['tsize_sld_mul_rnaepcam'],'spearman')





#################### construct and add the row ##############################
new_row={'SM':sig,'TIL_pear':TIL_pear,'EPCAM_pear':EPCAM_pear,'TIL_spear':TIL_spear,'EPCAM_spear':EPCAM_spear,'number_of_TIL_detected_in_patients':combine_csx_patients_tilcount,'number_of_EPCAM_detected_in_patients':combine_csx_patients_EPCAMcount,'number_of_EPCAM_or_TIL_detected_in_patient':combine_csx_patients_til_or_EPCAMcount,'number_of_TIL_detected_in_healthy':combine_csx_healthy_tilcount,'number_of_EPCAM_detected_in_healthy':combine_csx_healthy_EPCAMcount,'number_of_EPCAM_or_TIL_detected_in_healthy':combine_csx_healthy_til_or_EPCAMcount}
masterperfdf = masterperfdf.append(new_row, ignore_index=True)

masterperfdf.to_csv(masterperf,sep="\t",index=False)




















