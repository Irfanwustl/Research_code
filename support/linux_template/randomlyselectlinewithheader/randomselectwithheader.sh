filename=$1
lines=$2

{ IFS= read -r head; echo "$head"; shuf | head -n ${lines}; } < ${filename} > ${filename}_rand${lines}

