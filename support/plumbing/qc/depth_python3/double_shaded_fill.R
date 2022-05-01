library("data.table")
library("stringr")
args <- commandArgs(TRUE)
in_folder <- args[1]   

out_folder <- args[2]   


flist=list.files(path =in_folder,pattern="_depth$")
#print (flist)
#print("................")

for (file_input in flist)
  
{

  pngfile=paste(file_input,"png",sep = ".")
  
  pngfile=paste(out_folder,pngfile,sep = "/")  ############################################
  
  png(pngfile, bg="white",width = 900, height = 550)
  
  par(omi=c(0.25,0.25,0.25,0.25))
  par(mar=c(5,8,4,5))
  #par(mar=c(5,8,4,2))
  
 
  
  
  xpath=paste(in_folder,file_input,sep = "/")  #############################
  print(xpath)
  
  x5_path<-paste(xpath,"fifth",sep="_")
  x95_path<-paste(xpath,"ninefive",sep="_")

  
  x <- fread(xpath, header=F, sep="\t") ####
  
  x <- data.matrix(x)
  x <- as.numeric(x)
  
  
  x5<-fread(x5_path, header=F, sep="\t")
  x5 <- data.matrix(x5)
  x5 <- as.numeric(x5)
  
  
  x95<-fread(x95_path, header=F, sep="\t")
  x95 <- data.matrix(x95)
  x95 <- as.numeric(x95) 
  
  big_frame<-cbind(x,cbind(x5,x95))
  
  #print(big_frame)
  
  sorted_bigframe<-big_frame[order(big_frame[,1]),]

  #print("........")
  #print(sorted_bigframe)  
  #print("........")
  
  
  
  

  

  
  
 
  sorted_bigframe<- subset(sorted_bigframe,sorted_bigframe[,1] > 0)
  
  #print("yessss")
  #print(sorted_bigframe)
  
  
  
  x=sorted_bigframe[,1]
  stat=quantile(x, c(.01, .05,.25,.5, .75,.95,.99)) 
  
  sorted_bigframe <- subset(sorted_bigframe,sorted_bigframe[,1] <= stat[7])
  
  x<-sorted_bigframe[,1]
  mn=min(x)
  
  mx=max(x)
 
  #print(stat)
  
  
  
  
  #print(x)
  #print("final bigframe")
  #print(sorted_bigframe)
  #print('........')
  
  #print(x)
  
  
  sorted_bigframe_swapped<-sorted_bigframe[,c(2,1,3)]
  #print("swapped")
  #print(sorted_bigframe_swapped)
  ready_to_plot<-c(t(sorted_bigframe_swapped))
  
  #print(ready_to_plot)
  #print(length(ready_to_plot))
  
  col_len=length(ready_to_plot)/3
  col_vec<-c()
  type_vec<-c()
  for (i in 1:col_len)
  {
    three_col<-c("dodgerblue4","red","darkgreen")
    col_vec<-c(col_vec,three_col)
    #three_type<-c("h","p","p")
    #type_vec<-c(type_vec,three_type)
    
  }
  
  #print(col_vec)
  
  main_title=str_remove(file_input,".final.bam_depth")
  

  #plot(ready_to_plot,las=1,ylab="Depth",cex.axis=1,cex.lab=1,cex.main=2,main=main_title,xlab="",xaxt="n",type="h",col=col_vec)
  
  plot(ready_to_plot,log="y",las=1,ylab="Depth",cex.axis=1,cex.lab=1,cex.main=2,main=main_title,xlab="",xaxt="n",type="p",col=col_vec,pch=20)
  
  par(new = TRUE)
 
  #plot(ready_to_plot,las=1,ylab="Depth",cex.axis=1,cex.lab=1,cex.main=2,main=main_title,xlab="",xaxt="n",type="h",col=col_vec, yaxt = "n")
  plot(ready_to_plot,log="y",las=1,ylab="Depth",cex.axis=1,cex.lab=1,cex.main=2,main=main_title,xlab="",xaxt="n",type="p",col=col_vec, yaxt = "n",pch=20)
  annote_labels=c("1st%ile","5th%ile","25th%ile","50th%ile","75th%ile","95th%ile","99th%ile")
    
  axis(side=4,at=stat,las=2,labels = annote_labels,cex.axis=0.7)
  
  #abline(h=median(x), col="orangered", untf = F, lwd=3,lty=1)
  #abline(h=stat[1], col="blue", untf = F, lwd=3,lty=1)
  #legend("topright",legend=c("tile", "med"),col=c( "blue","orangered"),bty="n",cex=2,lwd=3,lty=1)
  
  legend("topleft",legend=c( "95th%ile", "mean","5th%ile"),
         col=c("darkgreen","red","dodgerblue4"),bty="n",cex=1,lwd=2,lty=1)
  
  
  mtext("bin size=10kb",side=1,outer=F)
  
  dev.off()
  
  new_stat=unname(stat)
  new_stat=append(new_stat,mn,after=0)
  
  #new_stat=append(stat, min, after = 0)
  new_stat
  
  
  file_bar=paste(file_input,"bar",sep = "_")
  
  pngfile_bar=paste(file_bar,"png",sep = ".")
  
  pngfile_bar=paste(out_folder,pngfile_bar,sep = "/")
  
  png(pngfile_bar, bg="white")
  
  barplot(new_stat, main=main_title,las=2,
          names.arg=c("min","1st%ile", "5th%ile", "25th%ile", "50th%ile","75th%ile","95th%ile","99th%ile"))
  dev.off()
  
  
  
  
  file_text=paste(file_input,"txt",sep = ".")
  
  outpath=paste(out_folder,file_text,sep = "/")
  
  if (file.exists(outpath))
  {
    file.remove(outpath)
  }
  
  fileConn<-file(outpath,"a")
  
  line="\n\n######################### Depth ########################\n\n"  ###############################
  
  writeLines(line, fileConn)
  line=paste("minimum",mn,sep = "\t")
  writeLines(line, fileConn)
  
  line=paste("01st%ile",stat[1],sep = "\t")
  writeLines(line, fileConn)
  
  line=paste("05th%ile",stat[2],sep = "\t")
  writeLines(line, fileConn)
  
  line=paste("25th%ile",stat[3],sep = "\t")
  writeLines(line, fileConn)
  
  line=paste("50th%ile",stat[4],sep = "\t")
  writeLines(line, fileConn)
  
  line=paste("75th%ile",stat[5],sep = "\t")
  writeLines(line, fileConn)
  
  line=paste("95th%ile",stat[6],sep = "\t")
  writeLines(line, fileConn)
  
  line=paste("99th%ile",stat[7],sep = "\t")
  writeLines(line, fileConn)
  
 
  
  
  close(fileConn)

}



