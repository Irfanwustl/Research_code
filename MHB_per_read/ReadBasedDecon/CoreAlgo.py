import BamParser
import pandas as pd
import sys
import CountingDecon

class CoreAlgo:
    def __init__(self, bamfile, quality_score,phred_score, SMbg,outfilename,mode):
        """

       :param bamfile: Path to sorted bam file location
       :param quality_score: Only include reads >= this fastq quality
       :param SMbg: the SM_MHB bg file
       """
        self.bamfile=bamfile
        self.quality_score=quality_score
        self.phred_score=phred_score
        self.SMbg=self.parseSMbg(SMbg)
        self.outfilname=outfilename
        self.mode=mode
        self.pattern_percentage=.8 ###### self.pattern_percentage (e.g. 80%) of a read should be of this pattern to call it pattern specific

        self.runCore()






    def parseSMbg(self,SMbg):
        df=pd.read_csv(SMbg, sep="\t")
        #df=df.rename(columns={0: "chrom", 1: "start", 2: "end"})
        return df

    def runCore(self):
        bp = BamParser.BamParser(self.bamfile, self.quality_score,self.phred_score)
        result=[]
        for index,r in self.SMbg.iterrows():
            #print(r)


            alignedsegmentlist=bp.get_reads(r["chrom"],r["start"],r["end"])


            temp=bp.get_metinfoallreads(alignedsegmentlist,self.mode,mhbdfrow=r)
            mhbkey=r["chrom"]+":"+str(r["start"])+"-"+str(r["end"])
            #print(mhbkey)
            result.append({"mhb": mhbkey,"celltype":r["celltype"],"info":temp})

            #print(temp)



            #break
        #print(result)

        resultdf=pd.DataFrame(result)
        resultdf.to_csv(self.outfilname,sep="\t",index=False)

        decondf=self.preparefordecon(resultdf)
        decondf.to_csv(self.outfilname+"_fordecon.txt", sep="\t", index=False)

        decon=CountingDecon.CountingDecon(decondf,self.outfilname)



    def howmanyreadpermhhb(self,onemhb):
        ### will return only the count of processed reads (excluding -1)
        #print(len(onemhb["info"]))
        count=0
        filteredread=[]
        filteredlist=[]
        for elem in onemhb["info"]:
            for key in elem:
                if elem[key][0]!=-1:
                    count=count+1
                    filteredread.append(key)
                    filteredlist.append(elem[key])

        if len(filteredread)!=len(filteredlist):
            print("error in howmanyreadpermhhb")
            sys.exit(1)
        return filteredread,filteredlist

    def howmanyreadpermhhb_matchesMHBpattern(self,filteredread,filteredlist,direction):
        supportedread=[]
        supportedpattern=[]
        notsupportedread=[]
        notsupportedpattern=[]
        for ind in range(len(filteredlist)):
            T_count=filteredlist[ind].count("T")
            C_count=filteredlist[ind].count("C")

            if direction=="T":
                if T_count>=(len(filteredlist[ind])*self.pattern_percentage):
                    supportedread.append(filteredread[ind])
                    supportedpattern.append(filteredlist[ind])
                else:
                    notsupportedread.append(filteredread[ind])
                    notsupportedpattern.append(filteredlist[ind])
            if direction=="C":
                if C_count>=(len(filteredlist[ind])*self.pattern_percentage):
                    supportedread.append(filteredread[ind])
                    supportedpattern.append(filteredlist[ind])
                else:
                    notsupportedread.append(filteredread[ind])
                    notsupportedpattern.append(filteredlist[ind])

        return supportedread,supportedpattern,notsupportedread,notsupportedpattern
    def preparefordecon(self,allinfo):
        deconlist=[]
        for index,r in allinfo.iterrows():
            filteredread, filteredlist=self.howmanyreadpermhhb(r)
            direction="T" ##########################################################################
            supportedread, supportedpattern, notsupportedread, notsupportedpattern=self.howmanyreadpermhhb_matchesMHBpattern(filteredread,filteredlist,direction)

            filteredread_count=len(filteredread)
            supportedread_count=len(supportedread)
            notsupportedread_count=len(notsupportedread)

            if filteredread_count !=supportedread_count+notsupportedread_count or len(supportedpattern)!=supportedread_count or len(notsupportedpattern)!=notsupportedread_count:
                print("error in preparefordecon")
                sys.exit(1)

            #print(supportedread, supportedpattern, notsupportedread, notsupportedpattern)

            templist=[["filtered_read",filteredread],["filtered_read_pattern",filteredlist],["filtered_read_count",filteredread_count],["supported_read",supportedread],["supported_read_pattern",supportedpattern],["supported_read_count",supportedread_count],["notsupported_read",notsupportedread],["notsupported_read_pattern",notsupportedpattern],["notsupported_read_count",notsupportedread_count]]
            index, value = zip(*templist)
            templistS=pd.Series(value, index=index)

            combinedseries=r.append(templistS)

            deconlist.append(combinedseries)


        decondf=pd.DataFrame(deconlist)
        return decondf







bamfile="TWCY-1382-1382-BULK-PBMC_sorted"
outname=bamfile+"_out"

#c=CoreAlgo("/Users/irffanalahi/Research/weekly/for_9_24_20/Analysis/bamfiles/bamfiles_onlyregionIN_smMHB_cd4_cd8_g50_hypo_mhb_sorted_sorted/"+bamfile,40,20,"/Users/irffanalahi/Research/weekly/for_9_24_20/preparation/SM/MHBcpg2/smMHB_cd4_cd8_g50_hypo_assigned.txt_mhb","/Users/irffanalahi/Research/weekly/for_9_24_20/Analysis/result/"+outname)


#c=CoreAlgo("/Users/irffanalahi/Research/Research_update/Sequencing/understandBamFiles/try1/bamfiles_onlyregionIN_bluSMsingle450_MHBWGBS_pos_c2brename_corresSAM/bam_sorted/"+bamfile,40,20,"data/testsinglcpgRes/sample_singlecpg.txt_mhb","data/testsinglcpgRes/"+outname,2)

c=CoreAlgo("/Users/irffanalahi/Research/weekly/for_9_24_20/Usig_Single_Cpg_SM/450ksm/bamfiles/bamfiles_onlyregionIN_blleuko450kg50_hypo_pos_sorted_sorted/"+bamfile,40,20,"/Users/irffanalahi/Research/weekly/for_9_24_20/Usig_Single_Cpg_SM/450ksm/SM/blleuko450kg50_hypo_assigned.txt_bg","/Users/irffanalahi/Research/weekly/for_9_24_20/Usig_Single_Cpg_SM/450ksm/result/radius_0/"+outname,2)
