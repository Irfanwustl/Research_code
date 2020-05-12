

args <- commandArgs(TRUE)
file_input <-args[1]
x_in<-args[2]
y_in<-args[3]
lcol<-args[4]


Data <- read.table(file_input,header=T,sep="\t")





library("ggpubr")


if ( x_in %in% colnames(Data) & y_in %in% colnames(Data) ) 
{
  filename<-paste(file_input,x_in,sep="_")
  pdf(file =paste(filename,"pdf",sep="."))
  print(ggscatter(Data, x = x_in, y = y_in, 
            add = "reg.line", #conf.int = TRUE, 
            cor.coef = TRUE, cor.method = "pearson",
            xlab = x_in, ylab = y_in,label="Mixture",color = lcol))
  
  dev.off()
}


