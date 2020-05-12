library(e1071)
library(pi0)
library(colorRamps)


FDR = function(Z, ttest.pval, classes) {
  class1 = classes==1
  class2 = classes==2
  
  threshold <- 0.05
  if (sum(class1==TRUE)==2) {threshold <- 0.1}
  
  countGreaterPt5 = length(which(ttest.pval>0.5))
  countt = length(which(ttest.pval<threshold))
  
  # Compute FDR
  fdr = min(1.0, (2*countGreaterPt5*threshold)/countt)
  
  # Estimator for FDR
  pie0 = (2*countGreaterPt5)/nrow(Z) # ((double)2*countGreaterPt5)/array.length;
  
  # Compute q-value
  pval.order = order(ttest.pval)
  sp = ttest.pval[pval.order]
  qvalm = sp[length(sp)]*pie0 # double qvalm = sp[sp.length-1].pvalue*pie0; # -1 b/c java index-0 based?
  qvalues = rep(NA, length(sp)) # double[] qvalues = new double[sp.length];
  qvalues[length(qvalues)] = qvalm # qvalues[qvalues.length-1] = qvalm;
  end = length(sp)-1
  for (i in end:1){
    qval0 = (2*countGreaterPt5)*sp[i]/(i+1) # double qval0 = (((double)2*countGreaterPt5)*sp[i].pvalue)/(i+1);
    qval = min(qval0, qvalues[i+1])# double qval = Math.min(qval0,qvalues[i+1]);
    qvalues[i] = min(1.0, qval)# qvalues[i] = Math.min(1.0,qval);
  }
  qvalues = qvalues[order(pval.order)]
  return(qvalues)
}



# Calculate condition number
performOptimization <- function(B.list, G.min, G.max, median.comb, verbose=T) {
  k.array <- rep(NA, G.max - G.min + 1)
  for (G in G.min:G.max){
    
    # Take the G top significant genes
    BG.comb  <- unique(unlist(lapply(B.list, topGenes, top = G)))
    BG.comb.xpr <- subset(median.comb, rownames(median.comb) %in% BG.comb)
    
    # Calculate condition number using R kappa function
    k <- kappa(BG.comb.xpr, exact <- T)
    k.array[G - (G.min - 1)] <- k
  }
  G.opt <- which.min(k.array) + G.min - 1
  if (verbose) cat(paste(">Group size: ", G.opt, ", Kappa: ", min(k.array), "\n", sep = ""))
  if (verbose) cat(paste(">Best kappa:", min(k.array), "\n"))
  return(G.opt)
}


# Extract top genes from list
topGenes <- function(x, top){
  if (length(x) <= top) {
    x.extracted <- x
  } else {x.extracted <- subset(x, c(rep(T, top), rep(F, length(x) - top)))
  }
  return(x.extracted)
}





buildHyperProfile <- function(refsample,phenoclasses,FC_threshold){
  
  Z <- read.table(refsample, header=T, sep="\t", check.names=F)
  phenoClass <- read.table(phenoclasses, sep = "\t", row.names = 1)
  
  
  
  rownames(Z) <- Z[,1]
  
  # Remove immunoglobulin genes
  tokens <- grepl("-", Z[,1])
  ig.genes <- grepl("IG", Z[,1])
  Z <- Z[!(tokens & ig.genes),]
  ################################
  
  
  
  Z <- Z[order(rownames(Z)),]
  # Store gene names for later
  genesymbols = Z[,1]
  Z <- Z[,-1]
  Z <- data.matrix(Z)
  
  # Log2 transformation
  dummy <- 0
  if (min(Z)<= 0) {dummy <- 1}
  if (max(Z) > 50){
    Z[which(Z<0)] <- 0 # Set negative values to 0
    Z <- log10(Z+dummy)/log10(2)
  }
  
  
  # Un logtransform the expression values
  Z.transf <- 2^Z
  
  
  
  nCells <- nrow(phenoClass)
  nGenes <- nrow(Z)
  B.list <- list()
  n.sign <- rep(NA, nCells)
  median.comb <- NULL
  
  # Loop through each cell subtype
  for (i in 1:nCells){
    threshold <- 0.05
    
    # Save classes
    classes <- phenoClass[i,]
    class1 <- classes==1
    class2 <- classes==2
    if (sum(class1==TRUE)==2) {threshold <- 0.1}
    class1.mean <- rowMeans(Z[, class1])
    class2.mean <- rowMeans(Z[, class2])
    foldChange <- class1.mean - class2.mean
    
    # Store the median expression values of that cell type for later
    median.xpr <- apply(Z.transf[,class1], 1, median)
    
    # t-test
    dat <- cbind(Z[,class1],Z[,class2])
    ttest.pval <- matrix.t.test(dat, 1, sum(class1), sum(class2), pool <- F)
    
    
    ####################################################################
    #ttest.pval[is.na(ttest.pval)] <- 1.0
    ttest.pval[is.na(ttest.pval) & foldChange==0] <- 1.0
    ttest.pval[is.na(ttest.pval) & foldChange>0] <- 0.0
    ####################################################################
    
    
    # Calculating q-values
    #qval <- qvalue(ttest.pval)$qvalues
    qval = FDR(Z, ttest.pval, classes)
    #print(qval)
    
    
    pval.dt <- data.frame(cbind(rep(rownames(phenoClass[i,]), length(rownames(Z))),
                                rownames(Z),
                                ttest.pval,
                                qval,
                                foldChange))
    
    
    # Filter the significant genes from the reference sample file
    names(pval.dt) <- c("celltype", "genes", "pval", "qval", "logFC")
    #names(pval.dt) <- c("celltype", "genes", "pval", "logFC")
    
    FC <- pval.dt[ttest.pval < threshold,]
    #write.table(rownames(Z)[is.na(ttest.pval)], "na.ttest.txt", sep = "\t", quote=F)
    n.sign[i] <- nrow(FC)
    FC$qval <- as.numeric(as.character(FC$qval))
    FC$logFC <- as.numeric(as.character(FC$logFC))
    
    ## CHANGE THIS - WE WANT NEGATIVE
    FC = FC[FC$logFC >= FC_threshold,]
    # FC = FC[FC$logFC <= -0.5,]
    FC.filtered <- FC[FC$qval <= q.value,]
    
    ## CHANGE THIS - REMOVE NEGATIVE
    # Sort the significant genes by fold change
    FC.sorted <- FC.filtered[order(-FC.filtered$logFC),]
    # FC.sorted <- FC.filtered[order(FC.filtered$logFC),]
    
    # Store the gene lists sorted according to fold change, and restrict to G.max nr of genes
    if (length(FC.sorted$genes) >= G.max){
      B.list[[i]] <- as.character(FC.sorted$genes[1:G.max])
    } else {B.list[[i]] <- as.character(FC.sorted$genes)}
    
    # Add the median expression values of that cell type to dataset with all expression values
    if (is.null(median.comb)){
      median.comb <- data.frame(median.xpr)
      colnames(median.comb) <- rownames(phenoClass[i,])
    } else {
      tpm <- colnames(median.comb)
      median.comb <- cbind(median.comb, median.xpr)
      colnames(median.comb) <- c(tpm, rownames(phenoClass[i,]))
    }
  }
  
  
  return(list("B.list"=B.list,"median.comb"=median.comb))
}





