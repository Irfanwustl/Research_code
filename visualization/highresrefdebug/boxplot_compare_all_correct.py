import pandas as pd
import itertools

from matplotlib import pyplot as plt
import seaborn as sns
from statannot import add_stat_annotation
import sys
import os
import shutil

datatypelist=[]

f1="/Users/irffanalahi/Research/Research_update/Dataqc/allqc_together/WB_PBMC/Wetlab/pevPBMCLabQC-080221.txt"
df1=pd.read_csv(f1,sep="\t")
tmpdata='CRC PBMC (n=' + str(len(df1)) + ')'
df1['data']=tmpdata
datatypelist.append(tmpdata)

f2="/Users/irffanalahi/Research/Research_update/Dataqc/allqc_together/WB_PBMC/Wetlab/melPBMCLabQC-080221.txt"
df2=pd.read_csv(f2,sep="\t")
tmpdata='SKCM PBMC (n=' + str(len(df2)) + ')'
df2['data']=tmpdata
datatypelist.append(tmpdata)

f3="/Users/irffanalahi/Research/Research_update/Dataqc/allqc_together/WB_PBMC/Wetlab/Healthy_cfDNA_and_WB_QC_ 072721_WBonly.txt"
df3=pd.read_csv(f3,sep="\t")
tmpdata='Healthy WB (n=' + str(len(df3)) + ')'
df3['data']=tmpdata
datatypelist.append(tmpdata)

outputfile=f3
outputfolder=os.path.dirname(outputfile)

dflist=[df1,df2,df3] ###########


######duplication_rate####
valuevars=['d50th_ptle','50th_ptle','total','secondary','supplementary','duplicates','mapped','mapped_percent','paired_in_sequencing','read1','read2','properly_paired','properly_paired_percentage','with_itself_and_mate_mapped','singletons','with_mate_mapped_to_a_different_chr','with_mate_mapped_to_a_different_chr_mapQ>=5','duplication_rate']

#valuevars=['rc1','rc1_stdev','rc2','rc2_stdev','rc3','rc3_stdev','1 - rc1','1-rc1_stdev','1 - rc2','1-rc2_stdev','1 - rc3','1-rc3_stdev','1 - mean(rc)','1-mean(rc)_stdev','BCR']
valuevars=['Total DNA amount (ng)','gDNA used for Lib prep (ng)','Unmethylated Lambda DNA- 0.5% (ng)','gDNA (ng) for BS conversion','Indexing PCR cycles','Target sequencing Depth','Library Avg. Fragment size (Bioanalyzer)','Final Lib. Conc. (ng/ul)','Elution vol. (ul)','Total amount of Lib (ng)','dsDNA-MW (660) x Avg. Fragment size','nM of Library/ul']
#valuevars=['Plasma vol. (ml)','cfDNA amount (ng)','cfDNA amount (ng/ml)','Total cfDNA amt (ng) including previous extractions','Bioanalyzer 70bp-450bp percentage']#	'Indexing PCR cycles'	Final Lib. Conc. (ng/ul)	Elution vol. (ul)	Total amount of Lib (ng)

alldf = pd.concat(dflist)

cols = []
values = []

for col in alldf.columns:
    split = col.split('_')
    joined = '-'.join(split)
    cols.append(joined)
    
for col in valuevars:
    split = col.split('_')
    joined = '-'.join(split)
    values.append(joined)

alldf.columns = cols
valuevars = values

mdf = pd.melt(alldf, id_vars=['data'], value_vars=valuevars)

def combine_box_pairs(samples, cell_types):
    box_pairs = []
    for cell in cell_types:
        pairs = []
        for sample in samples:
            pairs.append((cell, sample))
        for i in range(len(samples)):
            try:
                box_pairs.append((pairs[i], pairs[i + 1]))
            except IndexError:
                box_pairs.append((pairs[i], pairs[0]))
    return box_pairs

fig, axs = plt.subplots(1, len(valuevars), figsize=(len(valuevars)*5, 10))

p_vals_fol = outputfolder + '/p_vals'
os.mkdir(p_vals_fol)

