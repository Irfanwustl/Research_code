#! /bin/bash

#parm1=input_folder
#parm2=output_file_name

set -e  # exit if any exception


function create_string_form_array () {

local file_list=("$@")
local i=0
while (( i < ${#file_list[@]} ))
do
	x=".bedgraph"
	this_file=$(basename ${file_list[i]} $x)
	if (( i ==0 ))
	then
		files_concatenated=$this_file
	else
		files_concatenated="$files_concatenated   ${this_file}"
	fi
	
	(( i++ ))
done

echo $files_concatenated
}

function create_string_form_array_real () {

local file_list=("$@")
local i=0
while (( i < ${#file_list[@]} ))
do
	if (( i ==0 ))
	then
		files_concatenated="${file_list[i]}"
	else
		files_concatenated="$files_concatenated  ${file_list[i]}"
	fi
	
	(( i++ ))
done

echo $files_concatenated
}

g1_folder=$1


celltype1_file_list=($( ls $g1_folder/*.bedgraph ))




celltype1_files_concatenated=$(create_string_form_array "${celltype1_file_list[@]}")

celltype1_files_concatenated_path=$(create_string_form_array_real "${celltype1_file_list[@]}")


out=$2     #${g1_folder}_allMatrix


final_command="bedtools unionbedg -i ${celltype1_files_concatenated_path}  -filler NA > $out"

echo $final_command


bedtools unionbedg -i ${celltype1_files_concatenated_path} -filler NA > $out








