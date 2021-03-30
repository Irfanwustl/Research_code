import pysam
import sys
from collections import defaultdict
import pandas as pd



def read_pair_generator(bam,region_string=None):
	"""
	Generate read pairs in a BAM file or within a region string.
	Reads are added to read_dict until a pair is found.
	"""
 


	read_dict = defaultdict(lambda: [None, None])
	
	for read in bam.fetch(region=region_string):
		

		if not read.is_proper_pair or read.is_secondary or read.is_supplementary:
			continue
		qname = read.query_name
		if qname not in content:
			continue
		if qname not in read_dict:
			if read.is_read1:
				read_dict[qname][0] = read
			else:
				read_dict[qname][1] = read
		else:
			if read.is_read1:
				yield read, read_dict[qname][1]
			else:
				yield read_dict[qname][0], read
			del read_dict[qname]


def coreAlgo(bam,out,outl):
	OpenBamFile = pysam.AlignmentFile(bam, 'rb')
	legthlist=[]
	namelist=[]

	for read1, read2 in read_pair_generator(OpenBamFile):
		currenttlength=1*(read1.template_length+read2.template_length)/2
		legthlist.append(currenttlength)
		namelist.append(read1.query_name)





	outdf=pd.DataFrame({'read_name':namelist,'frag_length':legthlist})
	outdf.to_csv(outl,sep="\t",index=False)

	outdf['frag_length'].to_csv(out,sep="\t",index=False,header=False)


	### sanity check ######
	contentlen=len(content)
	outdfrownum=outdf.shape[0]

	if contentlen > outdfrownum:
		print(bam)
		print ("contentlen greater. contentlen=",contentlen," outdfrownum=",outdfrownum)

	elif contentlen < outdfrownum:
		print(bam)
		print ("Thats the case....contentlen smaller. contentlen=",contentlen," outdfrownum=",outdfrownum)




		
		



inputbam=sys.argv[1]
readnamefile=sys.argv[2]
outbam=sys.argv[3]
outlog=sys.argv[4]

with open(readnamefile) as f:
	content = f.readlines()
	content = [x.strip() for x in content]

coreAlgo(inputbam,outbam,outlog)



