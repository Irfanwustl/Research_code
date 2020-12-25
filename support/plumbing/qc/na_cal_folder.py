import time
import os
import sys


input_folder=sys.argv[1]
out_file=input_folder+"_na.txt"


with open(out_file,'w') as of:
	for file in os.listdir(input_folder):
		with open(input_folder+"/"+file) as fin:
			count=0
			while True:
				line=fin.readline()
				if line:
					if line.strip():
						count=count+1
				else:
					str_to_write=file+"\t"+str(count)+"\n"
					of.write(str_to_write)
					break
