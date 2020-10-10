import pysam
from collections import defaultdict
import re
import sys
from collections import Counter
import pandas as pd



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


        self.pattern_percentage = .8  ###### for monod2mhb. self.pattern_percentage (e.g. 80%) of a read should be of this pattern to call it pattern specific
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
        self.readCpGdict=defaultdict(list)

        self.readCpGdictAll=defaultdict(list)






        '''
        for read1, read2 in self.read_pair_generator(self.OpenBamFile):
            print(read1)
            print(read2)
            break
        '''



        self.outpath = outpath + "_howsm_" + self.howsm

        self.outpath = self.outpath+"_mode_"+self.mode


        self.CoreAlgo()




    def CoreAlgo(self):
        self.ReadCountpercelltype()

        print("rawresult")
        print(self.rawreadcount)

        normaldict=dict(self.rawreadcount) ################### should save this

        with open(self.outpath+"_readassigned.txt", 'w') as f:
            print(normaldict, file=f)


        readcpgnormaldict=dict(self.readCpGdict)
        with open(self.outpath+"_readCpG.txt", 'w') as f:
            print(readcpgnormaldict, file=f)


        readAllCpGnormaldict=dict(self.readCpGdictAll)

        with open(self.outpath+"_readALLCpG.txt", 'w') as f:
            print(readAllCpGnormaldict, file=f)

        dictforcount={}
        for k in normaldict:
            dictforcount[k]=[len(normaldict[k])]

        print(dictforcount)


        dfforcount=pd.DataFrame(dictforcount)  ####should save this

        print(dfforcount)
        dfforcount.to_csv(self.outpath+"_rawcount.txt",sep="\t",index=False)


        dfnormalized=dfforcount.div(dfforcount.sum(axis=1), axis=0)
        print(dfnormalized)

        dfnormalized.to_csv(self.outpath + "_rawcountNormalized.txt", sep="\t", index=False)




    def ReadCountpercelltype(self):
        if self.mode=="pp":
            self.ppReadcountperCelltype()
        elif self.mode=="single_read":
            self.singleReadcountpercelltype()
        else:
            print("Somehow wrong mode")
            sys.exit(1)

    def singleReadcountpercelltype(self):
        allreads=self.OpenBamFile.fetch()
        for read in allreads:
            no_indel_mapping = re.match("^\d+M$", read.cigarstring)
            if no_indel_mapping == None:
                #print("problem cigar, not processing===", read.cigarstring)
                continue

            readresult = self.singleReadcounthelper(read)
            if len(readresult) != 0:
                self.celltypeassigntoread(readresult, read)
            #break


    def singleReadcounthelper(self,read):
        if read.mapping_quality < self.mapping_quality:
            return []

        #print(read)
        chr=read.reference_name
        block=read.get_blocks()
        if len(block)!=1:
            print("len(block) !=1")
            print(len(block))
            sys.exit(1)


        start=block[0][0]
        end=block[0][1]+1


        #print(chr,start,end)

        #print(self.getCorresCpgFromSM(chr,start,end))


        if self.howsm=='mhb':

            return self.MHBperRead_SMcpg_associate(self.getCorresCpgFromSM(chr, start, end), read)

        else:
            return self.read_SMcpg_associate(self.getCorresCpgFromSM(chr, start, end), read)


        ############start from here########################################################################################################

    def getCorresCpgFromSM(self,blockchr,blockstart,blockend):

        outdf=self.sm[(self.sm['chrom']==blockchr) & (self.sm['start'] >=blockstart) & (self.sm['end']<blockend)]
        return outdf








    def read_SMcpg_associate(self, smsubset, read):



        if smsubset.shape[0]<2:
            print("singleton")
            print(smsubset)
            return []

        if read.query_alignment_start != 0:
            print("...................................read query doe not start at 0.....................................")
            print(read.query_name)
            return []
        yd = read.get_tag("YD")
        offset = 0
        if yd == "r":
            offset = 1

        firstrefpos = read.get_reference_positions()[0]

        result = []
        for index, row in smsubset.iterrows():

            cpg=row['start']

            pos = cpg + offset - firstrefpos#-1 #####################################################################



            if read.query_alignment_qualities[pos] < self.phred_score:
                continue

            refbase = (read.get_reference_sequence()[pos]).upper()

            readbase = (read.query_sequence[pos]).upper()

            cpgname = row['chrom'] + ":" + str(row['start'])
            if readbase == refbase:
                self.readCpGdict[read.query_name].append("")
                pass
            elif (refbase == "C" and readbase == "T") or (refbase == "G" and readbase == "A"):
                result.append(row['celltype'])


                self.readCpGdict[read.query_name].append(cpgname)
            else:
                self.readCpGdict[read.query_name].append("")
                print("read base ref base mismatch problem==",cpg)  ####this is not a problem chr1:21317473 read: A00118:116:HJ7VFDSXX:3:2518:7690:26553
                print(read.query_name)
                print(refbase)
                print(readbase)
                print(read.query_name)
                # sys.exit(1)

            self.readCpGdictAll[read.query_name].append(cpgname)



        #read_meth_dict = {read.query_name: result}

        return result

    def singlemhbperread(self, read, mhbdfrow):
        allcpgpos = self.allCpGintheread(read)

        result = []
        for cpgpos in allcpgpos:
            if cpgpos >= mhbdfrow['start'] and cpgpos <= mhbdfrow["end"]:
                result.append(cpgpos)

        return result

    def allCpGintheread(self, read):
        refseq = (read.get_reference_sequence()).upper()
        cpgCpos = [m.start() for m in re.finditer('CG', refseq)]

        firstrefpos = read.get_reference_positions()[0]

        result = [x + firstrefpos for x in cpgCpos]

        # print(result)
        return result

    def MHBperRead_SMcpg_associate(self, smsubset, read):
        print("...................mhbmode..................")

        if read.query_alignment_start != 0:
            print("...................................read query doe not start at 0.....................................")
            print(read.query_name)
            return []

        yd = read.get_tag("YD")
        offset = 0
        if yd == "r":
            offset = 1

        firstrefpos = read.get_reference_positions()[0]

        finalresult = []
        for index, row in smsubset.iterrows():

            corresCpG=self.singlemhbperread(read,row)

            result = []
            for cpg in corresCpG:
                pos = cpg + offset - firstrefpos

                if read.query_alignment_qualities[pos] < self.phred_score:
                    continue

                refbase = (read.get_reference_sequence()[pos]).upper()

                readbase = (read.query_sequence[pos]).upper()

                if readbase == refbase:
                    result.append('C')
                elif (refbase == "C" and readbase == "T") or (refbase == "G" and readbase == "A"):
                    result.append('T')
                else:



                    print("read base ref base mismatch problem==",cpg)  ####this is not a problem chr1:21317473 read: A00118:116:HJ7VFDSXX:3:2518:7690:26553
                    print(read.query_name)
                    print(refbase)
                    print(readbase)
                    print(read.query_name)
                    # sys.exit(1)

            T_count = result.count("T")

            if T_count >= (len(result) * self.pattern_percentage):
                finalresult.append(row['celltype'])





        return finalresult





    def ppReadcountperCelltype(self):

        for read1, read2 in self.read_pair_generator(self.OpenBamFile):
            no_indel_mapping1 = re.match("^\d+M$", read1.cigarstring)
            no_indel_mapping2 = re.match("^\d+M$", read2.cigarstring)

            if (no_indel_mapping1==None) and (no_indel_mapping2==None):
                print("CIGAR prob")
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



    #output of read_SMcpg_associate
    def celltypeassigntoread(self,readCpgAss,read):

        #print("in .....celltypeassigntoread..... ")
        #print(readCpgAss)
        flat_list = [item for sublist in readCpgAss for item in sublist]
        #print(flat_list)

        cellwisecount=Counter(flat_list)


        firsttwo=cellwisecount.most_common(2)
        if len(firsttwo)==1:
            #print("mostcommon")

            self.rawreadcount[firsttwo[0][0]].append(read.query_name)
            #self.rawreadcount.append({firsttwo[0][0]:read.query_name})








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
