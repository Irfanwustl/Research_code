

medgenomesite=$1 #'https://portal-us.medgenome.com/P2003825_04222022/FASTQ' ###without backslash
username=$2 #'P2003825_04222022'
password=$3 #'t^8s368cK!@%'
infile=$4 #'md5sum.txt'

wheretodownload=$5





bsub -Is -q general-interactive -a 'docker(irfanwustl/pythonwithpandas)'  python3 downloading_from_medgenome.py ${medgenomesite}  ${username} ${password} ${infile} ${wheretodownload}




chmod +x ${wheretodownload}/medgenome_download.sh        #####hardcoded name from the python file


${wheretodownload}/medgenome_download.sh








