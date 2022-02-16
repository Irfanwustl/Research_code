import time
import os
import sys



input_file_name=sys.argv[1]  ### must be with header, the output will be headerless

out_file_name=input_file_name+"_onlyposition"



with open (input_file_name) as f:

	with open (out_file_name,'w') as outputfile:
		f.readline()
		while True:
			line=f.readline()
			if line:
				if line.strip():
					str_list=line.split()
					str_list=str_list[0].split(":")
					our_chr=str_list[0]
					our_end=int(str_list[1])+1
					our_start=our_end-2

					


					str_to_write=our_chr+"\t"+str(our_start)+"\t"+str(our_end)+"\n"
					outputfile.write(str_to_write)
			else:
				break
