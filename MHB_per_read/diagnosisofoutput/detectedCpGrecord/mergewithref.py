import sys
import pandas as pd

ref=sys.argv[1]

rdoutcpgrecord=sys.argv[2]

out=sys.argv[3]



refdf=pd.read_csv(ref,sep="\t",index_col=0)
rdoutcpgrecorddf=pd.read_csv(rdoutcpgrecord,sep="\t",index_col=0)

frame = pd.concat([refdf,rdoutcpgrecorddf], axis=1)

frame = frame.fillna(0)

frame.index.name = 'position'

frame.to_csv(out,sep="\t")