import ReadAssign

import pandas as pd

sm="data/smMHB_cd4_cd8_g50_hypo_assigned_maual_list.txt_mhb"#"data/smMHB_cd4_cd8_g50_hypo_assigned_maual_list_testing.txt_mhb"#"data/corres_pos_cgr1-1222701_nodup_sorted_cpg_testSM.txt"
sm=pd.read_csv(sm, sep="\t")

bamfile="TWCY-1382-1382-BULK-PBMC_sorted"#"corres_pos_cgr1-1222701_nodup_sorted"#"TWCY-1382-1382-BULK-PBMC_sorted.bam"#"corres_pos_cgr1-1222701_nodup_sorted"

bamfolder="/Users/irffanalahi/Research/weekly/for_9_24_20/Analysis/bamfiles/bamfiles_onlyregionIN_smMHB_cd4_cd8_g50_hypo_mhb_sorted_sorted"#"/Users/irffanalahi/Research/Research_update/Sequencing/understandBamFiles/try1/bamfiles_onlyregionIN_bluSMsingle450_MHBWGBS_pos_c2brename_corresSAM/bam_sorted"#"/Users/irffanalahi/Research/weekly/for_9_24_20/Analysis/bamfiles/bamfiles_onlyregionIN_smMHB_cd4_cd8_g50_hypo_mhb_sorted_sorted_rename"
    #"/Users/irffanalahi/Research/Research_update/Sequencing/understandBamFiles/try1/bamfiles_onlyregionIN_bluSMsingle450_MHBWGBS_pos_c2brename_corresSAM/bam_sorted"

bamfilepath=bamfolder+"/"+bamfile


outfolder="data"
outname=bamfile+"_rd2out"
outpath=outfolder+"/"+outname


#### for our data howsm should be changed###
b=ReadAssign.ReadAssign(bamfilepath, 40, 20,sm,outpath,howsm='mhb')#,mode='single_read')