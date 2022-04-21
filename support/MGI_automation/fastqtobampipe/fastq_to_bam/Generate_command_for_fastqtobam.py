#!/usr/bin/env python
# coding: utf-8

# In[1]:


import glob
import os
import sys

fastqfolder= sys.argv[1]  #'/Users/irffanalahi/Research/Research_code/support/MGI_automation/toydata/fastqfolder'


outfolder=sys.argv[2]   #'/Users/irffanalahi/Research/Research_code/support/MGI_automation/toydata/fastqfolder_convertingtobam'

outcommandfile=sys.argv[3]  #outfolder+"/"+os.path.basename(outfolder)+"_bamconversion.sh"

outfolder_bams=outfolder+"/"+os.path.basename(outfolder)+"_allbams"
outfolder_logs=outfolder+"/"+os.path.basename(outfolder)+"_bamconversiion_logs"


os.mkdir(outfolder)
os.mkdir(outfolder_bams)
os.mkdir(outfolder_logs)


# In[2]:


R1fastqs=glob.glob(fastqfolder+'/*_R1.fastq.gz')
R2fastqs=glob.glob(fastqfolder+'/*_R2.fastq.gz')


# In[3]:


bsub_commandlist=[]

for r1fastq in R1fastqs:
    r1fastq_base=os.path.basename(r1fastq).replace('_R1.fastq.gz','')
    
    
    r2fastq_path=fastqfolder+'/'+r1fastq_base+'_R2.fastq.gz'
    
    if r2fastq_path not in R2fastqs:
        print("R1,R2 mismatch. Exiting")
        sys.exit(1)
    
    outforthisbam=outfolder_bams+"/"+r1fastq_base
    
    os.mkdir(outforthisbam)
    
    bsub_command="bsub -M 48000000 -R 'select[mem>48000] rusage[mem=48000]' -oo "+outfolder_logs+"/"+r1fastq_base+".log" + "  -q general -a 'docker(bioslimcontainers/picard:2.18.29)' picard FastqToSam F1="+r1fastq+" F2="+r2fastq_path+     "  O="+outforthisbam+"/"+r1fastq_base+".bam"+" SM="+r1fastq_base+"\n\n"
    
    bsub_commandlist.append(bsub_command)
   


# In[4]:


with open(outcommandfile, 'w') as f:
    for item in bsub_commandlist:
        f.write("%s" % item)

