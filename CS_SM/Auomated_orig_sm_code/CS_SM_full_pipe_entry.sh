#! /bin/bash


######

# Sig in hypo or hyper has the name SigMatrix from functional_CS_SM.R

#####


function call_run_CS_SM (){
	ref=$1
	pheno=$2
	gst=$3
	gend=$4

	suffix=$5

	group=${gst}

	

	while (( group <= ${gend} ))
	do
		dirname=g${group}_${suffix}
		mkdir ${dirname}
		./run_CS_SM.sh ${ref} ${pheno} ${dirname} ${group} ${group}

		if [ ${suffix} = hypo ]
		then
			hypoDirs=( "${hypoDirs[@]}" ${dirname} ) 
		else
			hyperDirs=( "${hyperDirs[@]}" ${dirname} ) 
		fi


		

		(( group++ ))
	done
	
}







###############param#######################

refsample=q25d1.txt_inverted
refsample_realhyper=q25d1.txt
phenoclasses=meth_phen_class_irf_only_relevant.txt

gStart=19
gEnd=21

grealStart=4
grealEnd=6


###############param#######################





hypoDirs=()

###### hypo is hard coded
call_run_CS_SM ${refsample} ${phenoclasses} ${gStart} ${gEnd} hypo        

hyperDirs=()
###### hyper is hard coded
call_run_CS_SM ${refsample_realhyper} ${phenoclasses} ${grealStart} ${grealEnd} hyper     





hypohyperSMfolder=combinedSM_hypo_${gStart}_${gEnd}_hyper_${grealStart}_${grealEnd}
mkdir ${hypohyperSMfolder}


echo "hypo dirs==="
echo ${hypoDirs[@]}


echo "hyper dirs==="
echo ${hyperDirs[@]}


for hypodir in ${hypoDirs[@]}
do
	for hyperdir in ${hyperDirs[@]}
	do

		python3 add_hypo_hyper.py ${hypodir}/SigMatrix ${hyperdir}/SigMatrix ${hypohyperSMfolder}
		
	done
done



onlyhypoDIR=Onlyhypo_${gStart}_${gEnd}
mkdir ${onlyhypoDIR}
for hypodir in ${hypoDirs[@]}
do
	cp ${hypodir}/SigMatrix ${onlyhypoDIR}/${hypodir}
done



onlyhyperDIR=Onlyhyper_${grealStart}_${grealEnd}
mkdir ${onlyhyperDIR}
for hyperdir in ${hyperDirs[@]}
do
	cp ${hyperdir}/SigMatrix ${onlyhyperDIR}/${hyperdir}
done



