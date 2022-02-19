#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Shoonhsin Li
# 02/10/2022

import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
import csv
import sys
import os

"""
Some important details:

- this works for the directory path in my Box drive using os, so otherwise change mypath variable
- I took the absolute value of the average in both graph and text file
- Files are not in any particular order except the default for listdir

"""
mypath = sys.argv[1]   #'cm4_thresholdpos_allthresholdcombinations_0.5_100_linked_2_radius_100'

outfile=sys.argv[2]

filenames = [f for f in listdir(mypath) if isfile(join(mypath, f))] # only adds the files
totals = []
avgs = []
counts = []
names = []
nums = [str(i) for i in list(range(0, 10))]

# find avg and count for each file
for filename in filenames:
    
    # label by file name
    names.append(filename)
    # determine average number
    split_lst = filename.split("_")
    total = 0
    n = 0
    for split in split_lst:
        if "-" in split and split[-1] in nums: # confirm that the substring is a negative number
            n += 1
            total += float(split)
    totals.append(abs(total))
    avgs.append(abs(total / n))
    
    # determine number of lines
    with open(join(mypath, filename), 'r') as f:
        count = 0 #-1 # account for first row
        for line in f:
            count += 1
    counts.append(count)

# write text file with name, 2st column avgs and 3rd column counts
L = zip(names, avgs, counts) # list of lists of the avg, count per file
df = pd.DataFrame(L, columns=["Filename","Average Value","Line Count"])
df.to_csv(outfile+".txt", index=None, sep='\t')

#
# with open("Shoonhsin_avg_and_linecount.txt", 'w', newline='') as f1:
    # writer= csv.writer(f1, delimiter='\t')
    # writer.writerow(["Average value", "Line count"])
    # writer.writerows(L)


# In[2]:


def renamect(act):
    if act=='CD4':
        return 'Naive CD4 T'
    if act=='CD8':
        return 'Naive CD8 T'

    if act=='NaiveCD4':
        return 'Naive CD4 T'
    if act=='NaiveCD8':
        return 'Naive CD8 T'
    if act=='Tr':
        return 'Tregs'
    if act=='mB':
        return 'Memory B'
    if act=='nB':
        return 'Naive B'
    if act=='m4':
        return 'Memory CD4 T'
    if act=='m8':
        return 'Memory CD8 T'
    if act=='Mn':
        return 'Monocyte'


    if act=='em8':
        return 'CD8 TEM'
    if act=='cm8':
        return 'CD8 TCM'

    if act=='em4':
        return 'CD4 TEM'
    if act=='cm4':
        return 'CD4 TCM'


    if act=='ed8':
        return 'CD8 TEMRA'

    if act=='PC':
        return 'PC'

    if act=='M0':
        return 'Mac (M0)'

    if act=='M1':
        return 'Mac (M1)'

    if act=='M2':
        return 'Mac (M2)'
    if act=='Eo':
        return 'Eos'

    if act=='Mg':
        return 'MK'




    return act


# make plot with average value
import matplotlib.pyplot as plt




fortitlesplit=(os.path.basename(mypath)).split("_")[0]

plt.semilogy(avgs, counts, 'o')
plt.title(renamect(fortitlesplit),fontsize=20)
plt.xlabel("Average delta",fontsize=18)
plt.ylabel("#CpG",fontsize=18)
plt.savefig(outfile+"_avg_linecount_plot.pdf")
#plt.show()

'''
# make plot with value sum
plt.semilogy(totals, counts, 'o')
plt.title("Value Sum versus Line Count")
plt.xlabel("Value Sum")
plt.ylabel("Line count")
plt.savefig(mypath+"_sum_linecount_plot.pdf")
plt.show()
'''


# In[ ]:




