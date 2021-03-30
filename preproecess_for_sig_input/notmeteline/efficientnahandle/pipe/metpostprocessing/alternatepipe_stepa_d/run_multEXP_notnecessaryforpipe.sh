infolder=$1

qcut=0.00001



./stepa_d.sh ${infolder} ${qcut} 0.3

./stepa_d.sh ${infolder} ${qcut} 0.4

./stepa_d.sh ${infolder} ${qcut} 0.5

./stepa_d.sh ${infolder} ${qcut} 0.6


./stepa_d.sh ${infolder} ${qcut} 0.2

./stepa_d.sh ${infolder} ${qcut} 0.7

./stepa_d.sh ${infolder} ${qcut} 0.8
