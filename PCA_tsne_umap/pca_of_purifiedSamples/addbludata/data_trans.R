args <- commandArgs(TRUE)
file_input <- args[1]

out_file_name= args[2]

MyData <- read.csv(file=file_input, header=FALSE, sep="\t")


tdata<-t(MyData)


write.table(tdata,out_file_name,sep="\t",row.names=FALSE,col.names=FALSE, quote = FALSE)