for i in range(len(valuevars)):
    axs[i] = sns.boxplot(x="variable", y="value", hue="data", data=mdf[mdf['variable'] == valuevars[i]],palette="Set3", ax = axs[i])
    axs[i].legend([],[], frameon=False)
    Box_pairs=combine_box_pairs(datatypelist, [valuevars[i]])
    original_stdout = sys.stdout

    with open(p_vals_fol + '/p_vals' + str(i) + '.txt', 'w') as f:
        sys.stdout = f # Change the standard output to the file we created.
        test_results = add_stat_annotation(axs[i],data=mdf[mdf['variable'] == valuevars[i]], x="variable", y="value", hue="data",box_pairs=Box_pairs,
                                   test='Mann-Whitney', text_format='star', comparisons_correction=None)
        sys.stdout = original_stdout # Reset the standard output to its original value
        f.close()

lines, labels = axs[0].get_legend_handles_labels()
fig.legend(lines, labels, loc=(0.933, 0.86))

fig.savefig(outputfile+"_all_separate.pdf",dpi=300, bbox_inches='tight')
plt.savefig('separate_example_non-hue_outside_all.png', dpi=300, bbox_inches='tight')

sig_comparison = []

for i in range(len(valuevars)):
    file_out = open(p_vals_fol + '/p_vals' + str(i) + '.txt', 'r')
    Lines = file_out.readlines()
    file_out.close()

    sig_list = []

    for line in Lines:
        if 'P_val' in line:
            split = line.split(' ')
            for name in split:
                if 'P_val' in name:
                    res = name.split('=')
                    if float(res[1]) < 0.05:
                        new_line = line.split('_')
                        cell = new_line[0]
                        val1 = new_line[1].split(' v.s.')[0]
                        val2 = new_line[2].split(':')[0]
                        sig_list.append(((cell, val1), (cell, val2)))
    sig_comparison.append(sig_list)

fig, axs = plt.subplots(1, len(valuevars), figsize=(len(valuevars)*5, 10))

for i in range(len(valuevars)):
    axs[i] = sns.boxplot(x="variable", y="value", hue="data", data=mdf[mdf['variable'] == valuevars[i]],palette="Set3", ax = axs[i])
    axs[i].legend([],[], frameon=False)
    Box_pairs=sig_comparison[i]
    if len(Box_pairs) != 0:
        test_results = add_stat_annotation(axs[i],data=mdf[mdf['variable'] == valuevars[i]], x="variable", y="value", hue="data",box_pairs=Box_pairs,
                                    test='Mann-Whitney', text_format='star', comparisons_correction=None)

lines, labels = axs[0].get_legend_handles_labels()
fig.legend(lines, labels, loc=(0.933, 0.86))

fig.savefig(outputfile+"_significant_separate.pdf",dpi=300, bbox_inches='tight')
plt.savefig('separate_example_non-hue_outside_significant.png', dpi=300, bbox_inches='tight')

plt.figure(figsize=(20,10))
ax = sns.boxplot(x="variable", y="value", hue="data", data=mdf,palette="Set3") 

Box_pairs = combine_box_pairs(datatypelist, valuevars)

original_stdout = sys.stdout

with open(outputfolder + '/p_vals.txt', 'w') as f:
    sys.stdout = f # Change the standard output to the file we created.
    test_results = add_stat_annotation(ax,data=mdf, x="variable", y="value", hue="data",box_pairs=Box_pairs,
                                   test='Mann-Whitney', text_format='star', comparisons_correction=None)
    sys.stdout = original_stdout # Reset the standard output to its original value
    f.close()

ax.figure.savefig(outputfile+"_all_combined.pdf",dpi=300, bbox_inches='tight')
plt.savefig('example_non-hue_outside_all.png', dpi=300, bbox_inches='tight')

file_out = open(outputfolder + '/p_vals.txt', 'r')
Lines = file_out.readlines()
file_out.close()

sig_list = []

for line in Lines:
    if 'P_val' in line:
        split = line.split(' ')
        for name in split:
            if 'P_val' in name:
                res = name.split('=')
                if float(res[1]) < 0.05:
                    new_line = line.split('_')
                    cell = new_line[0]
                    val1 = new_line[1].split(' v.s.')[0]
                    val2 = new_line[2].split(':')[0]
                    sig_list.append(((cell, val1), (cell, val2)))

plt.figure(figsize=(20,10))
ax = sns.boxplot(x="variable", y="value", hue="data", data=mdf,palette="Set3") 

test_results = add_stat_annotation(ax,data=mdf, x="variable", y="value", hue="data",box_pairs=sig_list,
                                   test='Mann-Whitney', text_format='star', comparisons_correction=None)

ax.figure.savefig(outputfile+"_significant_combined.pdf",dpi=300, bbox_inches='tight')
plt.savefig('example_non-hue_outside_significant.png', dpi=300, bbox_inches='tight')

