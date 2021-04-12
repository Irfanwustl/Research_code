import pandas as pd
import sys
import concurrent.futures
import math
import os.path
import re
import multiprocessing


class AllCompartmentMean:
	def __init__(self, rowmeancalculstedelsewhere, metoutfile, phenofile, outname, **kwargs):


		self.rowmeancalculstedelsewhere=rowmeancalculstedelsewhere
		self.metoutfile = pd.read_csv(metoutfile,sep="\t",header=None)
		self.pheno = phenofile
		self.outname = outname

		self.metoutfilename = os.path.basename(metoutfile)


	def coreAlgo(self):


		rowmeandf=self.rowmeancalculstedelsewhere





		outdf=self.setupparallalrun(rowmeandf)

		outdf,celltype=self.headerfix(outdf)

		outdf=self.comparmentwisdiff(outdf,celltype)

		#filsuffix="_".join(str(x) for x in self.pheno.index)




		out=self.outname


		outdf.to_csv(out,sep="\t",index=False)


	def headerfix(self,newdf):

		m = re.search('g1_(.+?)_\d+_g2', self.metoutfilename)
		if m:
			found = m.group(1)

		else:
			print("cell type not found", self.metoutfilename)
			print("exiting")

			sys.exit(1)

		celltype = found

		outdf = newdf.rename(columns={0: "chrom", 1: "start", 2: "end", 3: "q", 4: "diff", 5: "#cpg", 6: "p(MWU)",7: "p(2dks)", 8: celltype, 9: "others"})

		return outdf,found

	def comparmentwisdiff(self,newdf,celltype):
		cells=(self.pheno.index).tolist()

		compartmendeltalist=[]
		for cell in cells:
			if cell!=celltype:
				tempdelta=celltype+"-"+cell
				newdf[tempdelta]=newdf.iloc[:,8]-newdf[cell]

				compartmendeltalist.append(tempdelta)




		newdf['maxCompartmentwisedelta']=newdf[compartmendeltalist].max(axis=1)
		newdf['minCompartmentwiseDelta']=newdf[compartmendeltalist].min(axis=1)







		return newdf










	def setupparallalrun(self,rowmeandf):

		chunk =multiprocessing.cpu_count()-1
		print("chunk===")
		print(chunk)




		if chunk==0:
			chunk=1

		totalrow = self.metoutfile.shape[0]


		trdGroupSize=math.floor(totalrow/chunk)

		if trdGroupSize==0:
			trdGroupSize=totalrow





		trdend=0



		multiresult = []

		with concurrent.futures.ProcessPoolExecutor() as executor:

			processlist = []
			for trdgrtemp in range(chunk):
				trdstart = trdend
				trdend = trdstart + trdGroupSize  ###end excluded in python subset
				if trdgrtemp == chunk - 1:
					trdend = totalrow

				currentdf = self.metoutfile[trdstart:trdend]

				processlist.append(executor.submit(finalout, currentdf,self.pheno, rowmeandf))

			for process in concurrent.futures.as_completed(processlist):
				multiresult.append(process.result())

		multiresultdf = pd.concat(multiresult)

		return multiresultdf


def finalout(metoutfile,pheno,rowmeandf):

	rowlist=[]
	for index, row in metoutfile.iterrows():     ###tqdm
		mchrom=row[0]
		mstart=row[1]
		mend=row[2]

		tempdf=rowmeandf[(rowmeandf['chrom']==mchrom) & (rowmeandf['pos']>=mstart) & (rowmeandf['pos']< mend)]


		tempsize=pd.Series({"mycpgcount":tempdf.shape[0]})

		tempmean=tempdf[pheno.index].mean()



		temprow=row.append(tempmean)
		temprow=temprow.append(tempsize)


		rowlist.append(temprow)

	outdf = pd.DataFrame(rowlist)



	return outdf





def main():
	rowmeandf=sys.argv[1]
	metoutfile = sys.argv[2]
	phenfile = sys.argv[3]

	outname = sys.argv[4]

	acm = AllCompartmentMean(rowmeandf,metoutfile,phenfile,outname)

if __name__ == '__main__':
	main()