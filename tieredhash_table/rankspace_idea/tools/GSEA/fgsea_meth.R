#if (!require("BiocManager", quietly = TRUE))
 # install.packages("BiocManager")

#BiocManager::install("fgsea")

library(fgsea)
library(data.table)
library(ggplot2)

args <- commandArgs(TRUE)
rankfile <-args[1]
genefile<-args[2]

data_rank <- read.delim(rankfile, sep="\t")
ranks <- data_rank[,1]
rank_lst <- rep(NA, length(ranks))

data_gene <- read.delim(genefile, sep="\t")
genes <- data_gene[,1]
gene_lst <- rep(NA, length(genes))
for (x in 1:length(ranks))
{
  rank_lst[x] <- toString(x)
  if (ranks[x] %in% genes)
  {
    idx <- match(ranks[x], genes)
    gene_lst[idx] <- x
  }
}
rank_lst <- na.omit(rank_lst)
rank_final <- rep(1, length(rank_lst))
rank_lst <- as.numeric(unlist(rank_lst))
attr(rank_final, "names") = rank_lst
gene_lst <- na.omit(gene_lst)

#data(examplePathways)
#data(exampleRanks)
set.seed(42)
#ex_path = examplePathways[["5991130_Programmed_Cell_Death"]]
pdf(file =paste(genefile,"pdf",sep="."))
plotEnrichment(gene_lst, rank_final) + labs(title="Enrichment Curve for Methylation")
dev.off()