
import sys

class aRead:
    def __init__(self, rname, allcelltype,ucelltype,assignedcelltype, CheckedCpG,mismatchCpG,notacceptedCpG, accepetedCpG, **kwargs):
        self.ReadName=rname
        self.allcelltype=allcelltype
        self.ucelltype=ucelltype
        self.assinedcelltype=assignedcelltype

        self.checkedCpG=CheckedCpG
        self.mismatchCpG=mismatchCpG
        self.notacceptedCpG=notacceptedCpG
        self.acceptedCpG=accepetedCpG


        self.finalacceptedfor="notdetermined"
        self.finalrejectedfor="notdetermined"
        self.matefound="N"

    def mergewithmate(self,aReadobj):
        if self.ReadName!=aReadobj.ReadName:
            print("not mate. Exiting")
            print(self.ReadName)
            print(aReadobj.ReadName)
            sys.exit(1)


        newassignedcelltype=self.assinedcelltype


        if self.assinedcelltype!=aReadobj.assinedcelltype:
            if (len(self.acceptedCpG)<len(aReadobj.acceptedCpG)):
                newassignedcelltype=aReadobj.assinedcelltype
                fragment = aRead(self.ReadName, aReadobj.allcelltype,
                                 aReadobj.ucelltype, newassignedcelltype,
                                 aReadobj.checkedCpG,aReadobj.mismatchCpG,aReadobj.notacceptedCpG,
                                 aReadobj.acceptedCpG)


            elif self.assinedcelltype in ("lowmapq","DupRead"):
                newassignedcelltype=aReadobj.assinedcelltype
                fragment = aRead(self.ReadName, aReadobj.allcelltype,
                                 aReadobj.ucelltype, newassignedcelltype,
                                 aReadobj.checkedCpG,aReadobj.mismatchCpG,aReadobj.notacceptedCpG,
                                 aReadobj.acceptedCpG)

            elif aReadobj.assinedcelltype in ("lowmapq","DupRead"):
                newassignedcelltype = self.assinedcelltype

                fragment = aRead(self.ReadName, self.allcelltype,
                                 self.ucelltype, newassignedcelltype,
                                 self.checkedCpG,self.mismatchCpG,self.notacceptedCpG,
                                 self.acceptedCpG)


            elif (len(self.acceptedCpG)==len(aReadobj.acceptedCpG)):
                print("two mate has different assigned read. Interesting....the read info may be wrong.......")
                print(self.ReadName)
                print(len(self.acceptedCpG))
                print(self.assinedcelltype)
                print(aReadobj.assinedcelltype)
                print(self.allcelltype)
                print(aReadobj.allcelltype)
                fragment = aRead(self.ReadName, self.allcelltype + aReadobj.allcelltype,
                                 list(set(self.ucelltype + aReadobj.ucelltype)), newassignedcelltype,
                                 list(set(self.checkedCpG + aReadobj.checkedCpG)),list(set(self.mismatchCpG + aReadobj.mismatchCpG)),list(set(self.notacceptedCpG + aReadobj.notacceptedCpG)),
                                 list(set(self.acceptedCpG + aReadobj.acceptedCpG)))
            else:
                fragment = aRead(self.ReadName, self.allcelltype + aReadobj.allcelltype,
                                 self.ucelltype, newassignedcelltype,
                                 self.checkedCpG,self.mismatchCpG,self.notacceptedCpG,
                                 self.acceptedCpG)

        else:

            fragment=aRead(self.ReadName,self.allcelltype+aReadobj.allcelltype,list(set(self.ucelltype+aReadobj.ucelltype)),newassignedcelltype,list(set(self.checkedCpG+aReadobj.checkedCpG)),list(set(self.mismatchCpG + aReadobj.mismatchCpG)),list(set(self.notacceptedCpG + aReadobj.notacceptedCpG)),list(set(self.acceptedCpG+aReadobj.acceptedCpG)))

        fragment.matefound="Y"
        return fragment

