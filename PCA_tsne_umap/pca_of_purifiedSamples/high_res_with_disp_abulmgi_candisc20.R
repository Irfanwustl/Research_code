library(ggplot2)
library(RColorBrewer)
library(stringr)
library(plyr)
library(dplyr)

graphics.off()

.get_variable_gene<-function(m) {
  
  df<-data.frame(mean=colMeans(m),cv=apply(m,2,sd)/colMeans(m),var=apply(m,2,var))
  df$dispersion<-with(df,var/mean)
  df$mean_bin<-with(df,cut(mean,breaks=c(-Inf,unique(quantile(mean,seq(0.1,1,0.05)),Inf))))
  var_by_bin<-ddply(df,"mean_bin",function(x) {
    data.frame(bin_median=median(x$dispersion),
               bin_mad=mad(x$dispersion))
  })
  df$bin_disp_median<-var_by_bin$bin_median[match(df$mean_bin,var_by_bin$mean_bin)]
  df$bin_disp_mad<-var_by_bin$bin_mad[match(df$mean_bin,var_by_bin$mean_bin)]
  df$dispersion_norm<-with(df,abs(dispersion-bin_disp_median)/bin_disp_mad)
  df
}
args <- commandArgs(TRUE)
file_input <- args[1]
topcpg<-as.numeric(args[2])



matt <- read.csv(file=file_input, header=FALSE, sep="\t")
m_n<-matt[,-1]  ######




df<-.get_variable_gene(m_n) 

disp_cut_off<-rev(sort(df$dispersion_norm))[topcpg] #########
disp_cut_off
df$used<-df$dispersion_norm >= disp_cut_off

#df$used
df$used[is.na(df$used)]<-FALSE
#df$used


m_n_3=m_n[df$used]
dim(m_n)
dim(m_n_3)

myPr <- prcomp(m_n_3)

to_bind<-cbind(matt , myPr$x)

TYPE=matt[,1]

tolog=cbind(TYPE,m_n_3)





for_symb<-character(0)

tstr<-as.character(TYPE)

col_str<-character(0)
for (i in 1:length(TYPE))
{
  b=str_detect(TYPE[i],fixed("-P-",ignore_case=TRUE))
  c=str_detect(TYPE[i],fixed("-T-",ignore_case=TRUE))
  d=str_detect(TYPE[i],fixed("GSM",ignore_case=TRUE))
  fname=sub(pattern = "(.*)\\..*$", replacement = "\\1", basename(as.character(TYPE[i])))
  if(b)
  {
    for_symb[i]<-"Normal (This Study)"
    col_str[i]<-sub(".*P-","",fname)
   
  }
  else if(c)
  {
    for_symb[i]<-"Tumor (This Study)"
    col_str[i]<-sub(".*T-","",fname)
    
  }
  else if (d)
  {
    for_symb[i]<-"PDAC (Public data)"
    col_str[i]<-"EpCam"
  }
  else
  {
    print ("badddd")
  }
  
  

  
  
}

ggplot(to_bind,aes(x=PC1,y=PC2,shape=for_symb,col=col_str,fill=col_str))+geom_point()+scale_shape()+scale_color_brewer(type='qual', palette='Set1')+scale_fill_brewer(type='qual',palette="Set1")+guides(shape=guide_legend("Origin"),fill=FALSE,color=guide_legend("Cell Type"))


out_file=paste(file_input,".pdf",sep="_")
outname=paste(file_input,topcpg,sep = "_")
out_top_1000=paste(outname,"txt",sep=".")


ggsave(out_file,width = 5, height = 4,dpi = 300,units = "in", device='pdf')

write.table(tolog,out_top_1000,sep="\t", quote = FALSE,row.names=FALSE,col.names=FALSE)


