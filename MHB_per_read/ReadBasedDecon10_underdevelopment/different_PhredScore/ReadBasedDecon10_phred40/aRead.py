
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



        ########### extra info########

        self.hypolist=[]
        self.lenhypolist=-1
        self.hyperlist=[]
        self.lenhyperlist=-1
        self.allnotmatched=[]
        self.lenallnotmatched=-1
        self.fraglength=-1

        self.interofhypohyper=[]
        self.leninterofhypohyper=-1




    def setextrainfo(self,hypolist, len_hypolist, hyperlist, len_hyperlist, allnotmatched, len_allnotmatched, fraglength):
        self.hypolist=hypolist
        self.lenhypolist=len_hypolist
        self.hyperlist=hyperlist
        self.lenhyperlist=len_hyperlist
        self.allnotmatched=allnotmatched
        self.lenallnotmatched=len_allnotmatched
        self.fraglength=fraglength

    def getextrainfo(self):
        return self.hypolist, self.lenhypolist, self.hyperlist, self.lenhyperlist, self.allnotmatched, self.lenallnotmatched, self.fraglength

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
                temphypolist, templenhypolist, temphyperlist, templenhyperlist, tempallnotmatched, templenallnotmatched, tempfraglength=aReadobj.getextrainfo()
                fragment.setextrainfo(temphypolist, templenhypolist, temphyperlist, templenhyperlist, tempallnotmatched, templenallnotmatched, tempfraglength)


            elif self.assinedcelltype in ("lowmapq","DupRead"):
                newassignedcelltype=aReadobj.assinedcelltype
                fragment = aRead(self.ReadName, aReadobj.allcelltype,
                                 aReadobj.ucelltype, newassignedcelltype,
                                 aReadobj.checkedCpG,aReadobj.mismatchCpG,aReadobj.notacceptedCpG,
                                 aReadobj.acceptedCpG)

                temphypolist, templenhypolist, temphyperlist, templenhyperlist, tempallnotmatched, templenallnotmatched, tempfraglength = aReadobj.getextrainfo()
                fragment.setextrainfo(temphypolist, templenhypolist, temphyperlist, templenhyperlist, tempallnotmatched,templenallnotmatched, tempfraglength)


            elif aReadobj.assinedcelltype in ("lowmapq","DupRead"):
                newassignedcelltype = self.assinedcelltype

                fragment = aRead(self.ReadName, self.allcelltype,
                                 self.ucelltype, newassignedcelltype,
                                 self.checkedCpG,self.mismatchCpG,self.notacceptedCpG,
                                 self.acceptedCpG)

                temphypolist, templenhypolist, temphyperlist, templenhyperlist, tempallnotmatched, templenallnotmatched, tempfraglength = self.getextrainfo()
                fragment.setextrainfo(temphypolist, templenhypolist, temphyperlist, templenhyperlist, tempallnotmatched,templenallnotmatched, tempfraglength)






            elif (len(self.acceptedCpG)==len(aReadobj.acceptedCpG)):
                
                '''
                print("two mate has different assigned read. Interesting....the read info may be wrong.......")
                print(self.ReadName)
                print(len(self.acceptedCpG))
                print(self.assinedcelltype)
                print(aReadobj.assinedcelltype)
                print(self.allcelltype)
                print(aReadobj.allcelltype)
                '''

                fragment = aRead(self.ReadName, self.allcelltype + aReadobj.allcelltype,
                                 list(set(self.ucelltype + aReadobj.ucelltype)), newassignedcelltype,
                                 list(set(self.checkedCpG + aReadobj.checkedCpG)),list(set(self.mismatchCpG + aReadobj.mismatchCpG)),list(set(self.notacceptedCpG + aReadobj.notacceptedCpG)),
                                 list(set(self.acceptedCpG + aReadobj.acceptedCpG)))

                hypolist, len_hypolist, hyperlist, len_hyperlist, notmatched, len_notmatched, fragmentlength, interofhypohyper, leninterofhypohyper=self.mergeextrainfo(aReadobj)

                fragment.setextrainfo(hypolist, len_hypolist, hyperlist, len_hyperlist, notmatched, len_notmatched, fragmentlength)
                fragment.interofhypohyper=interofhypohyper
                fragment.leninterofhypohyper=leninterofhypohyper

            else:
                fragment = aRead(self.ReadName, self.allcelltype + aReadobj.allcelltype,
                                 self.ucelltype, newassignedcelltype,
                                 self.checkedCpG,self.mismatchCpG,self.notacceptedCpG,
                                 self.acceptedCpG)

                temphypolist, templenhypolist, temphyperlist, templenhyperlist, tempallnotmatched, templenallnotmatched, tempfraglength = self.getextrainfo()
                fragment.setextrainfo(temphypolist, templenhypolist, temphyperlist, templenhyperlist, tempallnotmatched, templenallnotmatched, tempfraglength)


        else:

            fragment=aRead(self.ReadName,self.allcelltype+aReadobj.allcelltype,list(set(self.ucelltype+aReadobj.ucelltype)),newassignedcelltype,list(set(self.checkedCpG+aReadobj.checkedCpG)),list(set(self.mismatchCpG + aReadobj.mismatchCpG)),list(set(self.notacceptedCpG + aReadobj.notacceptedCpG)),list(set(self.acceptedCpG+aReadobj.acceptedCpG)))

            hypolist, len_hypolist, hyperlist, len_hyperlist, notmatched, len_notmatched, fragmentlength, interofhypohyper, leninterofhypohyper = self.mergeextrainfo(aReadobj)

            fragment.setextrainfo(hypolist, len_hypolist, hyperlist, len_hyperlist, notmatched, len_notmatched,fragmentlength)
            fragment.interofhypohyper = interofhypohyper
            fragment.leninterofhypohyper = leninterofhypohyper
        fragment.matefound="Y"
        return fragment



    def mergeextrainfo(self,aReadobj):
        shypolist, slen_hypolist, shyperlist, slen_hyperlist, sallnotmatched, slen_allnotmatched, sfraglength=self.getextrainfo()
        ahypolist, alen_hypolist, ahyperlist, alen_hyperlist, aallnotmatched, alen_allnotmatched, afraglength=aReadobj.getextrainfo()

        hypolist=list(set(shypolist+ahypolist))
        hyperlist=list(set(shyperlist+ahyperlist))

        hyposet=set(hypolist)
        hyperset=set(hyperlist)

        interofhypohyper=list(hyposet.intersection(hyperset))
        leninterofhypohyper=len(interofhypohyper)



        notmatched = list(set(sallnotmatched+aallnotmatched).difference((hyposet.union(hyperset))))


        fragmentlength=1.0*(sfraglength+afraglength)/2


        return hypolist,len(hypolist),hyperlist,len(hyperlist),notmatched,len(notmatched),fragmentlength,interofhypohyper,leninterofhypohyper
