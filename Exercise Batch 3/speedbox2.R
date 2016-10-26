inputFile <- "newdata.txt"
con  <- file(inputFile, open = "r")

while (length(oneLine <- readLines(con, n = 1, warn = FALSE)) > 0) {
        myVector <- (strsplit(oneLine, " "))#read each line
}

s<-boxplot(as.numeric(myVector[[1]]), ylab ="speed (km/h)", 
           main = "average speed")

dev.copy(png,filename="speedbox.png")
dev.off ()
close(con)
