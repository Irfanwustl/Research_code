
###### DEPENDS ON THE COMMANDFILE NAME OF PYTHON CODE####



bamfolder=$1  ####provide full path

commandfile=${bamfolder}_ReadNumber/command.sh  # DEPENDS ON THE COMMANDFILE NAME OF PYTHON CODE####

python3 Generate_command_for_read_numbernumber.py ${bamfolder} 


chmod +x ${commandfile}




${commandfile}


