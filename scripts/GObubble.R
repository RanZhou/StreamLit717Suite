# /usr/bin/env Rscript 
#Modified by Ran Zhou @2023 For python interface
args = commandArgs(trailingOnly=TRUE)

library(ggplot2)
install.packages('svglite')
library(svglite)

GO_all <- read.table(args[1],header=T,sep="\t",stringsAsFactors = T)

GO_all$logPx=GO_all$logP
GO_all$logPx[GO_all$logP < 1]=NA
GO_all$Fold[GO_all$logP < 1]=NA
GO_all$logPx[GO_all$logP < 2]=2
GO_all$logPx[GO_all$logP > 10]=10
#GO_all$Gene_number <- as.numeric(GO_all$Gene_number)
GO_all$GO_term <- factor(GO_all$GO_term,levels=unique(GO_all$GO_term))
GO_all$COND <- factor(GO_all$COND,levels=unique(GO_all$COND))

GO_all$'|log10(classic)|' <- GO_all$logPx

myplot<-
ggplot(GO_all, aes(x = GO_biological_process, y = COND)) +
  geom_point(data=GO_all,aes(y=COND, x=GO_term, size = Fold, colour = `|log10(classic)|`))+
  #scale_x_discrete(limits= GO_all$GO_term)+
  #scale_y_discrete(limits= GO_all$COND)+
  scale_color_gradient(low="purple",high="red",limits=c(2, 10))+
  coord_flip()+
  #theme_bw()+
  theme(axis.ticks.length=unit(-0.1, "cm"),
        axis.text.x = element_text(margin=margin(5,5,0,5,"pt")),
        axis.text.y = element_text(margin=margin(5,5,5,5,"pt")),
        axis.text = element_text(color = "black",size=12),
        panel.grid.minor = element_blank(),
        legend.title.align=0.5)+
  xlab("GO terms")+
  ylab("")+
  labs(color="-log10(pvalue)", size="Fold enrichment") #Replace by your variable names; \n allow a new line for text
  guides(y = guide_legend(order=2),
         colour = guide_colourbar(order=1))
uw=as.numeric(args[3])
uh=as.numeric(args[4])
ggsave(file=args[2], plot=myplot, width=uw, height=uh)
