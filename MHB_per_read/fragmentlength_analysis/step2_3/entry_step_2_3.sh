start=$SECONDS

bamdir=$1
readnamedir=$2


bamreadnameoutdir=${bamdir}_$( basename ${readnamedir} )_frag

./step2_pipe.sh ${bamdir}  ${readnamedir}  ${bamreadnameoutdir}



./makefrag_my.sh  ${bamreadnameoutdir}

end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"



