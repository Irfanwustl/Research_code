import time
import os
import sys


input_folder=sys.argv[1]


out_file=input_folder+"_samNEWmerged.txt"



total_read=""
mapped_read=""

with open(out_file,'w') as of:
	of.write("sample\ttotal\tsecondary\tsupplementary\tduplicates\tmapped\tmapped_percent\tpaired_in_sequencing\tread1\tread2\tproperly_paired\tproperly_paired_percentage\twith_itself_and_mate_mapped\tsingletons\twith_mate_mapped_to_a_different_chr\twith_mate_mapped_to_a_different_chr_mapQ>=5\n")
	for file in os.listdir(input_folder):
		with open(input_folder+"/"+file) as fin:
			i=0
			while i<16:
				line=fin.readline()
				

				strlist=line.split()
				
				if i==0:
					total_read=strlist[0]
				elif i==2:
					secondary=strlist[0]
				elif i==3:
					supplementary=strlist[0]
				elif i==4:
					duplicates=strlist[0]	
				elif i==6:
					mapped_read=strlist[0]
				elif i==8:
					paired_in_sequencing=strlist[0]
				elif i==9:
					read1=strlist[0]
				elif i==10:
					read2=strlist[0]
				elif i==11:
					properly_paired=strlist[0]
				elif i==12:
					with_itself_and_mate_mapped=strlist[0]
				elif i==13:
					singletons=strlist[0]
				elif i==14:
					with_mate_mapped_to_a_different_chr=strlist[0]
				elif i==15:
					with_mate_mapped_to_a_different_chr_mapQ_ge5=strlist[0]
				i=i+1

			mapped_per=float(mapped_read)/float(total_read)*100
			properly_paired_percentage=float(properly_paired)*1.0/(float(read1)+float(read2))*100
			strtowrite=file+"\t"+total_read+"\t"+secondary+"\t"+supplementary+"\t"+duplicates+"\t"+mapped_read+"\t"+str(mapped_per)+"\t"+paired_in_sequencing+"\t"+read1+"\t"+read2+"\t"+properly_paired+"\t"+str(properly_paired_percentage)+"\t"+with_itself_and_mate_mapped+"\t"+singletons+"\t"+with_mate_mapped_to_a_different_chr+"\t"+with_mate_mapped_to_a_different_chr_mapQ_ge5+"\n"
			of.write(strtowrite)
					

		