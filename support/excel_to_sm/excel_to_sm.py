import time
import os
import sys



input_file=sys.argv[1]  ###.txt file with header
merge1=int(sys.argv[2])
merge2=int(sys.argv[3])
merged_col_name=sys.argv[4]
asitiscol1=int(sys.argv[5])
asitiscol2=int(sys.argv[6])
out_file_name=sys.argv[7]


with open (input_file) as f:

	with open (out_file_name,'w') as outputfile:
		fl=f.readline()### header
		str_head=fl.split()
		new_head=merged_col_name+"\t"+str_head[asitiscol1]+"\t"+str_head[asitiscol2]+"\n"
		outputfile.write(new_head)
		while True:
			line=f.readline()
			if line:
				if line.strip():
					str_list=line.split()	
					m1=str_list[merge1]
					m2=str_list[merge2]	
					ais1=str_list[asitiscol1]
					ais2=str_list[asitiscol2]
					m12=m1+":"+m2
					strtowrite=m12+"\t"+ais1+"\t"+ais2+"\n"

					outputfile.write(strtowrite)
			else:
				break




