import sys
import glob
import os.path
import pandas as pd



class Info:
    def __init__(self, sample, poslist, **kwargs):
        self.sample=sample
        self.poslist=poslist

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return  str(self.__dict__)

class InvertedInfo:
    def __init__(self, pos,samplelist, **kwargs):
        self.pos=pos
        self.samplelist=samplelist
        self.count=len(self.samplelist)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return  str(self.__dict__)

    def to_dict(self):
        return {
            'pos': self.pos,
            'samplelist': self.samplelist,
            'count': self.count,
        }

class ReportGenerator:
    def __init__(self, infolder, outname, **kwargs):
        self.infolder=infolder
        self.outname=outname

        self.coreAlgo()




    def coreAlgo(self):
        infolist=self.readallfiles()



        countcommonlist=self.countcommon(infolist)

        self.savecountcommoninfo(countcommonlist)



    def savecountcommoninfo(self,countcommonlist):


        outdf=pd.DataFrame.from_records([s.to_dict() for s in countcommonlist])

        outdf.to_csv(self.outname,sep="\t",index=False)




    def countcommon(self,infolist):

        infolistlen=len(infolist)
        outlist=[]
        i=0
        while i< infolistlen:
            poslist=infolist[i].poslist
            for pos in poslist:
                samplelist=[infolist[i].sample]

                j=i+1
                while j<infolistlen:

                    if pos in infolist[j].poslist:
                        samplelist.append(infolist[j].sample)
                        infolist[j].poslist.remove(pos)



                    j=j+1

                ii=InvertedInfo(pos,samplelist)
                outlist.append(ii)

            i=i+1

        return outlist



    def readallfiles(self):
        allfiles=glob.glob(self.infolder+"/*.txt")


        infolist=[]
        for file in allfiles:
            with open(file) as f:
                lines = [line.rstrip() for line in f]

                info=Info(os.path.basename(file),lines)
                infolist.append(info)

        return infolist








def main():
    infolder = sys.argv[1]
    outname = sys.argv[2]

    rg = ReportGenerator(infolder,outname)


if __name__ == '__main__':
    main()
