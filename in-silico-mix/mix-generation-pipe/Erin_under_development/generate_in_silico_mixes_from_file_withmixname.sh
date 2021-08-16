########################################################################
########################################################################
# Version 4, produced by Erin Brown 19 Apr 2021
# Status: Ready
########################################################################
# This script takes as input the following:
#      - data path, one level above actual data folders (optional)
#      - input file, tab delimited text file with the first
#        row containing directory names specific to each cell
#        type, with each directory containing 1 or more replicates, 
#        all BAM files; subsequent rows should contain the
#        desired proportion of cell type within output mixture
#      - output directory (optional)
#      - number of reads desired in output mixture (optional)
#      - number of threads to use (optional)
# and outputs a BAM file within the provided output directory
# containing the desired proportion of cell types.
#
# Notes: All paired reads are sampled together or not at all.
########################################################################

# Print usage statement if called without inputs
[ $# -eq 0 ] && { echo "Usage: $0 -i INPUTFILE -a DATAPATH -o DIROUT 
-r NUMREADS -t THREADS -s DSDIR -m MERGEDIR";
echo 'Details:
     -i: input file name, file should be tab delimited text file with
         the first row containing directory names specific to each cell
         type, with each directory containing 1 or more replicates, all
         BAM files; subsequent rows should contain the desired proportion
         of cell type within output mixture (REQUIRED)
     -a: data path, one level above actual data folders (OPTIONAL, default 
         is working directory)
     -o: name of output directory (OPTIONAL, default is 
         mixture_output within working directory)
     -r: number of reads to include in output mixture (OPTIONAL,
         default is 1 billion)
     -t: number of threads to use for samtools commands (OPTIONAL,
         default is 20)
     -s: directory name for downsampled files (OPTIONAL, default is 
         downsamples within working directory)
     -m: directory name for merged replicates (OPTIONAL, default is
         merged_replicates within working directory)
     -p: file prefix for mixture outputs (REQUIRED)''';

exit 1; }

# Load inputs


nreads=1000000000
threads=20
dpath=$(pwd)
wdpath=$(pwd)
dirout=$wdpath/mixture_output
dsdir=$wdpath/downsamples
mergedir=$wdpath/merged_replicates

while getopts i:a:o:r:t:s:m:p: option
do
case "${option}"
in
i ) input_file=${OPTARG};;
n ) ntypes=${OPTARG};;
a ) dpath=${OPTARG};;
o ) dirout=${OPTARG};;
r ) nreads=${OPTARG};;
t ) threads=${OPTARG};;
s ) dsdir=${OPTARG};;
m ) mergedir=${OPTARG};;
p ) outprefix=${OPTARG};;
esac
done



# Define a timestamp function
timestamp() {
  date +"%T" # current time
}

echo "Starting Timestamp"
timestamp

mkdir -p $dirout
mkdir -p $dsdir

nmixes=$(wc -l < $input_file)
nmixes=$(($nmixes-1))

declare -a inputarray
readarray inputarray < $input_file

read -d "\t" -a indirs <<< "${inputarray[0]}"
ntypes=${#indirs[@]}


for (( j=1; j<=$nmixes; j++ ))
#for (( j=1; j<=2; j++ ))
do
    mlist=()
    pcts=()
    read -r -a pcts <<< "${inputarray[j]}"
    
    IFS='+'
    pct_tot=$(echo "scale=1;${pcts[*]}"|bc)
    unset IFS

    echo $pct_tot
    #if (( $(echo "$pct_tot != 100" | bc -l) ))
    if (( $(echo "$pct_tot <= 99.99" | bc -l) ))
    then
	echo "ERROR: Proportions do not sum to 100"
	exit 1;
    fi
    if (( $(echo "$pct_tot >= 100.01" | bc -l) ))
    then
	echo "ERROR: Proportions do not sum to 100"
	exit 1;
    fi



    # Echo main inputs
    echo "Generating in silico mixture including $ntypes types with the following distribution:"
    for (( i=0; i<$ntypes; i++ ))
    do
	echo "     ${pcts[$i]}% ${indirs[$i]}"
    done

    # Merge replicates, count reads, then downsample
    ext='bam'
    rcount=()

    for (( i=0; i<$ntypes; i++ ))
    do
	echo "Now working on cell type ${indirs[i]}..."

	if [ "${pcts[i]}" != "0" ]
	then
            # Check if merged file already exists
	    clist=($( find $dpath/${indirs[$i]} -type f -name "*${ext}" ))

	    output_merged=$mergedir/${indirs[$i]}
	
	    mkdir -p $output_merged

	    output_merged=$output_merged/all_replicates.bam

	    if [ -f "$output_merged" ]; then
		echo "File $output_merged already exists and will not be overwritten"
	    else
 	        # Check if there is only one replicate
		if [ ${#clist[@]} -gt 1 ]; then
		    echo "Now merging ${#clist[@]} replicates in ${indirs[i]}..."
		    SECONDS=0
		    samtools merge -@ $threads $output_merged ${clist[@]}
		    echo "Merged BAM file saved to $output_merged"
		    duration=$SECONDS
		    echo "Merging ${indirs[i]} replicates took $(($duration / 60)) minutes and $(($duration % 60)) seconds"
		else
		    echo "Only one replicate: copying to $output_merged"
		    cp ${clist[0]} $output_merged
		fi
		
                ################# Rename Reads in Merged File ########
		prefix=${indirs[$i]} 

		rn_file=$output_merged.read_names.txt
		samtools view $output_merged | cut -f 1 > $rn_file
		cut -c -3 $rn_file > $rn_file.3.txt
		sort $rn_file.3.txt | uniq > $rn_file.uniq.txt
		declare -a rn_chars
		readarray rn_chars < $rn_file.uniq.txt
		num_pref=${#rn_chars[@]}
		samtools view -h $output_merged > $output_merged.SAM.sam
		for (( k=0; k<$num_pref; k++ ))
		do		    
		    pf=`echo ${rn_chars[k]} | xargs`
		    pf_add=`echo $prefix | xargs`
		    sed -e "s/$pf/$pf_add.$pf/" $output_merged.SAM.sam > $output_merged.2.SAM.sam
		    mv $output_merged.2.SAM.sam $output_merged.SAM.sam
		done
		samtools view -S -b $output_merged.SAM.sam > $output_merged.prefix.bam
		mv $output_merged.prefix.bam $output_merged

		rm $output_merged.SAM.sam
		rm $rn_file
		rm $rn_file.3.txt
		rm $rn_file.uniq.txt
	       	################# Rename Reads in Merged File ########


	    fi



	    echo "Downsampling merged file for ${indirs[i]}..."

   
            # CHECK HERE IF FILE ALREADY EXISTS

            # -b means output bam, -s means subsample
	    mkdir -p $dsdir
	    output_downsampled=$dsdir/${indirs[$i]}_downsampled_PCT_${pcts[i]}_NR_$nreads.bam
	    mlist+=($output_downsampled)
 	    if [ -f "$output_downsampled" ]; then
		echo "File $output_downsampled already exists and will not be overwritten"
		rcount+=($(samtools view -c -F 4 $output_merged)) 
	    else
		SECONDS=0
		rcount+=($(samtools view -c -F 4 $output_merged)) 
		#echo ${rcount[@]}
   	        # Calculate sampling proportion
		#echo ${pcts[i]}
		dspi=(`echo "1000000*${pcts[i]}*$nreads/${rcount[i]}" | bc -l`)
		#echo $dspi
                # We have to convert to integer for samtools input (do so by rounding)
		dspi=(`echo $dspi | awk '{print int($1+0.5)}'`)
		#echo $dspi
		dspi=(`echo $dspi | awk '{printf "%08d\n", $0;}'`)
		#echo $dspi
		if [ $dspi -gt 100000000 ]
		then
		    echo "ERROR: Not enough mapped reads in merged file for ${indirs[$i]}"
		    exit 1;
		fi
                # Count only mapped reads using -F 4 option
		#echo "samtools view -@ $threads -F 4 -b -s 0.${dspi} $output_merged > $output_downsampled"
		samtools view -@ $threads -F 4 -b -s 0.${dspi} $output_merged > $output_downsampled
		echo "Downsampled BAM file saved to $output_downsampled"
		duration=$SECONDS
		echo "Downsampling for merged ${indirs[i]} file took $(($duration / 60)) minutes and $(($duration % 60)) seconds"
	    fi
	else
	    echo "No ${indirs[i]} in mixture, skipping cell type ${indirs[i]}"
	    rcount+=(100) # this is just a filler to maintain array structure

	fi

    done

    # Now merge downsampled files into final output!
    echo "Producing final output mixture..."
    fnout=$outprefix\_NR_$nreads\_insilmix$j.bam
    echo $fnout
    output_final=$dirout/$fnout
    if [ -f "$output_final" ]; then
	echo "File $output_final already exists and will not be overwritten"
    else
	SECONDS=0
	samtools merge -@ $threads $output_final ${mlist[@]}
	echo "Final BAM mixture file saved to $output_final"    
	duration=$SECONDS
	echo "The final merge took $(($duration / 60)) minutes and $(($duration % 60)) seconds"
    fi
done


echo "Ending Timestamp"
timestamp


