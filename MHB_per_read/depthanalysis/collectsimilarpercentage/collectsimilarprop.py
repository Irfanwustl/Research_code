import sys
import glob
import re
import os
import shutil


diffpropfolder=sys.argv[1]



innerdirlist=glob.glob(diffpropfolder+"/*.bam")


for innerdir in innerdirlist:
    innerfilelist=glob.glob(innerdir+"/*.bam")

    for innerfile in innerfilelist:

        m = re.search('percent_(.+?).bam', innerfile)
        found=-1
        if m:
            found = m.group(1)

        else:
            print("found=", found)
            print("exiting")

            sys.exit(1)

        destinedfolder=diffpropfolder+"_"+found
        if not os.path.exists(destinedfolder):
            os.makedirs(destinedfolder)

        shutil.copyfile(innerfile, destinedfolder+"/"+os.path.basename(innerfile))