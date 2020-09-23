import pandas as pd




class CountingDecon:
    def __init__(self, allinfodf,outfilename,**kwargs):
        self.allinfodf=allinfodf
        self.outfilname = outfilename
        self.rundecon()
        self.decon_unbalancedSM()





    def rundecon(self):
        allinfodfgrp=self.allinfodf.groupby(['celltype'])

        sumdict={}
        for name,gr in allinfodfgrp:
            grwisesum=gr["supported_read_count"].sum()

            sumdict.update({name:[grwisesum]})

        print(sumdict)
        sumdf=pd.DataFrame(sumdict)
        sumdfnormalized=sumdf.div(sumdf.sum(axis=1), axis=0)
        print(sumdf)
        print(sumdfnormalized)

        sumdf.to_csv(self.outfilname+"_decon_sumdf.txt",sep="\t", index=False)
        sumdfnormalized.to_csv(self.outfilname + "_decon_sumdf_nomrmalized.txt", sep="\t", index=False)

    def decon_unbalancedSM(self):
        allinfodfgrp = self.allinfodf.groupby(['celltype'])

        ratiodict={}
        for name, gr in allinfodfgrp:
            grwisematchedsum = gr["supported_read_count"].sum()
            grwisetotalsum=gr["filtered_read_count"].sum()
            grwiseratio=(1.0*grwisematchedsum)/grwisetotalsum
            ratiodict.update({name:[grwiseratio]})

        print(ratiodict)

        ratiodf=pd.DataFrame(ratiodict)
        ratiodfnormalized=ratiodf.div(ratiodf.sum(axis=1), axis=0)

        print(ratiodf)
        print(ratiodfnormalized)

        ratiodf.to_csv(self.outfilname+"_decon_ratiodf.txt",sep="\t", index=False)
        ratiodfnormalized.to_csv(self.outfilname + "_decon_ratiodf_normalized.txt", sep="\t", index=False)


