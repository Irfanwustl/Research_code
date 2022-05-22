start=$SECONDS

dirList=("Adrenal gland" "Base of tongue" "Bladder" "Bones, joints and articular cartilage of limbs" "Brain" "Breast" "Bronchus and lung" "Cervix uteri" "Colon" "Corpus uteri" "Esophagus" "Floor of mouth" "Kidney" "Larynx" "Liver and intrahepatic bile ducts" "Other and ill-defined sites in lip, oral cavity and pharynx" "Other and unspecified parts of biliary tract" "Other and unspecified parts of tongue" "Palate" "Pancreas" "Prostate gland" "Rectosigmoid junction" "Rectum" "Skin" "Stomach" "Thymus" "Thyroid gland" "Uterus, NOS")

parallel -j 8 python3 illumina_retrieve_pairwise.py ::: "${dirList[@]}"


end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"
