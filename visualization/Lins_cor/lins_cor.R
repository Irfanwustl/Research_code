library(DescTools)
args <- commandArgs(TRUE)
file_input <-args[1]


Data <- read.table(file_input,header=T,sep="\t")

result<-CCC(Data$predicted,Data$ground_truth,  ci = "z-transform",
    conf.level = 0.95)

print(result$rho.c)