import pandas as pd


class Helpadapter:
    def __init__(self,df,colname):
        self.df=df
        self.colname=colname




    ###convert ['"\'CD4\'"', ' "\'CD8\'"'] to ["'CD4'","'CD8'"]##
    def adjustCellListRow(self):
        adjustedrows=[]
        for index, row in self.df.iterrows():

            if len(row['ucelltype'])>1 or row['ucelltype'][0]!="":
                row['ucelltype']=list(map(lambda x: eval(x),row['ucelltype']))



            adjustedrows.append(row)

        adjustedDF=pd.DataFrame(adjustedrows)

        return adjustedDF

