reffile=$1
dir=$2
outfol=${dir}_BILGEwgbs
mkdir ${outfol}

dirList=($( find ${dir} -maxdepth 1 -type f -not -path '*/\.*'))

parallel -j 8 python3 illumina_to_blueprint.py ::: ${reffile} ::: ${dirList[@]} ::: ${outfol}
