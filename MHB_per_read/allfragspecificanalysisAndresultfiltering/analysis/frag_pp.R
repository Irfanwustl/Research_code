
library("stringr")
args <- commandArgs(TRUE)
in_folder <- args[1]   

out_folder <- args[2]   


flist=list.files(in_folder)

for (file_input in flist)
  
{
  
  pngfile=paste(file_input,"png",sep = ".")
  
  pngfile=paste(out_folder,pngfile,sep = "/")  ############################################
  
  png(pngfile, bg="white")
  
  par(omi=c(0.25,0.25,0.25,0.25))
  par(mar=c(5,8,4,2))
  par(mar=c(5,8,4,2))
  
  xpath=paste(in_folder,file_input,sep = "/")
  
  x <- read.table(xpath, header=F, sep="\t")
  x <- data.matrix(x)
  x <- as.numeric(x)
  #x <- x[which(x > 0)]
  irfd<-x  ##########
  
  stat=quantile(x, c(.01, .05,.25,.5, .75,.95,.99)) 
  
  mx=max(x)
  mn=min(x)
  print(mx)
  
  #x <- x[which(x <=500)]
  
  par(mgp = c(6.5, 1, 0))
  
  
  
  main_title=str_remove(file_input,".final.bam_frag")#####################
  
  hist(x,breaks=50,las=1,ylab="Count",cex.axis=1,cex.lab=1,cex.main=2,main=main_title,xlab="",col="dodgerblue4")
 
 
  abline(v=median(irfd), col="orangered", untf = F, lwd=3,lty=1)  ########
  legend("topright","median",col="orangered",bty="n",cex=2,lwd=3,lty=1)
  mtext("Fragment length (bp)",side=1,outer=F)
  
  dev.off()
  
  
  
  
  new_stat=unname(stat)
  new_stat=append(new_stat,mn,after=0)
  
  
  
  
  file_bar=paste(file_input,"bar",sep = "_")
  
  pngfile_bar=paste(file_bar,"png",sep = ".")
  
  pngfile_bar=paste(out_folder,pngfile_bar,sep = "/")
  
  png(pngfile_bar, bg="white")
  
  barplot(new_stat, main=main_title,las=2,
          names.arg=c("min","1st%ile", "5th%ile", "25th%ile", "50th%ile","75th%ile","95th%ile","99th%ile"),ylim=range(pretty(c(0, new_stat))))
  dev.off()
  
  file_text=paste(file_input,"txt",sep = ".")
  
  outpath=paste(out_folder,file_text,sep = "/")
  
  if (file.exists(outpath))
  {
    file.remove(outpath)
  }
  
  fileConn<-file(outpath,"a")
  
  line="\n\n######################### Fragment ########################\n\n"  ###############################
  
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
  
  
  
  
  
  
  
  