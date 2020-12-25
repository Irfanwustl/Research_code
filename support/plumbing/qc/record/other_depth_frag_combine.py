import time
import os
import sys


input_folder=sys.argv[1]


out_file=sys.argv[2]






with open(out_file,'w') as of:
	of.write("sample\t01st_ptle\t05th_ptle\t25th_ptle\t50th_ptle\t75th_ptle\t95th_ptle\t99th_ptle\t\n")
	for file in os.listdir(input_folder):
		with open(input_folder+"/"+file) as fin:
			i=0
			depth=""
			while True:
				line=fin.readline()
				if line:
				
					if line.strip():
						
						strlist=line.split()
						val=strlist[1]
						
						if i in range(6,13):
							depth=depth+"\t"+val
						
						
					i=i+1
				else:
					break

			
			strtowrite=file+depth+"\n"
			of.write(strtowrite)
					

		