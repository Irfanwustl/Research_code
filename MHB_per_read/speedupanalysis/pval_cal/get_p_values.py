import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu
import sys
import subprocess

def get_p(df,col,c1,c2):
    try:
        stat, dfei = mannwhitneyu(df[df['Response']==c1][col],
                                         df[df['Response']==c2][col],
                                         alternative='two-sided')
    except:
        dfei = np.nan
    return dfei

response_file = sys.argv[1]
rc_file_directory = sys.argv[2]
output_file = sys.argv[3]

df_resp = pd.read_csv(response_file, sep='\t')

bash_command = 'ls '+rc_file_directory
process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
rc_file_list, error = process.communicate()
rc_file_list = rc_file_list.decode("utf-8")
rc_file_list = rc_file_list.splitlines()
rc_file_list = [rc_file_directory+'/'+rc_file_list[i] for i in range(len(rc_file_list))]

base_col_names = ['PreTxDCBvsNDB_','PreTxDCBvsHealthy_','PreTxNDBvsHealthy_','OnTxDCBvsNDB_',
                      'OnTxDCBvsHealthy_','OnTxNDBvsHealthy_']

df_rc_first = pd.read_csv(rc_file_list[0], sep='\t')

col_cats = np.array(df_rc_first.drop(columns='Mixture').columns)
col_names = []

for col in col_cats:
    col_names.append([base_col_names[i]+col for i in range(len(base_col_names))])

col_names = list(np.concatenate(col_names).flat)
df_out = pd.DataFrame(columns=col_names)

for rc_file in rc_file_list:

    df_rc = pd.read_csv(rc_file, sep='\t')
    df = df_rc.merge(df_resp,on='Mixture')

    if len(df['Time point'].unique())!=3:
        print('ERROR: invalid time point')

    df_pretx = df[df['Time point'] != 'on tx']
    df_pretx = df_pretx[df_pretx['Response']!='exclude ']
    df_ontx = df[df['Time point'] != 'pre tx']
    df_ontx = df_ontx[df_ontx['Response']!='Exclude ']
    df_entry = np.zeros(len(col_cats)*6)

    i = 0
    for col in col_cats:

        df_entry[i] = get_p(df_pretx,col,'DCB','NDB')
        i += 1
        df_entry[i] = get_p(df_pretx,col,'DCB','Healthy')
        i += 1
        df_entry[i] = get_p(df_pretx,col,'NDB','Healthy')
        i += 1
        df_entry[i] = get_p(df_ontx,col,'DCB','NDB')
        i += 1
        df_entry[i] = get_p(df_ontx,col,'DCB','Healthy')
        i += 1
        df_entry[i] = get_p(df_ontx,col,'NDB','Healthy')
        i += 1

    df_out.loc[rc_file] = df_entry

df_out.to_csv(output_file,sep="\t")
