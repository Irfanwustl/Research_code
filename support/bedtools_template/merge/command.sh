bedtools merge -d -1 -i a.bed > a_merged_onlyoverlapping.bed ### only overlapping, end same will be kept as it is

bedtools merge  -i a.bed > a_merged_endsameoverlapping.bed ### also end same will be considered