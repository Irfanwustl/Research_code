import collections
import pandas as pd

class ScalingFactorTools:

    # works for a list of frozen sets
    def countDupInalistofSet(self,dupset):
        counter = collections.Counter(dupset)
        return dict(counter)


    #linkage group should be in a set. Merging should be done for ref after generating one large scale mastedr df for all pure files.
    def mergeLinkagegroup(self,df,similarity_rate=0.75):
        df=df.copy()
        df['merged'] = 'no'

        totalrow=df.shape[0]


        i=0
        while i < totalrow:
            currentrow=df.iloc[i,:]
            currentLG=currentrow['LinkageGroup']


            j=i+1
            while j < totalrow:

                comprow=df.iloc[j,:]

                print("in comprow")
                compLG=comprow['LinkageGroup']

                intersected = currentLG.intersection(compLG)

                if len(currentLG) >= len(compLG):
                    maxlen=len(currentLG)
                else:
                    maxlen=len(compLG)

                if len(intersected) >= similarity_rate*maxlen:
                    self.coreMerge(currentrow,comprow)


                j=j+1


            i=i+1


    ##should check cell type too#####
    ### not completed################################################################################################################################
    def coreMerge(self,row1,row2):
        if row1['TrueCellType']!=row2['TrueCellType']:
            pass ######################################

        else:
            newpos=row1["positive"]+row2["positive"]
            newneg=row1["negative"]+row2["negative"]
            newtotal=newpos+newneg
            newposDividedByTotal=(1.0*newpos)/newtotal






















if __name__ == "__main__":
    test=ScalingFactorTools()
    vowels = {'a', 'e', 'i','a', 'o', 'u'}
    vowels2 = {'a', 'e', 'i', 'a', 'o','u'}

    fSet1 = frozenset(vowels)
    fSet2=frozenset(vowels2)
    flist=[fSet1,fSet2]

    #print(flist)

    #print(test.countDupInalistofSet(flist))


    toydf=pd.read_csv("/Users/irffanalahi/Research/Research_code/gitignorefolder/MHB_per_read/moretest/scaling_factorbased/BULK-PBMC-1313_final_neu_toy.txt_scaleinfo.txt",sep="\t")
    toydf['LinkageGroup'] = toydf.LinkageGroup.apply(lambda x: set(x[1:-1].split(',')))  #####################check it
    test.mergeLinkagegroup(toydf)


    #print(toydf.loc[0,'linkageGroup'])

    #print(type(toydf.loc[0,'linkageGroup']))