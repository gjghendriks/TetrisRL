
#setwd("/home/thesis/TetrisRL")
#file.choose()
#"/home/gijs/thesis/TetrisRL/src/output_scores.txt"

data <-as.data.frame(read.table("/home/gijs/thesis/TetrisRL/src/output_scores.txt"))
x <- seq(1,length(data$V1))
plot(x,data$V1)