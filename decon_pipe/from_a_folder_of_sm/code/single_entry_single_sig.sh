
#to chmod +x all files run the following command
#find . -type f -iname "*.sh" -exec chmod +x {} \;







#the name of the variable file must be decon_pipe_variables.txt
source decon_pipe_variables.txt



SmList=($( find ${SmFolder} ! '(' -name '*_selected' ')' -type f ))



for fl in ${SmList[@]}
do
	sig=$(basename ${fl})
	
	cp ${fl} .
	if [ ${SmFolderType} = COMBINED ]
	then
		hyper_selected_file=${sig}_selected
		cp ${fl}_selected .
	elif [ ${SmFolderType} = HYPO ]
	then
		hyper_selected_file=dummySelected
	elif [ ${SmFolderType} = HYPER ]
	then
		tail -n +2 ${sig} > ${sig}_selected 
		hyper_selected_file=${sig}_selected
	else 
		echo "${SmFolderType} wrong. Exiting..... "
		exit 1
	fi

	echo nowSM=========${sig} 
	echo nowSMselected=========${hyper_selected_file} 


	./pipe_to_generate_mix_to_csx.sh ${sig} ${hyper_selected_file} ${dataFolder}
	

done
