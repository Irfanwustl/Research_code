import pysam
import re
import sys


class BamParser:
    def __init__(self, bamfile, quality_score,phred_score):
        """
        Class used to read WGBSeq reads from a BAM file, extract methylation, and convert into data frame
        :param bamfile: Path to sorted bam file location
        :param quality_score: Only include reads >= this fastq quality
        :phred_score:phred_score
        :param MHB: the SM MHB dataframe
        """

        self.mapping_quality = quality_score
        self.phred_score=phred_score
        self.bamfile = bamfile

        self.OpenBamFile = pysam.AlignmentFile(bamfile, 'rb')

        # Check for presence of index file
        index_present = self.OpenBamFile.check_index()
        if not index_present:
            raise FileNotFoundError("BAM file index is not found. Please create it using samtools index")

    # Get reads from the bam file
    def get_reads(self, chromosome: str, start: int, stop: int):
        """
        :param chromosome: chromosome as "chr6"
        :param start: start coordinate
        :param stop: end coordinate
        :return: List of reads and their positional tags as assigned by bismark
        """

        reads = []
        for read in self.OpenBamFile.fetch(chromosome, start, stop):
            if read.mapping_quality >= self.mapping_quality:
                if read.is_duplicate == False:
                    reads.append(read)

        return reads

    def get_metinfoallreads(self, readlist, flag,**kwargs):
        result=[]
        for read in readlist:

            if flag==0:
                corresCpG=self.generate_corressCpG(read,flag)
            elif flag==1:
                corresCpG = self.generate_corressCpG(read, flag,**kwargs)

            temp=self.get_metinfo(read, corresCpG)
            if len(temp[read.query_name])>0:
                result.append(temp)
            #result.update(temp)
        return result



    def get_metinfo(self, read, corresCpG):
        """
        :param read: a single read
        :param corresCpG: list of CpG 0 based C pos without chr to check in this read. only mhb per read or all cpg in the read should be determined before calling this function
        :return: list of C(meth) and T(unmeth)
        """

        #print(read.query_name)
        #print(read.cigarstring)
        # if CIGER has anything but M return
        no_indel_mapping = re.match("^\d+M$", read.cigarstring)
        if no_indel_mapping == None:
            print("problem cigar, not processing===",read.cigarstring)
            return {read.query_name:[-1]}

        if read.query_alignment_start != 0:
            print(
                "...................................read query doe not start at 0.....................................")
            print(read.query_name)

        yd = read.get_tag("YD")
        offset = 0
        if yd == "r":
            offset = 1

        firstrefpos = read.get_reference_positions()[0]

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

                print("read base ref base mismatch problem==",cpg) ####this is not a problem chr1:21317473 read: A00118:116:HJ7VFDSXX:3:2518:7690:26553
                print(read.query_name)
                print(refbase)
                print(readbase)
                print(read.query_name)
                #sys.exit(1)

                pass
        read_meth_dict = {read.query_name:result}
        return read_meth_dict



    def singlemhbperread(self,read,mhbdfrow):
        allcpgpos=self.allCpGintheread(read)

        result=[]
        for cpgpos in allcpgpos:
            if cpgpos >=mhbdfrow['start'] and cpgpos<=mhbdfrow["end"]:
                result.append(cpgpos)

        return result



    def allCpGintheread(self,read):
        refseq=(read.get_reference_sequence()).upper()
        cpgCpos=[m.start() for m in re.finditer('CG', refseq)]



        firstrefpos = read.get_reference_positions()[0]

        result = [x + firstrefpos for x in cpgCpos]

        #print(result)
        return result
    def generate_corressCpG(self,read,flag,**kwargs):
        if flag==0:
            return self.allCpGintheread(read)

        elif flag==1:
            mhbdfrow= kwargs['mhbdfrow']
            return self.singlemhbperread(read,mhbdfrow)


