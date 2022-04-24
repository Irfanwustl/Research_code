start=$SECONDS



find *fastq.gz | parallel -j 20 md5sum > Our_md5.txt


end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"
