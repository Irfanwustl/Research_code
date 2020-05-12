
#to chmod +x all files run the following command
#find . -type f -iname "*.sh" -exec chmod +x {} \;







#here sig and hyper_selected_file will be generated then for different sig full csx will be run




##parm1=sig, parm2=hyper_selected, param3=mixin

sig=SigMatrix_FC_threshold_2_g20_SigMatrix_FC_threshold_2__realhyper_g5_combined #### Sig
hyper_selected_file=SigMatrix_FC_threshold_2_g20_SigMatrix_FC_threshold_2__realhyper_g5_selected

mixin=data




./pipe_to_generate_mix_to_csx.sh ${sig} ${hyper_selected_file} ${mixin}