
#setwd("/home/thesis/TetrisRL")
#file.choose()
#"/home/gijs/thesis/TetrisRL/src/output_scores.txt"

data <-as.data.frame(read.table(file.choose()))
x <- seq(1,length(data$V1))
plot(x,data$V1, ylab="Points scored", xlab = "Game number")

