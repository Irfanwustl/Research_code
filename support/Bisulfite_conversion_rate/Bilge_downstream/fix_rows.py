import pandas as pd
import sys
import os
from statistics import mean
from statistics import stdev

import sys

direc = sys.argv[1]
files = os.listdir(direc)

if '.DS_Store' in files:
    files.remove('.DS_Store')

files.sort()

def get_cols(lst):
    header = []
    row = []
    rc3_seen = False
    for col in lst:
        col = str(col)
        if 'rc3' in col:
            val1 = col[:3]
            val2 = col[3:]
            header.append(val1)
            row.append(val2)
            rc3_seen = True
        if rc3_seen and 'rc3' not in col:
            row.append(col)
        elif not rc3_seen:
            header.append(col)
    rows = []
    rows.append(row)
    return header, rows

j = 0
if '.DS_Store' in files:
    j = 1

file = direc + '/' + files[j]
data = pd.read_csv(file, sep='\t', header=None)
df = pd.DataFrame(data)
lst = df.values.tolist()[0]
header, row = get_cols(lst)
    
df_all = pd.DataFrame(row, columns=header)
rc1 = float(list(df_all['rc1'])[0])
rc2 = float(list(df_all['rc2'])[0])
rc3 = float(list(df_all['rc3'])[0])
df_all['1 - rc1'] = 1.0 - rc1
df_all['1 - rc2'] = 1.0 - rc2
df_all['1 - rc3'] = 1.0 - rc3
df_all['1 - mean(rc)'] = 1.0 - mean([rc1, rc2, rc3])

for i in range(j + 1, len(files)):
    file = direc + '/' + files[i]
    if 'DS_Store' not in files[i]:
        data = pd.read_csv(file, sep='\t', header=None)
        df = pd.DataFrame(data)
        lst = df.values.tolist()[0]
    
        header, rows = get_cols(lst)
    
        df_new = pd.DataFrame(rows, columns=header)
    
        rc1 = float(list(df_new['rc1'])[0])
        rc2 = float(list(df_new['rc2'])[0])
        rc3 = float(list(df_new['rc3'])[0])
        df_new['1 - rc1'] = 1.0 - rc1
        df_new['1 - rc2'] = 1.0 - rc2
        df_new['1 - rc3'] = 1.0 - rc3
        df_new['1 - mean(rc)'] = 1.0 - mean([rc1, rc2, rc3])
        df_all = pd.concat([df_new, df_all])

df_all.to_csv(direc + '_all.txt', sep='\t', index=None)

combined = {}
for file in list(df_all['file']):
    split = file.split('_')
    j = 0
    for i in range(len(split)):
        if 'readnum' in split[i]:
            j = i
    if split[j] in combined:
        combined[split[j]].append(file)
    else:
        combined[split[j]] = []
        combined[split[j]].append(file)
        
combined_cols = ['file', 'rc1', 'rc1_stdev', 'rc2', 'rc2_stdev', 'rc3', 'rc3_stdev', '1 - rc1', '1-rc1_stdev', '1 - rc2', '1-rc2_stdev', '1 - rc3', '1-rc3_stdev', '1 - mean(rc)', '1-mean(rc)_stdev']
df_combined = pd.DataFrame(columns=combined_cols)

lst = ['rc1', 'rc2', 'rc3', '1 - rc1', '1 - rc2', '1 - rc3', '1 - mean(rc)']
for key in list(combined.keys()):
    row = []
    row.append(key)
    df_slice = df_all[df_all['file'].isin(combined[key])]
    for col in lst:
        avg = pd.to_numeric(df_slice[col]).mean(axis=0)
        std = stdev(list(pd.to_numeric(df_slice[col])))
        row.append(avg)
        row.append(std)
        
    df_new = pd.DataFrame([row], columns=combined_cols)
    df_combined = pd.concat([df_new, df_combined])

df_combined.to_csv(direc + '_combined.txt', sep='\t', index=None)