# Main building signature matrix
#buildSignatureMatrix <- function(refsample, phenoclasses, do.QN=QN, G.min=G.min, G.max=G.max, q.value = q.value, filter=filter, k.max=k.max, verbose=verbose, label=label, outdir=outdir, single_cell=single_cell){
buildSignatureMatrix <- function(refsample,phenoclasses,outdir,q.value,G.min, G.max,k.max,FC_threshold,filter=filter){
  
  
  Hyper_List<-buildHyperProfile(refsample,phenoclasses,FC_threshold)
  
  B.list<-Hyper_List$B.list
  median.comb<-Hyper_List$median.comb
  
  
  # Option of filtering of non-hemapoietic genes
  if (filter){
    print("hereeeeeee before that read")
    ccle <- read.table("CCLE_nonBlood_Avgs.txt", sep="\t")
    print("hereeeeeee after that read")
    ccle <- ccle[which(ccle[,2] >= 7),]
    nonimmune <- read.table("XavierGEP.NonImmune.txt", sep="\t", header=T)
    nonimmune <- nonimmune[which(nonimmune[,3] >= 0.05),]
    tmp <- !(rownames(median.comb) %in% ccle[,1])
    median.comb <- median.comb[tmp,]
    tmp <- !(rownames(median.comb) %in% nonimmune[,1])
    median.comb <- median.comb[tmp,]
  }
  
  # Perform optimization
  G.opt <-performOptimization (B.list, G.min, G.max, median.comb, verbose=T)
  
  
  # Retrieve the optimal BG matrix - the Signature Matrix
  BG.opt  <- unique(unlist(lapply(B.list, topGenes, top = G.opt)))
  BG.opt.xpr <- subset(median.comb, rownames(median.comb) %in% BG.opt)
  
  phenoclassname = phenoclasses
  refsamplename = refsample
  
  
  # Write signature matrix to file:
  NAME = rownames(BG.opt.xpr)
  sign.matrix = data.frame(cbind(NAME, BG.opt.xpr), check.names=F)
  
  fname=paste(outdir, "SigMatrix",sep="/")
  #fname=paste(fname,"FC_threshold",FC_threshold,sep="_")
  
  write.table(sign.matrix,fname,sep = "\t", quote = F, row.names = F)
  
  
  pdf(file =paste(fname,"pdf",sep="."),width = 10, height = 10)
  heatmap(data.matrix(sign.matrix[,2:ncol(sign.matrix)]), col = blue2red(50), margins=c(15,5),labRow=NA ,ylab=)
  dev.off()
  
  return(sign.matrix)
}


#######################################
args <- commandArgs(TRUE)

refsample <-args[1]
phenoclasses <-args[2]
outdir <- args[3]
q.value<-as.numeric(args[4]) #0.3 lm 22
G.min<-as.numeric(args[5]) #50 lm 22
G.max<-as.numeric(args[6]) #200 lm22
filter<-args[7]
#####################################

k.max<-999  ### where is it used?

FC_threshold<-2

k<-buildSignatureMatrix(refsample,phenoclasses,outdir,q.value,G.min,G.max,k.max,FC_threshold,filter = filter)





















