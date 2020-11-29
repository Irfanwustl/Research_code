import collections
import pandas as pd

class ScalingFactorTools:

    # works for a list of frozen sets
    def countDupInalistofSet(self,dupset):
        counter = collections.Counter(dupset)
        return dict(counter)


    #linkage group should be in a set
    def mergeLinkagegroup(self,df):
        df=df.copy()
        df['merged'] = 'no'

        totalrow=df.shape[0]


        i=0
        while i < totalrow:
            currentrow=df.iloc[i,:]
            print(currentrow)


            j=i+1
            while j < totalrow:

                comprow=df.iloc[j,:]

                print("in comprow",)
                print(comprow)
                j=j+1


            i=i+1























if __name__ == "__main__":
    test=ScalingFactorTools()
    vowels = {'a', 'e', 'i','a', 'o', 'u'}
    vowels2 = {'a', 'e', 'i', 'a', 'o','u'}

    fSet1 = frozenset(vowels)
    fSet2=frozenset(vowels2)
    flist=[fSet1,fSet2]

    #print(flist)

    #print(test.countDupInalistofSet(flist))


    toydf=pd.read_csv("/Users/irffanalahi/Research/Research_code/gitignorefolder/MHB_per_read/moretest/scaling_factorbased/toy.txt",sep="\t")
    toydf['linkageGroup'] = toydf.linkageGroup.apply(lambda x: set(x[1:-1].split(',')))  #####################check it
    test.mergeLinkagegroup(toydf)


    #print(toydf.loc[0,'linkageGroup'])

    #print(type(toydf.loc[0,'linkageGroup']))