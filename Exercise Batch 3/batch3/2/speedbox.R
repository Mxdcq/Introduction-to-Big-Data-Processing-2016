args = commandArgs(trailingOnly=TRUE)
speeds = unlist(read.table(args[1], header=TRUE), use.names=FALSE)
png(args[2])
boxplot(speeds)
