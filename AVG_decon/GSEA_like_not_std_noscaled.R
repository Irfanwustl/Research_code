


#main function
GSEA <- function(sig_matrix, mixture_file){
  
  
  #read in data
  X <- read.table(sig_matrix,header=T,sep="\t",row.names=1,check.names=F)
  Y <- read.table(mixture_file, header=T, sep="\t",check.names=F)
  
  rownames(Y) <-Y[,1]
  Y <- Y[,-1, drop = FALSE]
  
  X <- data.matrix(X)
  Y <- data.matrix(Y)
  

  #order
  X <- X[order(rownames(X)),,drop=F]
  Y <- Y[order(rownames(Y)),,drop=F]
  
  #intersect genes
  Xgns <- row.names(X)
  Ygns <- row.names(Y)
  YintX <- Ygns %in% Xgns
  Y <- Y[YintX,,drop=F]
  XintY <- Xgns %in% row.names(Y)
  X <- X[XintY,]
  
  header <- c('Mixture',colnames(X))
  
  result_vector<-rep(0,ncol(X))
  howmanytimes<-rep(0,ncol(X))

  
  
  
  
  
  
  ###################why#######################
  #X <- (X - mean(X)) / sd(as.vector(X))   
  #Y <- (Y - mean(Y)) / sd(Y)
  #############################################
  
  count=0
  for (r in rownames(Y))
  {
    
    index=which.max(X[r,])
    result_vector[index]<-result_vector[index]+Y[r,]
    howmanytimes[index]<-howmanytimes[index]+1
    count=count+1
  }

  
  
  
  result_vector<-result_vector/howmanytimes
  result_vector<-result_vector/100.0

  #result_vector[result_vector<0]<-0
  #result_vector<-result_vector/sum(result_vector)
  
  out <- c("dummy",result_vector)
  final_out<-rbind(header,out)
  return(final_out)

 
}


args <- commandArgs(TRUE)
sig_matrix<-args[1]
mixture_file<-args[2]
outfolder <- args[3]


final_result<-GSEA(sig_matrix,mixture_file)

#save results #####################################################################directory??????
out_file_name<-paste(basename(mixture_file),basename(sig_matrix),sep="_wrt_")
out_file_name<-paste(out_file_name,"deconvolved_result.txt",sep="_")
out_file_name<-paste(outfolder,out_file_name,sep="/")
write.table(final_result, file=out_file_name, sep="\t", row.names=F, col.names=F, quote=F)

