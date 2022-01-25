import pandas as pd 
import sys
import os.path
import shutil

import re


inputfile=sys.argv[1]

inputfiledf=pd.read_csv(inputfile,sep="\t",header=None,low_memory = False)

outfoldercontainingfolder=sys.argv[2] 


inputfilebasename=os.path.basename(inputfile)

m = re.search('g1_(.+?)_\d+_g2', inputfilebasename)
if m:
    found = m.group(1)

else:
	found=inputfilebasename





celltype=found

outfolder=outfoldercontainingfolder+"/"+celltype
if not os.path.exists(outfolder):
    os.makedirs(outfolder)

outfile=outfolder+"/"+inputfilebasename

shutil.copyfile(inputfile, outfile)