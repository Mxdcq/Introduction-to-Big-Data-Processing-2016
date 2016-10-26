# ming

speed <- read.table("/Users/mingxiaodong/Ming/Master Degree/Second year/Introduction to Big Data Processing 2016 /Exercise Batch 3/average_speed.txt", header = TRUE)
speed <- as.matrix(speed)
a_1 <- as.numeric(speed[1,2])
a_2 <- as.numeric(speed[2,2])
a_3 <- as.numeric(speed[3,2])
a_4 <- as.numeric(speed[4,2])
a_5 <- as.numeric(speed[5,2])
a_6 <- as.numeric(speed[6,2])
a_7 <- as.numeric(speed[7,2])
a_8 <- as.numeric(speed[8,2])
a_9 <- as.numeric(speed[9,2])
a_10 <- as.numeric(speed[10,2])
a_11 <- as.numeric(speed[11,2])
a_12 <- as.numeric(speed[12,2])
a_13 <- as.numeric(speed[13,2])
a_14 <- as.numeric(speed[14,2])
a_15 <- as.numeric(speed[15,2])
a_16 <- as.numeric(speed[16,2])
a_17 <- as.numeric(speed[17,2])
a_18 <- as.numeric(speed[18,2])
a_19 <- as.numeric(speed[19,2])
a_20 <- as.numeric(speed[20,2])
a_21 <- as.numeric(speed[21,2])
data <- c(a_1,a_2,a_3,a_4,a_5,a_6,a_7,a_8,a_9,a_10,a_11,a_12,a_13,a_14,a_15,a_16,a_17,a_18,a_19,a_20,a_21)
data

typeof(speed)
class(speed)
speed

boxplot(data, main="Boxplot of average speed", ylab="Average speed")
