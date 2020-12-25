import os
import sys



####assumption: output folder should not exist, it can roll successfully if the gap is multiple of 2


input_folder=sys.argv[1]  #cd4 or cd8


output_folder=input_folder+"_rolled"

os.makedirs(output_folder)

all_files_temp = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

all_files=[]

for tempfile in all_files_temp:
	if ".bedgraph" in tempfile:
		all_files.append(tempfile)



print all_files


for file in all_files:
	output_file_name=file+"_rolled.bedgraph"
	output_file_name=output_folder+"/"+output_file_name


	file=input_folder+"/"+file
	
	with open(output_file_name,'w') as output_file:
		with open(file) as currentfile:
			while True:
				line=currentfile.readline()
				if line:
					if line.strip():
						str_list=line.split()

						total_line=(int(str_list[2])-int(str_list[1]))/2
						i=0
						start=int(str_list[1])
						while i<total_line:
							str_of_pad=str_list[0]+"\t"+str(start)+"\t"+str(start+2)+"\t"+str_list[3]+"\n"
							output_file.write(str_of_pad)
							start=start+2
							i=i+1
						
				else:
					break




