import time
import os
import sys


def normal_for_fromat(str_list):
	remain=""
	wc=0
	while wc < len(str_list):
		if wc == 0:
			remain=str_list[0]
		else:
			remain=remain+"\t"+str_list[wc]
	
		wc=wc+1
	remain=remain+"\n"
	return remain


def prep_to_write(str_list,mval):
	remain=""
	wc=0
	while wc < len(str_list):
		if wc  >= 1:
			remain=remain+"\t"+str(mval-float(str_list[wc]))  ############################################
	
		wc=wc+1
	remain=remain+"\n"
	return remain






combined_sig=sys.argv[1]   ####mix_file
hyper_selected_file=sys.argv[2]

out_dir=sys.argv[3] ####################### mix



out_file=out_dir+"/"+os.path.basename(combined_sig)+"_selectedinverted"  ###################mix

max_value=100 ########################## mix

with open (combined_sig) as f_combinedSig_in:

	with open (out_file,'w') as fout:
		while True:
			f_combinedSig_line=f_combinedSig_in.readline() 
			if f_combinedSig_line:
				if f_combinedSig_line.strip():
					str_comb_list=f_combinedSig_line.split()
					comb_pos=str_comb_list[0]
					str_to_write=normal_for_fromat(str_comb_list)
					with open (hyper_selected_file) as f_hperSel_in:
						while True:
							hs_line=f_hperSel_in.readline() 
							if hs_line:
								if hs_line.strip():
									str_hs=hs_line.split()
									hs_pos=str_hs[0]

									if hs_pos==comb_pos:
										#str_to_write=comb_pos+"\t"+prep_to_write(str_hs,max_value)
										str_to_write=comb_pos+prep_to_write(str_comb_list,max_value)
										break
							else:
								break
				fout.write(str_to_write)
			else:
				break





