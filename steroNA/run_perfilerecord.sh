allmatciberin=$1

outnafolder=${allmatciberin}_NA
mkdir ${outnafolder}

outnonafolder=${allmatciberin}_NoNA
mkdir ${outnonafolder}


python3 perfilerecord.py ${allmatciberin} ${outnafolder} ${outnonafolder}

