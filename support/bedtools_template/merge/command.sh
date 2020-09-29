bedtools merge -d -1 -i a.bed > a_merged_onlyoverlapping.bed ### only overlapping, end same will be kept as it is

bedtools merge  -i a.bed > a_merged_endsameoverlapping.bed ### also end same will be considered


bedtools merge -d 600 -i b > b_600_merged.txt ##### merge with a long distance