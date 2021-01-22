infile=$1 #no header. if header output will be no head
notoverfile=$2

outname=${infile}_notovwith_${notoverfile}



bedtools intersect -a ${infile} -b ${notoverfile} -v > ${outname}
