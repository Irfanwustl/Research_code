

import pandas as pd
import sys

infile=sys.argv[1]

outfile=sys.argv[2]


outdf=pd.read_csv(infile,sep='\t',index_col=0)


outdf_nomono=outdf.drop(['Mono'],axis=1)
outdf_nomono.head()


# In[14]:


outdf_nomono_normalized=(outdf_nomono.div(outdf_nomono.sum(axis=1), axis=0))*100
outdf_nomono_normalized['total']=outdf_nomono_normalized.sum(axis=1)
outdf_nomono_normalized.head()



outdf_nomono_normalized.to_csv(outfile+"_nomono",sep='\t')