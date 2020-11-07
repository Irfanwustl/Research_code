import pysam
from collections import defaultdict
import re
import sys
from collections import Counter
import pandas as pd
import aRead
import parseMasterDF


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


        masterdf=pd.DataFrame([[rfromrobjlist.ReadName,rfromrobjlist.allcelltype, rfromrobjlist.ucelltype, rfromrobjlist.assinedcelltype,rfromrobjlist.checkedCpG,rfromrobjlist.mismatchCpG,rfromrobjlist.notacceptedCpG,rfromrobjlist.acceptedCpG,rfromrobjlist.finalacceptedfor,rfromrobjlist.finalrejectedfor,rfromrobjlist.matefound] for rfromrobjlist in self.readObjectList],
                              columns=['ReadName','allcelltype', 'ucelltype', 'assignedcelltype','CheckedCpG','mismatchCpG','notacceptedCpG','acceptedCpG','finalacceptedfor','finalrejectedfor','MateCIGARok'])



        masterdf.to_csv(self.outpath+"_masterdf.txt",sep="\t", index=False)


        


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
            self.singleReadcountpercelltype()
        else:
            print("Somehow wrong mode")
            sys.exit(1)

    def singleReadcountpercelltype(self):
        allreads = self.OpenBamFile.fetch()
        for read in allreads:
            if read.mapping_quality < self.mapping_quality:
                continue
            no_indel_mapping = re.match("^\d+M$", read.cigarstring)
            if no_indel_mapping == None:
                # print("problem cigar, not processing===", read.cigarstring)
                continue

            readresult = self.singleReadcounthelper(read)
            if len(readresult) != 0:
                self.celltypeassigntoread(readresult, read)
            # break

    def singleReadcounthelper(self, read):


        # print(read)
        chr = read.reference_name
        block = read.get_blocks()
        if len(block) != 1:
            print("len(block) !=1")
            print(len(block))
            sys.exit(1)

        start = block[0][0]
        end = block[0][1] + 1

        # print(chr,start,end)

        # print(self.getCorresCpgFromSM(chr,start,end))


        return self.read_SMcpg_associate(self.getCorresCpgFromSM(chr, start, end), read)

        ############start from here########################################################################################################

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

        ###################### lookkkkk very important ###########################################################
        '''
        if smsubset.shape[0]<2:
            print("singleton")
            print(smsubset)
            return []
        '''
        ###################### lookkkkk very important ###########################################################

        if read.query_alignment_start != 0:
            print(
                "...................................read query doe not start at 0.....................................")
            print(read.query_name)
            readobject = aRead.aRead(read.query_name, [], [],
                                     "wrong start", [], [],[],[])
            self.readObjectList.append(readobject)
            return []

        yd = read.get_tag("YD")
        offset = 0
        if yd == "r":
            offset = 1

        #######################################ABS read COUNT#############################################################
        allcellsflatlistforabscount = (smsubset["celltype"]).tolist()
        allcellsflatlistforabscountflat_list = [item for sublist in allcellsflatlistforabscount for item in sublist]
        uniquecelltypes = list(set(allcellsflatlistforabscountflat_list))
        for uncell in uniquecelltypes:
            self.allreadpercelltype[uncell].append(read.query_name)
        ####################################################################################################





        firstrefpos = read.get_reference_positions()[0]

        result = []


        checkedCpG=[]
        notaccepedCpG=[]
        mismatchCpG=[]
        passedCpG=defaultdict(list)

        for index, row in smsubset.iterrows():

            cpg = row['start']

            pos = cpg + offset - firstrefpos  # -1 #####################################################################

            if read.query_alignment_qualities[pos] < self.phred_score:
                continue

            refbase = (read.get_reference_sequence()[pos]).upper()

            readbase = (read.query_sequence[pos]).upper()

            cpgname = row['chrom'] + ":" + str(row['start'])
            if readbase == refbase:
                self.readCpGdict[read.query_name].append("")
                notaccepedCpG.append(cpgname)

            elif (refbase == "C" and readbase == "T") or (refbase == "G" and readbase == "A"):
                result.append(row['celltype'])

                if len(row['celltype'])!=1:
                    print("wont work for crosstalk reference. Exit")
                    sys.exit(1)
                passedCpG[row['celltype'][0]].append(cpgname)

                self.readCpGdict[read.query_name].append(cpgname)
            else:
                self.readCpGdict[read.query_name].append("")
                mismatchCpG.append(cpgname)
                '''
                print("read base ref base mismatch problem==",
                      cpg)  ####this is not a problem chr1:21317473 read: A00118:116:HJ7VFDSXX:3:2518:7690:26553
                print(read.query_name)
                print(refbase)
                print(readbase)
                print(read.query_name)
                '''


            self.readCpGdictAll[read.query_name].append(cpgname)

            checkedCpG.append(cpgname)




        if len(result)==0:
            readobject = aRead.aRead(read.query_name, allcellsflatlistforabscountflat_list, uniquecelltypes,"NotAssigned", checkedCpG,mismatchCpG,notaccepedCpG, [])


        else:
            normalpassedCpG=dict(passedCpG)


            passedCpGOnly,passedCelltypeOnly=self.GetMaxFlow(normalpassedCpG)

            if len(passedCpGOnly) < self.pattern_percentage * smsubset.shape[0]:
                result = []
                readobject = aRead.aRead(read.query_name, allcellsflatlistforabscountflat_list, uniquecelltypes, "NotAssigned",checkedCpG,mismatchCpG,notaccepedCpG, [])
            else:
                readobject = aRead.aRead(read.query_name, allcellsflatlistforabscountflat_list, uniquecelltypes, passedCelltypeOnly,checkedCpG, mismatchCpG,notaccepedCpG,passedCpGOnly)



        self.readObjectList.append(readobject)




        return result


    ### get the highest cell type and corresponding CpG in the flows dict
    def GetMaxFlow(self,flows):
        maks = max(flows, key=lambda k: len(flows[k]))
        return flows[maks], maks

    def ppReadcountperCelltype(self):

        for read1, read2 in self.read_pair_generator(self.OpenBamFile):
            no_indel_mapping1 = re.match("^\d+M$", read1.cigarstring)
            no_indel_mapping2 = re.match("^\d+M$", read2.cigarstring)

            if (no_indel_mapping1==None) and (no_indel_mapping2==None):
                #print("CIGAR prob")
                continue
            elif no_indel_mapping1==None:
                r2result=self.singleReadcounthelper(read2)
                if len(r2result)!=0:
                    self.celltypeassigntoread(r2result,read2)

                #self.singleReadcounthelper(read2)
            elif no_indel_mapping2==None:
                r1result=self.singleReadcounthelper(read1)
                if len(r1result)!=0:
                    self.celltypeassigntoread(r1result,read1)



            else:



                read1result=self.singleReadcounthelper(read1)
                read2result=self.singleReadcounthelper(read2)
                pairedresult=read1result+read2result

                #print(read1result)
                #print(read2result)

                if len(pairedresult)!=0:
                    self.celltypeassigntoread(pairedresult,read1)
                    #break

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
