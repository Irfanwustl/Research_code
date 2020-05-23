###param1 =befor_polish_freq

###param2=after_polish_freq

###parm3=merged_freq











import pandas as pd

import sys





def mergedFreq(beforeDF,afterDF,mergedfile):
	if list(beforeDF.columns)!=list(afterDF.columns):
		print(beforeDF.columns)
		print(afterDF.columns)
		print ("column name mismatch")
		sys.exit(1)



	mergedDF=pd.DataFrame(columns = beforeDF.columns)

	beforeDF_rownum=beforeDF.shape[0]
	afterDF_rownum=afterDF.shape[0]

	if beforeDF_rownum<afterDF_rownum:
		print (beforeDF_rownum)
		print(afterDF_rownum)
		print ("beforedf has smaller row number")
		sys.exit(1)


	bi=0
	ai=0
	while bi< beforeDF_rownum:
		if (beforeDF['CHR'].iloc[bi]==afterDF['CHR'].iloc[ai]) and (beforeDF['POS'].iloc[bi]==afterDF['POS'].iloc[ai]):
			mergedDF=mergedDF.append(afterDF.iloc[ai])
			ai=ai+1

		else:
			mergedDF=mergedDF.append(beforeDF.iloc[bi])


		bi=bi+1



	mergedDF.to_csv(mergedfile,sep="\t",index=False)















befor_polish_freq=sys.argv[1]

after_polish_freq=sys.argv[2]


merged_freq=sys.argv[3]

befor_polish_freq_df = pd.read_csv(befor_polish_freq, sep="\t")

after_polish_freq_df = pd.read_csv(after_polish_freq, sep="\t")

mergedFreq(befor_polish_freq_df,after_polish_freq_df,merged_freq)

