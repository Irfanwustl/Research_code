import time
import os
import sys

import numpy as np
np.set_printoptions(suppress=True)

import glob

input_folder=sys.argv[1]

file_prefix=sys.argv[2]

bin_size=int(sys.argv[3])
out_folder=sys.argv[4]

infile_reg=input_folder+"/"+file_prefix+"*"  #####################################

flist=glob.glob(infile_reg)




print infile_reg
print flist



quant_arr=[5,50,95]

for input_file in flist:
	input_file_name=os.path.basename(input_file)
	out_file_name=out_folder+"/"+input_file_name  #######median 50 percentile
	out_file_name_5=out_file_name+"_fifth"
	out_file_name_95=out_file_name+"_ninefive"
	tenkb_list=[]
	with open(out_file_name,'w') as outputfile:
		with open(out_file_name_5,'w') as outputfile_5:
			with open(out_file_name_95,'w') as outputfile_95:
		
				with open (input_file) as f:
					i=0
					sum=0
					
					while True:
						line=f.readline()
						if line:
							if line.strip():
								str_list=line.split()
								if len(str_list) != 1:
									print "errror"
								elem=float(str_list[0])
								tenkb_list.append(elem)
								
								i=i+1
								if i==bin_size:
									npa=np.array(tenkb_list)
									stat_np=np.percentile(npa,quant_arr)
									avg=np.mean(npa)
									tenkb_list=[]
									#np.savetxt(outputfile,stat_np)
									outputfile_5.write(str(stat_np[0])+"\n")
									outputfile.write(str(avg)+"\n")
									#outputfile.write(str(stat_np[1])+"\n")
									outputfile_95.write(str(stat_np[2])+"\n")


									i=0
									

						else:
							if i>0:
								npa=np.array(tenkb_list)
								stat_np=np.percentile(npa,quant_arr)
								avg=np.mean(npa)
								outputfile_5.write(str(stat_np[0])+"\n")
								outputfile.write(str(avg)+"\n")
								outputfile_95.write(str(stat_np[2])+"\n")
							break







