

args <- commandArgs(TRUE)
file_input <- args[1]
ground_input <- args[2]


out_file<-args[3]


Data1 <- read.table(file_input,header=T,sep="\t")

Data2 <- read.table(ground_input,header=T,sep="\t")

total <- merge(Data1,Data2,by="Mixture")

#total

write.table(total,out_file,sep = "\t", quote = F,row.names = F)