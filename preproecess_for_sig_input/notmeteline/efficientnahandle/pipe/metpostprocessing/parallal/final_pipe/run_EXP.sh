echo "now run_compartmentmean CD8TILvsCD8PBLmetout" 
./run_compartmentmean.sh CD8tilvsCD8pblpromdataready_all_matrixCin_nr0.5_imputed CD8TILvsCD8PBLmetout CD8P_CD8T_PHENOCLASS.txt


echo "now run_compartmentmean WorkingTILmetout"
./run_compartmentmean.sh promdataready_all_matrixCin_nr0.5_imputed WorkingTILmetout pbltilMELtumor_abulmelMGI_PHENOCLASS.txt


echo "now run_compartmentmean TcellTILvsOthersmetout"
./run_compartmentmean.sh promdatareadyTcellTIL_all_matrixCin_nr0.5_imputed  TcellTILvsOthersmetout melTcellTIL_PHENOCLASS.txt

echo "now run_compartmentmean CD8TILvsOthesmetout"
./run_compartmentmean.sh  promdatareadyCD8TIL_all_matrixCin_nr0.5_imputed  CD8TILvsOthesmetout  melCD8TIL_PHENOCLASS.txt

echo "now run_compartmentmean CD4TILvsOthersmetout"
./run_compartmentmean.sh  promdatareadyCD4TIL_all_matrixCin_nr0.5_imputed  CD4TILvsOthersmetout  melCD4TIL_PHENOCLASS.txt

echo "now run_compartmentmean CD14TILvsOthers"
./run_compartmentmean.sh  promdatareadyCD14TIL_all_matrixCin_nr0.5_imputed  CD14TILvsOthers melCD14TIL_PHENOCLASS.txt
