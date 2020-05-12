
'''
Add hypo hyper SM and store final SM and SMselected in the final_sm_folder folder


'''



import sys

import os

import pandas as pd







def addandsave_hypohyper(hypo_path,hyper_path,final_sm_folder,**kwargs):

	hypo_df=pd.read_csv(hypo_path,sep="\t")
	hyper_df=pd.read_csv(hyper_path,sep="\t")

	hyper_df=hyper_df[~hyper_df['NAME'].isin(hypo_df['NAME'])]



	final_sig=pd.concat([hypo_df,hyper_df])

	SMname,SMselected_name=name_for_sm(hypo_path,hyper_path)


	finalPath_SM=final_sm_folder+"/"+SMname
	finalPath_SMselected=final_sm_folder+"/"+SMselected_name
	final_sig.to_csv(finalPath_SM,sep="\t",index=False)
	hyper_df.to_csv(finalPath_SMselected,header = False,sep="\t",index=False)






###genereate the name of SM and SMselected sile
###input is the path of hypo and hyper
def name_for_sm(hypo_path,hyper_path,**kwargs):
	
	hypo_name=os.path.basename(os.path.dirname(hypo_path))
	hypr_name=os.path.basename(os.path.dirname(hyper_path))
	SMname=hypo_name+"_"+hypr_name
	SMselected_name=SMname+"_selected"

	return SMname,SMselected_name





hypo_path=sys.argv[1]

hyper_path=sys.argv[2]

final_sm_folder=sys.argv[3]

addandsave_hypohyper(hypo_path,hyper_path,final_sm_folder)



