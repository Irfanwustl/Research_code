import pandas as pd 
import sys
import os.path
import shutil
import datetime

import re


inputfile=sys.argv[1]



outfoldercontainingfolder=sys.argv[2] 


inputfilebasename=os.path.basename(inputfile)








outfolder=outfoldercontainingfolder+"/"+inputfilebasename
if not os.path.exists(outfolder):
    os.makedirs(outfolder)




now = str(datetime.datetime.now())[:19]
now = now.replace(":","_")

outfile=outfolder+"/"+inputfilebasename+str(now)+".txt"

shutil.copyfile(inputfile, outfile)