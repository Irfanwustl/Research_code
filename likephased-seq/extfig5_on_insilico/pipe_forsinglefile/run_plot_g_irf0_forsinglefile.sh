infolder=$1


dirList=($( ls ${infolder}  ))


i=0
while (( i < ${#dirList[@]} ))
do

	echo now=========${dirList[i]} 
	

	python3 plot_g_irf0_forsinglefile.py ${infolder}/${dirList[i]}


 	(( i++ ))
done