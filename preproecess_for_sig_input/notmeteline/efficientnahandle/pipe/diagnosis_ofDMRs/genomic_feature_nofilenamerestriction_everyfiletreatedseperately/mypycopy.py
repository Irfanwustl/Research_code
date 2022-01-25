import pandas as pd 
import sys
import os.path
import shutil

import re

import glob
import os




def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))


inputfile=sys.argv[1]

inputfiledf=pd.read_csv(inputfile,sep="\t",header=None,low_memory = False)

outfoldercontainingfolder=sys.argv[2] 


genomicfeaturefolder=sys.argv[3]


inputfilebasename=os.path.basename(inputfile)






genomicfeaturefiles=listdir_nohidden(genomicfeaturefolder)

#######

#print(inputfilebasename)
#print('...........................')

flag=0
for genomefile in genomicfeaturefiles:

    genomefilebase=os.path.basename(genomefile)
    #print(genomefilebase)
    
    if inputfilebasename.endswith(genomefilebase):
        flag=1
        found=inputfilebasename[:len(inputfilebasename)-len(genomefilebase)]
        break


if  flag==0:
    print("name error. exit")
    sys.exit(1)

celltype=found

outfolder=outfoldercontainingfolder+"/"+celltype
if not os.path.exists(outfolder):
    os.makedirs(outfolder)

outfile=outfolder+"/"+inputfilebasename

shutil.copyfile(inputfile, outfile)
