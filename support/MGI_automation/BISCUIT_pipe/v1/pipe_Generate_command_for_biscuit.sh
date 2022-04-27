start=$SECONDS

bamfolder=$1  ####provide full path

biscuit_commandfile=${bamfolder}_BISCUIT.sh

python3 Generate_command_for_biscuit.py ${bamfolder} ${biscuit_commandfile}


chmod +x ${biscuit_commandfile}




${biscuit_commandfile}


end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"


