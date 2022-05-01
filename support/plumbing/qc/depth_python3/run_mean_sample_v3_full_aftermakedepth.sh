
in_folder=$1     ######"all_bams_pp_depth"
out_folder="${in_folder}_mean_samplev3"

mkdir ${out_folder}

#### mean sample
python mean_sample_v3.py  ${in_folder}   Y 10000  ${out_folder}      ###################################### need to be changed in every batch ######

echo "now R.."



rout="${out_folder}_img"
mkdir ${rout}

Rscript  double_shaded_fill.R ${out_folder} ${rout}