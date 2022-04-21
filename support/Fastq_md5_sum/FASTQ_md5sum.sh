start=$SECONDS




md5sum *fastq.gz > Our_md5.txt


end=$SECONDS
duration=$(( end - start ))
echo "stuff took $duration seconds to complete"
