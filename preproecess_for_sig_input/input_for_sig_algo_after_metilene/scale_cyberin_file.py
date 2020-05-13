import time
import os
import sys



def prep_to_write(str_list):
	unchanged=str_list[0]
	remain=unchanged
	wc=1
	while wc < len(str_list):
		if str_list[wc]!="NA":
			remain=remain+"\t"+str(float(str_list[wc])*100)
		else:
			remain=remain+"\t"+str_list[wc]
		wc=wc+1
	remain=remain+"\n"
	return remain

input_file_name=sys.argv[1]


#out_director=sys.argv[2]

out_file_name=sys.argv[2]




with open (out_file_name,'w') as outputfile:
	with open (input_file_name) as f:
		line=f.readline()  ####header
		outputfile.write(line)
		while True:
			line=f.readline()
			if line:
				if line.strip():
					str_list=line.split()
					strtowrite=prep_to_write(str_list)
					outputfile.write(strtowrite)
			else:
				break