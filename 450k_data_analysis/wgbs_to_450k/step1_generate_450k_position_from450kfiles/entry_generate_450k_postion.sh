
####parm=450k like ours sorted folder (like tcga my preprocessed data) 
meth450kFolder=$1



meth450kFolderAllmatrix=${meth450kFolder}AllMatrix


meth450kposition=${meth450kFolderAllmatrix}OnlyPosition



./run_cyber_in_bedgraphEndingNoheader.sh $meth450kFolder $meth450kFolderAllmatrix


cut -f 1-3 $meth450kFolderAllmatrix > ${meth450kposition}




