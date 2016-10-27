args = commandArgs(trailingOnly=TRUE)
speeds = read.delim("linespeeds.txt", check.names=FALSE)
png(args[2])
boxplot(speeds, las=2)
