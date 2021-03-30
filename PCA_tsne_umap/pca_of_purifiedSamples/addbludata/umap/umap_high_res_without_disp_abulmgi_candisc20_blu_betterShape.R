library(ggplot2)
library(RColorBrewer)
library(stringr)
library(plyr)
library(dplyr)

library(umap)

graphics.off()


args <- commandArgs(TRUE)
file_input <- args[1]
#topcpg<-as.numeric(args[2])



matt <- read.csv(file=file_input, header=FALSE, sep="\t")
m_n<-matt[,-1]  ######






m_n_3=m_n
dim(m_n)
dim(m_n_3)

set.seed(99999999)

myPr <- umap(m_n_3)

#head(myPr$layout)

#head(myPr)

to_bind<-cbind(matt , setNames(data.frame(myPr$layout), c('UMAP1', 'UMAP2')))

#head(to_bind)


TYPE=matt[,1]

tolog=cbind(TYPE,m_n_3)


nametoshow<-c()


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
    if (str_detect(TYPE[i],fixed(".bw")))
    {
      for_symb[i]<-"Normal (Blueprint)"
      col_str_tmp=sub(".*P-","",fname)
      
      cstat<-sub(pattern = "(.*)\\..*$", replacement = "\\1", basename(col_str_tmp))
      col_str[i]<-cstat
      if (cstat=="alt_activated_macrophage_M2")
      {
        nametoshow<-c(nametoshow,"M2")
      }
      else if(cstat=="CD14pos_classical_monocyte")
      {
        nametoshow<-c(nametoshow,"Mn")
      }
      else if(cstat=="Class-switched_mem_B_cell")
      {
        nametoshow<-c(nametoshow,"cB")
      }
      else if(cstat=="CM-CD4pos_T-cell")
      {
        nametoshow<-c(nametoshow,"cm4")
      }
      else if(cstat=="CM-CD8pos_T-cell")
      {
        nametoshow<-c(nametoshow,"cm8")
      }
      else if(cstat=="conventional_dendritic_cell")
      {
        nametoshow<-c(nametoshow,"cDC")
      }
      else if(cstat=="EM-CD4pos_T-cell")
      {
        nametoshow<-c(nametoshow,"em4")
      }
      else if(cstat=="EM-CD8pos_T-cell")
      {
        nametoshow<-c(nametoshow,"em8")
      }
      else if(cstat=="EM-CD8pos_T-cell_term-diff")
      {
        nametoshow<-c(nametoshow,"ed8")
      }
      else if(cstat=="Erythroblast")
      {
        nametoshow<-c(nametoshow,"Er")
      }
      else if(cstat=="immature_conventional_dendritic_cell")
      {
        nametoshow<-c(nametoshow,"iDC")
      }
      else if(cstat=="Inflammatory_macrophage_M1")
      {
        nametoshow<-c(nametoshow,"M1")
      }
      else if(cstat=="macrophage_M0")
      {
        nametoshow<-c(nametoshow,"M0")
      }
      else if(cstat=="mature_conventional_dendritic_cell")
      {
        nametoshow<-c(nametoshow,"mDC")
      }
      else if(cstat=="mature_neutrophils")
      {
        nametoshow<-c(nametoshow,"mN")
      }
      else if(cstat=="mature-eosinophil")
      {
        nametoshow<-c(nametoshow,"Eo")
      }
      else if(cstat=="megakaryocyte")
      {
        nametoshow<-c(nametoshow,"Mg")
      }
      else if(cstat=="memory_B_cell")
      {
        nametoshow<-c(nametoshow,"mB")
      }
      else if(cstat=="naive_B_cell")
      {
        nametoshow<-c(nametoshow,"nB")
      }
      else if(cstat=="naive-CD4-T-cell")
      {
        nametoshow<-c(nametoshow,"n4")
      }
      else if(cstat=="naive-CD8-T-cell")
      {
        nametoshow<-c(nametoshow,"n8")
      }
      else if(cstat=="NK_cell")
      {
        nametoshow<-c(nametoshow,"NK")
      }
      else if(cstat=="Plasma-cell")
      {
        nametoshow<-c(nametoshow,"PC")
      }
      else if(cstat=="Tregs")
      {
        nametoshow<-c(nametoshow,"Tr")
      }
      else
      {
        print("wrong cell state")
        print(cstat)
      }
    }
    else
    {
      for_symb[i]<-"Normal (This Study)"
      col_str[i]<-sub(".*P-","",fname)
    }
    
   
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
    print(TYPE[i])
  }
  
  

  
  
}

ggplot(to_bind,aes(x=UMAP1, y=UMAP2,label=nametoshow))+geom_text(size=2.5)+scale_shape_manual(values=seq(65,88))+scale_color_brewer(type='qual', palette='Set1')+scale_fill_brewer(type='qual',palette="Set1")+guides(label=guide_legend("Cell Type",ncol =1)) +theme(legend.title = element_text(size = 10),legend.text = element_text(size = 7,face="bold"))

out_file=paste(file_input,"pdf",sep="_umap.")
#outname=paste(file_input,topcpg,sep = "_")
#out_top_1000=paste(outname,"txt",sep=".")


#ggsave(out_file,width = 5, height = 4,dpi = 300,units = "in", device='pdf')

ggsave(out_file,dpi = 300,units = "in", device='pdf')

#write.table(tolog,out_top_1000,sep="\t", quote = FALSE,row.names=FALSE,col.names=FALSE)


