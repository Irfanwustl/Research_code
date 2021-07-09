

args <- commandArgs(TRUE)
file_input <-args[1]
file_output<-args[2]
x_in<-args[3]
y_in<-args[4]
lcol<-'red'


Data <- read.table(file_input,header=T,sep="\t")





library("ggpubr")


if ( x_in %in% colnames(Data) & y_in %in% colnames(Data) ) 
{
  
  pdf(file =paste(file_output,"pdf",sep="."))
  print(ggscatter(Data, x = x_in, y = y_in, 
            add = "reg.line", #conf.int = TRUE, 
            cor.coef = TRUE, cor.method = "pearson",
            xlab = x_in, ylab = y_in,label="Mixture",color = lcol))
  
  dev.off()
}


