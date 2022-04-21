


#################################################
genome individual create --taxon=1653198737 --name=EM_4_cfDNA
genome sample create --source=EM_4_cfDNA --extraction-label=auto --name=EM_4_cfDNA-auto
genome library create --name=EM_4_cfDNA-auto-library --sample=EM_4_cfDNA-auto   --bisulfite-conversion=STANDARD 
genome instrument-data import trusted-data --analysis-project=17eb4eea6cb344f889c546a3a5f7c686 --import-source-name=Chaudhuri_WGBS  --library=EM_4_cfDNA-auto-library   --source-directory=/Users/irffanalahi/Research/Research_code/support/MGI_automation/toydata/bamfolder/EM_4_cfDNA  --import-format=bam --read-count=962652



#################################################
genome individual create --taxon=1653198737 --name=EM_3_cfDNA
genome sample create --source=EM_3_cfDNA --extraction-label=auto --name=EM_3_cfDNA-auto
genome library create --name=EM_3_cfDNA-auto-library --sample=EM_3_cfDNA-auto   --bisulfite-conversion=STANDARD 
genome instrument-data import trusted-data --analysis-project=17eb4eea6cb344f889c546a3a5f7c686 --import-source-name=Chaudhuri_WGBS  --library=EM_3_cfDNA-auto-library   --source-directory=/Users/irffanalahi/Research/Research_code/support/MGI_automation/toydata/bamfolder/EM_3_cfDNA  --import-format=bam --read-count=1087539



#################################################
genome individual create --taxon=1653198737 --name=EM_10_cfDNA
genome sample create --source=EM_10_cfDNA --extraction-label=auto --name=EM_10_cfDNA-auto
genome library create --name=EM_10_cfDNA-auto-library --sample=EM_10_cfDNA-auto   --bisulfite-conversion=STANDARD 
genome instrument-data import trusted-data --analysis-project=17eb4eea6cb344f889c546a3a5f7c686 --import-source-name=Chaudhuri_WGBS  --library=EM_10_cfDNA-auto-library   --source-directory=/Users/irffanalahi/Research/Research_code/support/MGI_automation/toydata/bamfolder/EM_10_cfDNA  --import-format=bam --read-count=1319173
