
#to chmod +x all files run the following command
#find . -type f -iname "*.sh" -exec chmod +x {} \;







#here sig and hyper_selected_file will be generated then for different sig full csx will be run




##parm1=sig, parm2=hyper_selected, param3=mixin

sig=SM_1000_1000_median_ref_forag_phencomp.txt_cohen2_5000_p200_o200_SM_yod93.txt #### Sig
#hyper_selected_file=dummy_s.txt

mixin=CRC_SM_1000_1000




./pipe_to_generate_mix_to_csx.sh ${sig} ${hyper_selected_file} ${mixin}