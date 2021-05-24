import time
import os
import sys


def prep_to_write(str_list):
	remain=""
	wc=0
	while wc < len(str_list):
		if wc  >= 3:
			remain=remain+"\t"+str_list[wc]
	
		wc=wc+1
	remain=remain+"\n"
	return remain

input_file_name=sys.argv[1]
with_header=int(sys.argv[2])  ###1=yes, 0=no

out_file_name=sys.argv[3]



with open (input_file_name) as f:

	with open (out_file_name,'w') as outputfile:
		if with_header==1:
			line=f.readline()
			str_list_h=line.split()
			header="position"+prep_to_write(str_list_h)
			outputfile.write(header)
		else:
			header="position"+"\t"+"value\n"
			outputfile.write(header)
		while True:
			line=f.readline()
			if line:
				if line.strip():
					str_list=line.split()
					our_chr=str_list[0]
					our_end=str_list[2]

					


					str_to_write=our_chr+":"+str(int(our_end)-1)+prep_to_write(str_list)
					outputfile.write(str_to_write)
			else:
				break
