import pysam
from collections import defaultdict
import re
import sys
from collections import Counter
import pandas as pd
import aRead



class ReadAssign:
    def __init__(self, bamfile, quality_score,phred_score,sm,outpath,**kwargs):
        """

        :param sm: the SM assigned dataframe
        """
        self.howsm='single'
        if 'howsm' in kwargs:
            if kwargs['howsm']=='mhb':
                self.howsm=kwargs['howsm']
            elif kwargs['howsm']!='single':
                print("wrong howsm")
                sys.exit(1)


        self.pattern_percentage = .8
        if 'pattern_percentage' in kwargs:
            self.pattern_percentage=kwargs['pattern_percentage']


        self.mapping_quality = quality_score
        self.phred_score=phred_score
        self.bamfile = bamfile



        sm['celltype'] = sm.celltype.apply(lambda x: x[1:-1].split(','))
        self.sm=sm

        self.OpenBamFile = pysam.AlignmentFile(bamfile, 'rb')

        self.mode="pp"

        if 'mode' in kwargs:
            if kwargs['mode']=='single_read':
                self.mode=kwargs['mode']
            elif kwargs['mode']!='pp':
                print("wrong mode")
                sys.exit(1)

        # Check for presence of index file
        index_present = self.OpenBamFile.check_index()
        if not index_present:
            raise FileNotFoundError("BAM file index is not found. Please create it using samtools index")


        self.rawreadcount=defaultdict(list)

        self.allreadpercelltype=defaultdict(list)


        self.readCpGdict=defaultdict(list)

        self.readCpGdictAll=defaultdict(list)




        self.outpath = outpath + "_howsm_" + self.howsm

        self.outpath = self.outpath+"_mode_"+self.mode



        self.readObjectList=[]

        self.CoreAlgo()



    def CoreAlgo(self):
        self.ReadCountpercelltype()



        normaldict = dict(self.rawreadcount)  ################### should save this

        with open(self.outpath + "_readassigned.txt", 'w') as f:
            print(normaldict, file=f)

        readcpgnormaldict = dict(self.readCpGdict)
        with open(self.outpath + "_readCpG.txt", 'w') as f:
            print(readcpgnormaldict, file=f)

        readAllCpGnormaldict = dict(self.readCpGdictAll)

        with open(self.outpath + "_readALLCpG.txt", 'w') as f:
            print(readAllCpGnormaldict, file=f)

        dictforcount = {}
        for k in normaldict:
            dictforcount[k] = [len(normaldict[k])]



        dfforcount = pd.DataFrame(dictforcount)  ####should save this


        dfforcount.to_csv(self.outpath + "_rawcount.txt", sep="\t", index=False)

        dfnormalized = dfforcount.div(dfforcount.sum(axis=1), axis=0)


        dfnormalized.to_csv(self.outpath + "_rawcountNormalized.txt", sep="\t", index=False)

        ################## ABS read COUNT ##################
        self.processABScount(dfforcount)


        masterdf=pd.DataFrame([[rfromrobjlist.ReadName,rfromrobjlist.allcelltype, rfromrobjlist.ucelltype, rfromrobjlist.assinedcelltype,rfromrobjlist.checkedCpG,rfromrobjlist.mismatchCpG,rfromrobjlist.notacceptedCpG,rfromrobjlist.acceptedCpG,rfromrobjlist.finalacceptedfor,rfromrobjlist.finalrejectedfor,rfromrobjlist.matefound,rfromrobjlist.hypolist, rfromrobjlist.lenhypolist, rfromrobjlist.hyperlist, rfromrobjlist.lenhyperlist, rfromrobjlist.allnotmatched, rfromrobjlist.lenallnotmatched, rfromrobjlist.fraglength,rfromrobjlist.CT_checked, rfromrobjlist.CT_checked_length,rfromrobjlist.CpG_checked, rfromrobjlist.CpG_checked_length,rfromrobjlist.CT_mismatch,rfromrobjlist.CT_mismatch_length,rfromrobjlist.CpG_mismatch,rfromrobjlist.CpG_mismatch_length, rfromrobjlist.CT_accepted,rfromrobjlist.CT_accepted_length,rfromrobjlist.CpG_accepted,rfromrobjlist.CpG_accepted_length, rfromrobjlist.CT_notacceped,rfromrobjlist.CT_notacceped_length,rfromrobjlist.CpG_notacceped,rfromrobjlist.CpG_notacceped_length,rfromrobjlist.interofhypohyper,rfromrobjlist.leninterofhypohyper] for rfromrobjlist in self.readObjectList],
                              columns=['ReadName','allcelltype', 'ucelltype', 'assignedcelltype','CheckedCpG','mismatchCpG','notacceptedCpG','acceptedCpG','finalacceptedfor','finalrejectedfor','MateCIGARok','hypolist', 'len_hypolist', 'hyperlist', 'len_hyperlist', 'allnotmatched', 'len_allnotmatched', 'fraglength','smCT_checkedunique', 'smCT_checked_lengthunique','smCpG_checked', 'smCpG_checked_length','smCT_mismatchunique','smCT_mismatch_lengthunique','smCpG_mismatch','smCpG_mismatch_length', 'smCT_acceptedunique','smCT_accepted_lengthunique','smCpG_accepted','smCpG_accepted_length', 'smCT_notaccepedunique','smCT_notacceped_lengthuniqe','smCpG_notacceped','smCpG_notacceped_length','intersection_ofhypohyper','len_intersection_ofhypohyper'])

        masterdf=self.parseMasterDF(masterdf)

        
        onlymeasurableFragments=masterdf[~masterdf['assignedcelltype'].isin(["lowmapq","DupRead"])]

        

        ctbasedinfo=self.weightedFragment_Result(onlymeasurableFragments)

      

        masterdf.to_csv(self.outpath+"_masterdf.txt",sep="\t", index=False)


    
    





    #110421
    def parseMasterDF(self,mdf): 

        mdf['efficientFinalAcceptedFor']='notdetermined'
        mdf['efficientFinalRejectedFor']='notdetermined'

     

        mdf.loc[(mdf['smCpG_accepted_length']>=self.pattern_percentage*(mdf['smCpG_notacceped_length']+mdf['smCpG_accepted_length'])) & (mdf['smCpG_notacceped_length']+mdf['smCpG_accepted_length']>0),'efficientFinalAcceptedFor']= mdf.loc[(mdf['smCpG_accepted_length']>=self.pattern_percentage*(mdf['smCpG_notacceped_length']+mdf['smCpG_accepted_length'])) & (mdf['smCpG_notacceped_length']+mdf['smCpG_accepted_length']>0),'smCT_acceptedunique']
        mdf.loc[(mdf['smCpG_accepted_length']<self.pattern_percentage*(mdf['smCpG_notacceped_length']+mdf['smCpG_accepted_length'])) & (mdf['smCpG_notacceped_length']+mdf['smCpG_accepted_length']>0),'efficientFinalRejectedFor']= mdf.loc[(mdf['smCpG_accepted_length']<self.pattern_percentage*(mdf['smCpG_notacceped_length']+mdf['smCpG_accepted_length'])) & (mdf['smCpG_notacceped_length']+mdf['smCpG_accepted_length']>0),'smCT_notaccepedunique']

        
        mdf=mdf.explode('efficientFinalAcceptedFor')

        mdf=mdf.explode('efficientFinalRejectedFor')



        mdf['efficientFinalAcceptedForNoCrossTalk']=mdf['efficientFinalAcceptedFor'].copy()
        mdf['efficientFinalRejectedForNoCrossTalk']=mdf['efficientFinalRejectedFor'].copy()


        mdf.loc[mdf['smCT_accepted_lengthunique']>1,'efficientFinalAcceptedForNoCrossTalk']='crosstalk'
        mdf.loc[mdf['smCT_notacceped_lengthuniqe']>1,'efficientFinalRejectedForNoCrossTalk']='crosstalk'

        




        return mdf


    #110421
    def weightedFragment_Result(self,mdf):
        allct=list(set(mdf['efficientFinalAcceptedForNoCrossTalk'].tolist()+mdf['efficientFinalRejectedForNoCrossTalk'].tolist()))

        try:
            allct.remove('notdetermined')
        except ValueError:
            pass  # do nothing!
        


        weightedFragmentResultdict=defaultdict(list)

        weightedAVGdict=defaultdict(list)

        storectBasedinfolist=[]

        for ct in allct:
            ctaccdf=mdf[mdf['efficientFinalAcceptedForNoCrossTalk']==ct]
            ctaccINFO=ctaccdf.groupby(['smCpG_accepted_length']).size() ###########################

            ctaccINFO=ctaccINFO.to_frame('totalaccfragment').reset_index()



            ctrejdf=mdf[mdf['efficientFinalRejectedForNoCrossTalk']==ct]
            ctrejINFO=ctrejdf.groupby(['smCpG_notacceped_length']).size()

            ctrejINFO=ctrejINFO.to_frame('totalrejfragment').reset_index()


            ctbasedINFO=ctaccINFO.merge(ctrejINFO,left_on='smCpG_accepted_length',right_on='smCpG_notacceped_length',how='outer')

            ctbasedINFO['weightedTotalaccFragment']=ctbasedINFO['smCpG_accepted_length']*ctbasedINFO['totalaccfragment']
            ctbasedINFO['weightedTotalrejFragment']=ctbasedINFO['smCpG_accepted_length']*ctbasedINFO['totalrejfragment']
            ctbasedINFO['celltype']=ct

            storectBasedinfolist.append(ctbasedINFO)

            weightedFragmentResultdict[ct].append(ctbasedINFO['weightedTotalaccFragment'].sum()/(ctbasedINFO['weightedTotalaccFragment'].sum()+ctbasedINFO['weightedTotalrejFragment'].sum()))

            
            
            #########################
            weightedAVGdict[ct].append(self.weightedcellproportion_Result(ctaccINFO,ctrejINFO))




        weightedFragmentResultDF=pd.DataFrame(weightedFragmentResultdict)

        storectBasedinfoDF=pd.concat(storectBasedinfolist)

        mincpg=min(storectBasedinfoDF['smCpG_accepted_length'].tolist()+storectBasedinfoDF['smCpG_notacceped_length'].tolist())

        weightedFragmentResultDF.to_csv(self.outpath + "_weightedFragmentResult_mincpg"+str(int(mincpg))+".txt", sep="\t", index=False)

        weightedAVGdf=pd.DataFrame(weightedAVGdict)

        weightedAVGdf.to_csv(self.outpath + "_weightedCellProportion_mincpg"+str(int(mincpg))+".txt", sep="\t", index=False)


        storectBasedinfoDF.to_csv(self.outpath + "_fragCpGinfo.txt", sep="\t", index=False,na_rep='NA')

        return storectBasedinfoDF



    #110421
    def weightedcellproportion_Result(self,onectaccINFO,onectrejINFO):
        allcpglength=list(set(onectaccINFO['smCpG_accepted_length'].tolist()+onectrejINFO['smCpG_notacceped_length'].tolist()))

       

        runningresult=0
        for cpglength in allcpglength:
            tmpaccdf=onectaccINFO[onectaccINFO['smCpG_accepted_length']>=cpglength] 
            tmprejdf=onectrejINFO[onectrejINFO['smCpG_notacceped_length']>=cpglength]

            tmpresult=onectaccINFO['totalaccfragment'].sum()/(onectaccINFO['totalaccfragment'].sum()+onectrejINFO['totalrejfragment'].sum())
            tmpresult=cpglength*tmpresult
            runningresult=runningresult+tmpresult


        weightedavg=runningresult/sum(allcpglength)

        return weightedavg
            


          
             









    def processABScount(self,dfforcount):
        normalABSdict=dict(self.allreadpercelltype)

        normalABSdictuniqread={}
        normalABSdictuniqreadCount={}
        for k in normalABSdict:
            normalABSdictuniqread[k]=list(set(normalABSdict[k]))
            normalABSdictuniqreadCount[k]=[len(list(set(normalABSdict[k])))]

        with open(self.outpath+"_ABSread.txt", 'w') as f:
            print(normalABSdictuniqread, file=f)



        normalABSdictuniqreadCountDF=pd.DataFrame(normalABSdictuniqreadCount)

        normalABSdictuniqreadCountDF.to_csv(self.outpath+"_ABSreadcount.txt",sep="\t",index=False)

        divisoned=dfforcount/normalABSdictuniqreadCountDF
        divisoned.to_csv(self.outpath+"_ABSreadcount_divisioned.txt",sep="\t",index=False)

        normalABSdictuniqreadCountDFNormalized=divisoned.div(divisoned.sum(axis=1), axis=0)

        normalABSdictuniqreadCountDFNormalized.to_csv(self.outpath+"_ABSreadcount_divisionedNormalized.txt",sep="\t",index=False)


    def ReadCountpercelltype(self):
        if self.mode == "pp":
            self.ppReadcountperCelltype()
        elif self.mode == "single_read":
            #self.singleReadcountpercelltype()
            print("not implemented")
            sys.exit(1)
        else:
            print("Somehow wrong mode")
            sys.exit(1)




    def ppReadcountperCelltype(self):

        for read1, read2 in self.read_pair_generator(self.OpenBamFile):
            read1result = self.singleReadcounthelper(read1)
            read2result = self.singleReadcounthelper(read2)
            pairedresult = read1result + read2result

            # print(read1result)
            # print(read2result)

            if len(pairedresult) != 0:
                self.celltypeassigntoread(pairedresult, read1)
                # break

            #################################store into the read object##############################

            robj1 = self.readObjectList[-2]
            robj2 = self.readObjectList[-1]

            self.readObjectList.pop(-1)

            self.readObjectList.pop(-1)

            fragobject = robj1.mergewithmate(robj2)

            self.readObjectList.append(fragobject)

            #################################store into the read object##############################




    #output of read_SMcpg_associate
    def celltypeassigntoread(self,readCpgAss,read):


        flat_list = [item for sublist in readCpgAss for item in sublist]

        cellwisecount=Counter(flat_list)


        firsttwo=cellwisecount.most_common(2)
        if len(firsttwo)==1:


            self.rawreadcount[firsttwo[0][0]].append(read.query_name)

    def read_pair_generator(self, bam, region_string=None):
        """
        Generate read pairs in a BAM file or within a region string.
        Reads are added to read_dict until a pair is found.
        """
        read_dict = defaultdict(lambda: [None, None])
        for read in bam.fetch(region=region_string):
            if not read.is_proper_pair or read.is_secondary or read.is_supplementary:
                continue
            qname = read.query_name
            if qname not in read_dict:
                if read.is_read1:
                    read_dict[qname][0] = read
                else:
                    read_dict[qname][1] = read
            else:
                if read.is_read1:
                    yield read, read_dict[qname][1]
                else:
                    yield read_dict[qname][0], read
                del read_dict[qname]




    ### get the highest cell type and corresponding CpG in the flows dict
    def GetMaxFlow(self,flows):
        maks = max(flows, key=lambda k: len(flows[k]))
        return flows[maks], maks



    ##################################### CIGAR prob fixed ########################################

    def singleReadcounthelper(self, read):

        # print(read)
        chr = read.reference_name
        block = read.get_blocks()



        start = block[0][0]
        end = block[len(block)-1][1] + 1

        #print(block)

        #print(chr,start,end)

        # print(self.getCorresCpgFromSM(chr,start,end))

        return self.read_SMcpg_associate(self.getCorresCpgFromSM(chr, start, end), read)

    def getCorresCpgFromSM(self, blockchr, blockstart, blockend):

        outdf = self.sm[(self.sm['chrom'] == blockchr) & (self.sm['start'] >= blockstart) & (self.sm['end'] < blockend)]
        return outdf

    def read_SMcpg_associate(self, smsubset, read):







        if read.mapping_quality < self.mapping_quality:
            readobject = aRead.aRead(read.query_name, [], [],
                                     "lowmapq", [], [],[],[])
            self.readObjectList.append(readobject)
            return []

        if read.is_duplicate == True:
            readobject = aRead.aRead(read.query_name, [], [],
                                     "DupRead", [], [],[],[])
            self.readObjectList.append(readobject)
            return []



        #######################################ABS read COUNT#############################################################
        allcellsflatlistforabscount = (smsubset["celltype"]).tolist()
        allcellsflatlistforabscountflat_list = [item for sublist in allcellsflatlistforabscount for item in sublist]
        uniquecelltypes = list(set(allcellsflatlistforabscountflat_list))
        for uncell in uniquecelltypes:
            self.allreadpercelltype[uncell].append(read.query_name)
        ####################################################################################################

        
        offset = 0

        if read.has_tag('YD'):
            yd = read.get_tag("YD")
            if yd == "r":
                offset = 1

        elif read.has_tag('XB'):
            xb=read.get_tag("XB")

            if xb=='G':
                offset=1
            elif xb=='C':
                pass
            else:
                print("unknown xb value. Exiting....")
                print(read.query_name)

                sys.exit(1)

        else:
            print("no tag found. Exiting")
            print(read.query_name)
            sys.exit(1)


        result = []
        checkedCpG=defaultdict(list) ####11_4_21
        notaccepedCpG=defaultdict(list)  ####11_4_21
        accCpGforsanity=[] ######JUST FOR SANITY
        mismatchCpG=defaultdict(list)  ####11_4_21
        passedCpG=defaultdict(list)

        alignedpairs=read.get_aligned_pairs(with_seq=True)
        #alignedpairs=read.get_aligned_pairs()


        #########################################
        for index, row in smsubset.iterrows():

            cpg = row['start']

            pos = cpg + offset

            self.CpGsanityCheck(cpg,read)

            qpos, refbase = self.getqposAndRefbase(alignedpairs, pos)

            if  qpos==None or refbase == None:
                continue




            if read.query_qualities[qpos] < self.phred_score:


                continue






            refbase=refbase.upper()

            '''
            if refbase != "C" and refbase != "G":
                print("Wrong Refbase. Exiting")
                print(read.query_name)
                print(pos,refbase)
                sys.exit(1)
            '''




            readbase = (read.query_sequence[qpos]).upper()

            cpgname = row['chrom'] + ":" + str(row['start'])


            rowcols=row.keys().tolist()




            if ('direction' in rowcols) and (row['direction'] == 'C'):
                

                if readbase == refbase:
                    result.append(row['celltype'])

                    accCpGforsanity.append(cpgname)

                    if len(row['celltype']) != 1:
                        print("wont work for crosstalk reference. Exit")
                        sys.exit(1)

                    passedCpG[row['celltype'][0]].append(cpgname)

                    self.readCpGdict[read.query_name].append(cpgname)

                elif (refbase == "C" and readbase == "T") or (refbase == "G" and readbase == "A"):
                    self.readCpGdict[read.query_name].append("")
                    notaccepedCpG[row['celltype'][0]].append(cpgname)
                else:
                    self.readCpGdict[read.query_name].append("")
                    mismatchCpG[row['celltype'][0]].append(cpgname)


            else:
                if readbase == refbase:
                    self.readCpGdict[read.query_name].append("")
                    notaccepedCpG[row['celltype'][0]].append(cpgname)

                elif (refbase == "C" and readbase == "T") or (refbase == "G" and readbase == "A"):
                    result.append(row['celltype'])

                    accCpGforsanity.append(cpgname)

                    if len(row['celltype']) != 1:
                        print("wont work for crosstalk reference. Exit")
                        sys.exit(1)

                    passedCpG[row['celltype'][0]].append(cpgname)

                    self.readCpGdict[read.query_name].append(cpgname)
                else:
                    self.readCpGdict[read.query_name].append("")
                    mismatchCpG[row['celltype'][0]].append(cpgname)


            self.readCpGdictAll[read.query_name].append(cpgname)

            checkedCpG[row['celltype'][0]].append(cpgname)







        #########################################
        CT_checked,CpG_checked=self.seperate_ct_and_cpg(checkedCpG)
        CT_mismatch,CpG_mismatch=self.seperate_ct_and_cpg(mismatchCpG)
        CT_accepted,CpG_accepted=self.seperate_ct_and_cpg(passedCpG)
        CT_notacceped,CpG_notacceped=self.seperate_ct_and_cpg(notaccepedCpG)


        if len(CpG_checked)!=len(CpG_accepted)+len(CpG_mismatch)+len(CpG_notacceped):
            print("len mismatch of diiferent CpG. Exiting")
            sys.exit(1)

        if len(CT_checked)!=len(CT_accepted)+len(CT_mismatch)+len(CT_notacceped):
            print("len mismatch of diiferent CT. Exiting")
            sys.exit(1)


        if len(result)!=len(accCpGforsanity):
            print("result len and accCpG len mismatch. Exiting")
            sys.exit(1)




        

        if len(result)==0:
            readobject = aRead.aRead(read.query_name, allcellsflatlistforabscountflat_list, uniquecelltypes,"NotAssigned", CpG_checked,CpG_mismatch,CpG_notacceped, [])


        else:
            normalpassedCpG=dict(passedCpG)


            passedCpGOnly,passedCelltypeOnly=self.GetMaxFlow(normalpassedCpG)

            if len(passedCpGOnly) < self.pattern_percentage * len(checkedCpG):
                result = []
                readobject = aRead.aRead(read.query_name, allcellsflatlistforabscountflat_list, uniquecelltypes, "NotAssigned",CpG_checked,CpG_mismatch,CpG_notacceped, [])
            else:
                readobject = aRead.aRead(read.query_name, allcellsflatlistforabscountflat_list, uniquecelltypes, passedCelltypeOnly,CpG_checked,CpG_mismatch,CpG_notacceped,passedCpGOnly)







        hypolist, len_hypolist, hyperlist, len_hyperlist, allnotmatched, len_allnotmatched, fraglength=self.collectextrainfo(read,offset)
        readobject.setextrainfo(hypolist, len_hypolist, hyperlist, len_hyperlist, allnotmatched, len_allnotmatched, fraglength,  CT_checked,CpG_checked,CT_mismatch,CpG_mismatch,CT_accepted,CpG_accepted,CT_notacceped,CpG_notacceped)

        self.readObjectList.append(readobject)



        return result




    def seperate_ct_and_cpg(self,cpgctdict):
        cpgctdict=dict(cpgctdict)
        ctlist=[]
        cpglist=[]
        for key, value in cpgctdict.items():
            ctlist=ctlist+[key]*len(value)
            cpglist=cpglist+value

        return ctlist,cpglist


    def getqposAndRefbase(self,listoftuples,refpos):
        for t in listoftuples:
            if refpos==t[1]:
                return t[0],t[2]

        print("some wrong in getqposAndRefbase")
        sys.exit(1)


    ## check whether I get C followed by G #####
    def CpGsanityCheck(self,cpg,read):
        firstrefpos = read.get_reference_positions()[0]
        Cpos=cpg-firstrefpos
        refCbase = (read.get_reference_sequence()[Cpos]).upper()
        refGbase= (read.get_reference_sequence()[Cpos+1]).upper()

        #if refCbase!="C" or refGbase!="G":
            #print("wrong in CpGsanityCheck. But not Exiting  cause may be prob in the SM position")
            #print(read.query_name,refCbase,refGbase,Cpos,cpg)
            #sys.exit(1)






    def getCGindex(self,read):
        alignedpairs = read.get_aligned_pairs(with_seq=True)
        outuplelist=[]
        alignedpairslen=len(alignedpairs)
        for i in range (alignedpairslen):
            if i!=alignedpairslen-1:

                if (None not in alignedpairs[i]) and (None not in alignedpairs[i+1]):

                    tempbase=(alignedpairs[i][2]).upper()
                    tempnextbase=(alignedpairs[i+1][2]).upper()

                    if tempbase=='C' and tempnextbase=='G':
                        outuplelist.append(alignedpairs[i])

        return outuplelist




    def collectextrainfo(self, read,offset):


        corressreadinfo=self.getCGindex(read)


        hypolist, hyperlist, notmatched=self.parsealignedpaires(read,corressreadinfo,offset)



        fraglength = abs(read.template_length)


        return hypolist,len(hypolist),hyperlist,len(hyperlist),notmatched,len(notmatched),fraglength



    def parsealignedpaires(self,read,corressreadinfo,offset):   ######################################## supply offset###################



        chrname=read.reference_name
        corresreadindex = [x[0] for x in corressreadinfo]

        corresbaspos = [x[1] for x in corressreadinfo]

        corresreadindex=[x + offset for x in corresreadindex]
        if offset==0:
            hyporef="T"
            hyperref="C"
        elif offset==1:
            hyporef="A"
            hyperref="G"



        readbases=(read.query_sequence).upper()


        hypolist=[]
        hyperlist=[]
        notmatched=[]

        j=0
        for i in corresreadindex:


            currentbase=readbases[i]

            if read.query_qualities[i] >= self.phred_score:

                cpgname=chrname+":"+str(corresbaspos[j])########### need to check offset effect



                if currentbase == hyporef:
                    hypolist.append(cpgname)

                elif currentbase == hyperref:
                    hyperlist.append(cpgname)

                else:
                    notmatched.append(cpgname)

            j=j+1



        return hypolist,hyperlist,notmatched






















