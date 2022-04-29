import numpy as np
import pandas as pd
import sys

ref_file = sys.argv[1]
test_file = sys.argv[2]
outfol = sys.argv[3]

df_ref = pd.read_csv(ref_file, comment='#', sep='\t',low_memory=False)
df_ref = df_ref[['ID', 'Chromosome_36', 'Coordinate_36']]

df_test = pd.read_csv(test_file, sep='\t', header=None, names=['ID_old', 'met'],low_memory=False)
df_test = df_test.dropna(how='any')
df_test_num = df_test.to_numpy()

df_ref = df_ref[df_ref.ID.isin(df_test_num.T[0])]
# df_test = df_test[df_test.ID_old.isin(np.array(df_ref['ID']))]
df_ref['ID_cat'] = pd.Categorical(
    df_ref['ID'], 
    categories=df_test_num.T[0], 
    ordered=True
)
df_ref = df_ref.sort_values('ID_cat')

df_test['chr'] = np.char.add('chr', np.array(df_ref['Chromosome_36'], dtype=str))
df_test['start'] = np.array(df_ref['Coordinate_36'])
df_test = df_test[df_test['start'] != 'MULTI']
df_test['end'] = np.array(df_test['start'], dtype=int) + 2
df_test = df_test[['chr', 'start', 'end', 'met']]
df_test = df_test.sort_values(by=['chr'])
df_test.to_csv(outfol + '/' + test_file.split('/')[-1] + '_blueprint.txt', index=None, header=None, sep='\t')