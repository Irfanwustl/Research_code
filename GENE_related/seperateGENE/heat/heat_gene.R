
library(gplots)
library(viridis)

args <- commandArgs(TRUE)
file_input <- args[1]


data <- read.table(file_input,header=T,sep="\t",row.names = 1)

#data<- data[seq(dim(data)[1],1),]  ####### reverse order
data<-data.matrix(data)



pdf(file =paste(file_input,"pdf",sep="."),width = 10, height = 10)


map = heatmap.2(data, col=viridis,key=TRUE,trace="none",margins=c(15,6),density.info="none",dendrogram='none', Rowv=FALSE,Colv=FALSE,scale="none",na.color="dimgray",labRow = FALSE)
title(sub(pattern = "(.*)\\..*$", replacement = "\\1", basename(file_input)), line= -3,cex.main = 5)
dev.off()
