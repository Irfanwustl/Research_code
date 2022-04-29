

modelinfo=$1

destinationfolder=$2





bsub -Is -q general-interactive -a 'docker(irfanwustl/pythonwithpandas)'  python3 cramtobam_and_copy.py ${modelinfo} ${destinationfolder}




chmod +x ${destinationfolder}_commands/cramtobam_commands.sh        #####hardcoded name from the python file


${destinationfolder}_commands/cramtobam_commands.sh




chmod +x ${destinationfolder}_commands/copy_commands.sh         #####hardcoded name from the python file


${destinationfolder}_commands/copy_commands.sh 





