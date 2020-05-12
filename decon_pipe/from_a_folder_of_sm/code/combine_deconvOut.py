import time
import os
import sys





def prep_to_write(str_list):
	remain=""
	wc=0
	while wc < len(str_list):
		if wc  >= 1:
			remain=remain+"\t"+str_list[wc]
	
		wc=wc+1
	remain=remain+"\n"
	return remain



input_folder=sys.argv[1]
out_file=sys.argv[2]

with open(out_file,'w') as of:
	count=0
	for sub_folder in os.listdir(input_folder):
		if os.path.isdir(input_folder+"/"+sub_folder):
			for file in os.listdir(input_folder+"/"+sub_folder):
				with open(input_folder+"/"+sub_folder+"/"+file) as fin:
					header=fin.readline()
					data=fin.readline()
					if (count==0):
						of.write(header)
					

					str_list=data.split()
					strtowrite=sub_folder+prep_to_write(str_list)
					of.write(strtowrite)
					count=count+1
				
