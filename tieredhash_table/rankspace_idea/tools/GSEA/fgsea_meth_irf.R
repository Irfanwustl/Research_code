#if (!require("BiocManager", quietly = TRUE))
 # install.packages("BiocManager")

#BiocManager::install("fgsea")

library(fgsea)
library(data.table)
library(ggplot2)

args <- commandArgs(TRUE)
rankfile <-'BL22_all_matrix_promdata_intwith_Tregs_CpGdelta_info_faster.txt_3000_forheatunderlyingdata_ranked_pos.txt_sorted.txt_cyberin'
genefile<-'BL22_all_matrix_promdata_intwith_Tregs_CpGdelta_info_faster.txt_3000_forheatunderlyingdata_ranked_pos.txt_sorted_500.txt_cyberin_toy.txt'

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
#rank_lst <- na.omit(rank_lst)
rank_final <- rep(1, length(rank_lst))

print(length(rank_final))
rank_lst <- as.numeric(unlist(rank_lst))
attr(rank_final, "names") = rank_lst

print(summary(gene_lst))
print(table(is.na (gene_lst)))
print(class(gene_lst))


startval<-length(rank_lst)+10
for (row in 1:length(gene_lst))
{
  if (is.na(gene_lst[row]))
  {
    gene_lst[row] <- startval
    startval<-startval+1
  }
  
}
print(startval)
#gene_lst <- na.omit(gene_lst)

#data(examplePathways)
#data(exampleRanks)
set.seed(42)
#ex_path = examplePathways[["5991130_Programmed_Cell_Death"]]
#pdf(file =paste(genefile,"pdf",sep="."))
plotEnrichment(gene_lst, rank_final) + labs(title="Enrichment Curve for Methylation")
#dev.off()