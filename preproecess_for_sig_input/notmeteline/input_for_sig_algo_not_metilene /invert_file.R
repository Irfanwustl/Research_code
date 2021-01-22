
args <- commandArgs(TRUE)


refsample<-args[1]

out_file<-args[2]


Z <- read.table(refsample, header=T, sep="\t", check.names=F)



first_header<-names(Z)[1]

print(first_header)

rownames(Z) <- Z[,1]


Z <- Z[,-1,drop = FALSE]

Z<-100-Z
dat <- cbind(rownames(Z),Z)
names(dat)[1]<-first_header


#out_file=paste(basename(refsample),"inverted",sep = "_")
#out_file=paste(outdir,out_file,sep = "/")
write.table(dat,out_file,sep = "\t", quote = F,row.names = F)