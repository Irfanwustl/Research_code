
metout=$1
imputedfile=$2
phenofile=$3








qcut=0.05
diffcut=0.1
meththrsholdpassed=${metout}_q${qcut}_diff${diffcut}


echo "now run_metthresholdpassed"

./run_metthresholdpassed.sh ${metout} ${qcut} ${diffcut} ${meththrsholdpassed}



meththrsholdpassedhypo=${meththrsholdpassed}_hypo
meththrsholdpassedhyper=${meththrsholdpassed}_hyper

mkdir ${meththrsholdpassedhypo}
mkdir ${meththrsholdpassedhyper}

cp ${meththrsholdpassed}/*hypo.txt ${meththrsholdpassedhypo}/
cp ${meththrsholdpassed}/*hyper.txt ${meththrsholdpassedhyper}/




#####then only hypo file. But hyper is storred up there. If necessary, can manipulate later#######

addedcol=${meththrsholdpassedhypo}_addedcol

echo "now run_driver_driver_compartmentmean_parallal"

./run_driver_driver_compartmentmean_parallal.sh ${imputedfile} ${meththrsholdpassedhypo} ${phenofile} ${addedcol}


echo "now run_plotter"

./run_plotter.sh ${addedcol}


