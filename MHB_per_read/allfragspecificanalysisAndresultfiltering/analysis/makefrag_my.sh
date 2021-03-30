#! /bin/bash


dir=$1 


echo "now R ...."

frag_img=${dir}_img

mkdir ${frag_img}

Rscript frag_pp.R ${dir} ${frag_img}