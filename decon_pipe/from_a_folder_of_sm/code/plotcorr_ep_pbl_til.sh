
all_merdged_gt=$1



Rscript pearson_plot_crc.R ${all_merdged_gt} tsize_SLD_path EPCAM red 

Rscript pearson_plot_crc.R ${all_merdged_gt} tsize_sld_mul_rnaepcam EPCAM red 


Rscript pearson_plot_crc.R ${all_merdged_gt} tsize_sld_mul_rnacd45 TIL green



Rscript spearman_plot_crc.R ${all_merdged_gt} tsize_SLD_path EPCAM red 

Rscript spearman_plot_crc.R ${all_merdged_gt} tsize_sld_mul_rnaepcam EPCAM red 

Rscript spearman_plot_crc.R ${all_merdged_gt} tsize_sld_mul_rnacd45 TIL green

