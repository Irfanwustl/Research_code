import pandas as pd 

import sys






def geneSpecificFile(gdf,allmatgdf,outpathfolder):
	genename=gdf.iloc[:, 3]


	

	for gene in genename:
		
		tempdf=allmatgdf[allmatgdf.iloc[:,-1]==gene]
		tempdf=tempdf.iloc[:,:-4]

		gene=gene.replace("/", "irfor")
		outfile=outpathfolder+"/"+gene+".txt"
		tempdf.to_csv(outfile,sep="\t",index=False)













geneFile=sys.argv[1]

geneFiledf=pd.read_csv(geneFile, header=None,sep="\t")

allmatgeneFile=sys.argv[2]

allmatgeneFiledf=pd.read_csv(allmatgeneFile,sep="\t",keep_default_na=False)



outfolder=sys.argv[3]


geneSpecificFile(geneFiledf,allmatgeneFiledf,outfolder)









