import glob
import os
import sys
import subprocess


bamfolder=sys.argv[1]




def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))



outfolder=bamfolder+"_ReadNumber"

outfolder_Readnumber=outfolder+"/Readnumber"
outfolder_logs=outfolder+"/logs"

os.mkdir(outfolder)
os.mkdir(outfolder_Readnumber)
os.mkdir(outfolder_logs)


outfolder_commandfile=outfolder+"/command.sh"





allbamfolder=listdir_nohidden(bamfolder)
allbamfolder



commandlist=[]
for abam in allbamfolder:
    currentbam=glob.glob(abam+'/*.bam')
    if len(currentbam)!=1:
        print('multiple bams in bam folder. EXITING')
        sys.exit(1)
    currentbam=currentbam[0]

    str1='samtools view -c '+currentbam +' > '+ outfolder_Readnumber+'/'+os.path.basename(abam)+'\n'

    fullcommand="bsub -M 48000000 -R 'select[mem>48000] rusage[mem=48000]' -oo "+outfolder_logs+"/"+os.path.basename(abam)+".log" + "  -q general -a  'docker(irfanwustl/insilico_mix)' "+str1

    commandlist.append(fullcommand)

with open(outfolder_commandfile, 'w') as f:
    for item in commandlist:
        f.write("%s" % item)


