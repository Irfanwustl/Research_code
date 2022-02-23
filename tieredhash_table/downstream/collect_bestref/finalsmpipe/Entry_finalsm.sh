start=$SECONDS



bestreffile=$1 #'/Users/irffanalahi/Research/Research_update/SoftRD/hashtable_stats/tieredApproach/BL22_groupv2/All/Alllinked/fromBilge/allct_subset_linecount_txt_filelist.txt'


groupnumber=$2  #4
#####it can be both position and final SM like locations
locationofrefs=$3   #'/Users/irffanalahi/Research/Research_update/SoftRD/hashtable_stats/tieredApproach/BL22_groupv2/All/Alllinked/towardsFinalRef/input'
outdir=${locationofrefs}_towardsSM     #locationofrefs+"_bestref"







python3 collectBestRef_AND_calculateAVG.py ${bestreffile}  ${groupnumber} ${locationofrefs} ${outdir}


dummyout=${outdir}_dummy

./run_adddumy_compartment_removeend.sh ${outdir} ${dummyout}


meanfolder=${dummyout}_mean
minfolder=${dummyout}_min
maxfolder=${dummyout}_max

mkdir ${meanfolder}
mkdir ${minfolder}
mkdir ${maxfolder}

cp ${dummyout}/*mean ${meanfolder}/

cp ${dummyout}/*min ${minfolder}/

cp ${dummyout}/*max ${maxfolder}/


python3 mergealldfinafolderrbindlike.py ${meanfolder} ${meanfolder}_SM.txt  mean

python3 mergealldfinafolderrbindlike.py ${minfolder}  ${minfolder}_SM.txt  min

python3 mergealldfinafolderrbindlike.py ${maxfolder}  ${maxfolder}_SM.txt  max




end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"


