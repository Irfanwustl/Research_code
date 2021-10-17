#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import os
from collections import defaultdict


def featureSignificance(infile,celltype,SMrecordfile,outfilename):

	SMrecordDF=pd.read_csv(SMrecordfile,sep="\t")

	indf=pd.read_csv(infile,sep='\t')
	indf['acceptedCpG']=indf.acceptedCpG.apply(lambda x: x[1:-1].split(','))
	indf['notacceptedCpG']=indf.notacceptedCpG.apply(lambda x: x[1:-1].split(','))

	indf=indf[(indf['finalacceptedfor']==celltype) |  (indf['finalrejectedfor'].str.contains(celltype))] 


	accepteddf=(indf[indf['finalacceptedfor']==celltype]).copy()



	TPdf=accepteddf[accepteddf['ReadName'].str.contains(celltype)]
	FPdf=accepteddf[~accepteddf['ReadName'].str.contains(celltype)]


	rejecteddf=(indf[indf['finalrejectedfor'].str.contains(celltype)]).copy()

	

	TNdf=rejecteddf[~rejecteddf['ReadName'].str.contains(celltype)]
	FNdf=rejecteddf[rejecteddf['ReadName'].str.contains(celltype)]



	TPdf_cpg_freq=entryFullcount(TPdf,'acceptedCpG')
	FPdf_cpg_freq=entryFullcount(FPdf,'acceptedCpG')
	TNdf_cpg_freq=entryFullcount(TNdf,'notacceptedCpG')
	FNdf_cpg_freq=entryFullcount(FNdf,'notacceptedCpG')



	TPdf_cpg_freqdf=pd.DataFrame.from_dict(TPdf_cpg_freq,orient='index', columns=['#TP_fragment'])
	FPdf_cpg_freqdf=pd.DataFrame.from_dict(FPdf_cpg_freq,orient='index', columns=['#FP_fragment'])
	TNdf_cpg_freqdf=pd.DataFrame.from_dict(TNdf_cpg_freq,orient='index', columns=['#TN_fragment'])
	FNdf_cpg_freqdf=pd.DataFrame.from_dict(FNdf_cpg_freq,orient='index', columns=['#FN_fragment'])


	combineddf=pd.concat([TPdf_cpg_freqdf,FPdf_cpg_freqdf,TNdf_cpg_freqdf,FNdf_cpg_freqdf],axis=1)
	combineddf.fillna(0,inplace=True)

	combineddf['#Total_Fragment']=combineddf['#TP_fragment']+combineddf['#FP_fragment']+combineddf['#TN_fragment']+combineddf['#FN_fragment']


	combineddf['TPR']=combineddf['#TP_fragment']/(combineddf['#TP_fragment']+combineddf['#FN_fragment'])
	combineddf['FPR']=combineddf['#FP_fragment']/(combineddf['#FP_fragment']+combineddf['#TN_fragment'])
	combineddf['FDR']=combineddf['#FP_fragment']/(combineddf['#FP_fragment']+combineddf['#TP_fragment'])

	combineddf['fileName']=os.path.basename(infile)


	combineddf.reset_index(inplace=True)



	combineddf[['chrom','start']] = combineddf['index'].str.split(":",expand=True)

	combineddf.drop(['index'],inplace=True,axis=1)


	combineddf['start']=combineddf['start'].astype(int)
	combineddf['end']=combineddf['start']+2

	combineddf=combineddf[['chrom','start','end','#TP_fragment','#FP_fragment','#TN_fragment','#FN_fragment','#Total_Fragment','TPR','FPR','FDR','fileName']]

	
	prevtotalcpg=combineddf.shape[0]


	combineddf=SMrecordDF.merge(combineddf,on=['chrom','start','end'])


	newtotalcpg=combineddf.shape[0]

	if newtotalcpg < prevtotalcpg:
		print('some problem in merging')
		sys.exit(1)

	
	combineddf.to_csv(outfilename+"_cpgwise.txt",sep="\t", index=False)

	DMRwiseoutdf=DMRwise(combineddf)
	DMRwiseoutdf.to_csv(outfilename+"_DMRwise.txt",sep="\t", index=False)


	






	return combineddf,DMRwiseoutdf
	


def DMRwise(allinfodf):
	grouped=allinfodf.groupby(['DMRchr','DMRstart','DMRend'])

	
	DMRwiselist=[]
	for name, group in grouped:
		group_subset=(group[['#TP_fragment','#FP_fragment','#TN_fragment','#FN_fragment','#Total_Fragment','TPR','FPR','FDR']]).mean(axis=0)
		group_subset['fileName']=group['fileName'].tolist()[0]

		group_subset['DMRchr']=(group['DMRchr'].tolist())[0]
		group_subset['DMRstart']=(group['DMRstart'].tolist())[0]
		group_subset['DMRend']=(group['DMRend'].tolist())[0]


		group_subset=group_subset[['DMRchr','DMRstart','DMRend','#TP_fragment','#FP_fragment','#TN_fragment','#FN_fragment','#Total_Fragment','TPR','FPR','FDR','fileName']]


		DMRwiselist.append(group_subset)

	
	DMRwisedf=pd.DataFrame(DMRwiselist)
	return DMRwisedf







def CountFrequency(my_list):
 
	# Creating an empty dictionary
	freq = {}
	for item in my_list:
		if (item in freq):
			freq[item] += 1
		else:
			freq[item] = 1
	return freq

def fullcount(cpglist):
	cpglist_flat=[item for sublist in cpglist for item in sublist]
	cpglist_flat=list(map(eval,cpglist_flat))
	cpglist_flat=[i for i in cpglist_flat if i]
	cpglist_flat_freq=CountFrequency(cpglist_flat)
	return cpglist_flat_freq


def entryFullcount(edf,colname):
	allcpg=edf[colname].tolist()
	allcpg_freq=fullcount(allcpg)
	return allcpg_freq



