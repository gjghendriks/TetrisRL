require(stringi)
require(stringr)
setwd("/home/gijs/thesis/TetrisRL/src/outputs")
#file.choose()
#"/home/gijs/thesis/TetrisRL/src/output_scores.txt"

filename = file.choose()

data <-as.data.frame(read.table(filename))
x <- seq(1,length(data$V1))
titlearr = strsplit(filename, split="/")


plottitle = paste(titlearr[[1]][8], "avg =", mean(data$V1))
plot(x,data$V1, ylab="Points scored", xlab = "Game number", main = plottitle)
