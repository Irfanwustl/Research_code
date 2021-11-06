
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



        self.CT_checked=[]
        self.CT_checked_length=-1
        self.CpG_checked=[]
        self.CpG_checked_length=-1

        self.CT_mismatch=[]
        self.CT_mismatch_length=-1
        self.CpG_mismatch=[]
        self.CpG_mismatch_length=-1

        self.CT_accepted=[]
        self.CT_accepted_length=-1
        self.CpG_accepted=[]
        self.CpG_accepted_length=-1

        self.CT_notacceped=[]
        self.CT_notacceped_length=-1
        self.CpG_notacceped=[]
        self.CpG_notacceped_length=-1




    def setextrainfo(self,hypolist, len_hypolist, hyperlist, len_hyperlist, allnotmatched, len_allnotmatched, fraglength,CT_checked,CpG_checked,CT_mismatch,CpG_mismatch,CT_accepted,CpG_accepted,CT_notacceped,CpG_notacceped):
        self.hypolist=hypolist
        self.lenhypolist=len_hypolist
        self.hyperlist=hyperlist
        self.lenhyperlist=len_hyperlist
        self.allnotmatched=allnotmatched
        self.lenallnotmatched=len_allnotmatched
        self.fraglength=fraglength


        self.CT_checked=CT_checked
        self.CT_checked_length=len(CT_checked)
        self.CpG_checked=CpG_checked
        self.CpG_checked_length=len(CpG_checked)

        self.CT_mismatch=CT_mismatch
        self.CT_mismatch_length=len(CT_mismatch)
        self.CpG_mismatch=CpG_mismatch
        self.CpG_mismatch_length=len(CpG_mismatch)

        self.CT_accepted=CT_accepted
        self.CT_accepted_length=len(CT_accepted)
        self.CpG_accepted=CpG_accepted
        self.CpG_accepted_length=len(CpG_accepted)

        self.CT_notacceped=CT_notacceped
        self.CT_notacceped_length=len(CT_notacceped)
        self.CpG_notacceped=CpG_notacceped
        self.CpG_notacceped_length=len(CpG_notacceped)

    def getextrainfo(self):
        return self.hypolist, self.lenhypolist, self.hyperlist, self.lenhyperlist, self.allnotmatched, self.lenallnotmatched, self.fraglength, self.CT_checked,self.CpG_checked,self.CT_mismatch,self.CpG_mismatch,self.CT_accepted,self.CpG_accepted,self.CT_notacceped,self.CpG_notacceped

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

                temphypolist, templenhypolist, temphyperlist, templenhyperlist, tempallnotmatched, templenallnotmatched, tempfraglength, tempCT_checked,tempCpG_checked,tempCT_mismatch,tempCpG_mismatch,tempCT_accepted,tempCpG_accepted,tempCT_notacceped,tempCpG_notacceped = aReadobj.getextrainfo()
                fragment.setextrainfo(temphypolist, templenhypolist, temphyperlist, templenhyperlist, tempallnotmatched, templenallnotmatched, tempfraglength, tempCT_checked,tempCpG_checked,tempCT_mismatch,tempCpG_mismatch,tempCT_accepted,tempCpG_accepted,tempCT_notacceped,tempCpG_notacceped)
                
         


            elif aReadobj.assinedcelltype in ("lowmapq","DupRead"):
                newassignedcelltype = self.assinedcelltype

                fragment = aRead(self.ReadName, self.allcelltype,
                                 self.ucelltype, newassignedcelltype,
                                 self.checkedCpG,self.mismatchCpG,self.notacceptedCpG,
                                 self.acceptedCpG)

                
                temphypolist, templenhypolist, temphyperlist, templenhyperlist, tempallnotmatched, templenallnotmatched, tempfraglength, tempCT_checked,tempCpG_checked,tempCT_mismatch,tempCpG_mismatch,tempCT_accepted,tempCpG_accepted,tempCT_notacceped,tempCpG_notacceped = self.getextrainfo()
                fragment.setextrainfo(temphypolist, templenhypolist, temphyperlist, templenhyperlist, tempallnotmatched, templenallnotmatched, tempfraglength, tempCT_checked,tempCpG_checked,tempCT_mismatch,tempCpG_mismatch,tempCT_accepted,tempCpG_accepted,tempCT_notacceped,tempCpG_notacceped)






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



            else:
                fragment = aRead(self.ReadName, self.allcelltype + aReadobj.allcelltype,
                                 self.ucelltype, newassignedcelltype,
                                 self.checkedCpG,self.mismatchCpG,self.notacceptedCpG,
                                 self.acceptedCpG)




        else:


            fragment=aRead(self.ReadName,self.allcelltype+aReadobj.allcelltype,list(set(self.ucelltype+aReadobj.ucelltype)),newassignedcelltype,list(set(self.checkedCpG+aReadobj.checkedCpG)),list(set(self.mismatchCpG + aReadobj.mismatchCpG)),list(set(self.notacceptedCpG + aReadobj.notacceptedCpG)),list(set(self.acceptedCpG+aReadobj.acceptedCpG)))





        if (self.assinedcelltype not  in ("lowmapq","DupRead")) and (aReadobj.assinedcelltype not in ("lowmapq","DupRead")):
            hypolist, len_hypolist, hyperlist, len_hyperlist, notmatched, len_notmatched, fragmentlength, CT_checked,CpG_checked,CT_mismatch,CpG_mismatch,CT_accepted,CpG_accepted,CT_notacceped, CpG_notacceped, interofhypohyper, leninterofhypohyper = self.mergeextrainfo(aReadobj)

            fragment.setextrainfo(hypolist, len_hypolist, hyperlist, len_hyperlist, notmatched, len_notmatched, fragmentlength, CT_checked,CpG_checked,CT_mismatch,CpG_mismatch,CT_accepted,CpG_accepted,CT_notacceped, CpG_notacceped)
            fragment.interofhypohyper = interofhypohyper
            fragment.leninterofhypohyper = leninterofhypohyper


        fragment.matefound="Y"
        return fragment



    def mergeextrainfo(self,aReadobj):
        shypolist, slen_hypolist, shyperlist, slen_hyperlist, sallnotmatched, slen_allnotmatched, sfraglength,sCT_checked,sCpG_checked,sCT_mismatch,sCpG_mismatch,sCT_accepted,sCpG_accepted,sCT_notacceped,sCpG_notacceped=self.getextrainfo()
        ahypolist, alen_hypolist, ahyperlist, alen_hyperlist, aallnotmatched, alen_allnotmatched, afraglength,aCT_checked,aCpG_checked,aCT_mismatch,aCpG_mismatch,aCT_accepted,aCpG_accepted,aCT_notacceped,aCpG_notacceped=aReadobj.getextrainfo()

        hypolist=list(set(shypolist+ahypolist))
        hyperlist=list(set(shyperlist+ahyperlist))

        hyposet=set(hypolist)
        hyperset=set(hyperlist)

        interofhypohyper=list(hyposet.intersection(hyperset))
        leninterofhypohyper=len(interofhypohyper)



        notmatched = list(set(sallnotmatched+aallnotmatched).difference((hyposet.union(hyperset))))


        fragmentlength=1.0*(sfraglength+afraglength)/2



        ##############################
        CT_checked=list(set(sCT_checked+aCT_checked))
        CpG_checked=list(set(sCpG_checked+aCpG_checked))
        CT_mismatch=list(set(sCT_mismatch+aCT_mismatch))
        CpG_mismatch=list(set(sCpG_mismatch+aCpG_mismatch))
        CT_accepted=list(set(sCT_accepted+aCT_accepted))
        CpG_accepted=list(set(sCpG_accepted+aCpG_accepted))
        CT_notacceped=list(set(sCT_notacceped+aCT_notacceped))
        CpG_notacceped=list(set(sCpG_notacceped+aCpG_notacceped))

        ##############################






        return hypolist,len(hypolist),hyperlist,len(hyperlist),notmatched,len(notmatched),fragmentlength,CT_checked,CpG_checked,CT_mismatch,CpG_mismatch,CT_accepted,CpG_accepted,CT_notacceped, CpG_notacceped,  interofhypohyper,leninterofhypohyper
