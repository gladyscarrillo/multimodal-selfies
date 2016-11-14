data <- read.csv(file="/home/gcarrillo/Documentos/MCC/pasantias/video/result.txt", header=FALSE, sep=",")
library(qcc)
library(ggplot2)


df <- as.data.frame(data)

ggplot(data=df, aes(x=V1, y=V2, group=1)) +
  geom_line()+
  geom_point() + xlab("")