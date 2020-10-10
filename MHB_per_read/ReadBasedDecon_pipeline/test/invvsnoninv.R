#### inv vs inv ARE same###


# install.packages("rstudioapi") # run this if it's your first time using it to install
library(rstudioapi) # load it
# the following line is for getting the path of your current open file
current_path <- getActiveDocumentContext()$path 
# The next line set the working directory to the relevant one:
setwd(dirname(current_path ))

invfile="/Users/irffanalahi/Research/weekly/for_10_15_20/friday_morning/Analysis/codedevelop/corr/deconresult/atleast3cpg.txt_ABSreadcount_divisionedNormalized.txt_CSxOut.txt"
noinvfile="/Users/irffanalahi/Research/weekly/for_10_15_20/friday_morning/Analysis/codedevelop/corr_checkinvertedcomma/deconresult/atleast3cpg.txt_ABSreadcount_divisionedNormalized.txt_CSxOut.txt"


invdf <- read.table(invfile,header=T,sep="\t")


invdf

write.table(invdf,"invdf.txt",sep = "\t", quote = F,row.names = F)

noninvdf <- read.table(noinvfile,header=T,sep="\t")

noninvdf

write.table(noninvdf,"noninvdf.txt",sep = "\t", quote = F,row.names = F)


#### inv vs inv ARE same###