require(stringi)
require(stringr)
setwd("/home/gijs/thesis/TetrisRL/src/outputs")
#file.choose()
#"/home/gijs/thesis/TetrisRL/src/output_scores.txt"

filename = file.choose()

data <-as.data.frame(read.table(filename, header = TRUE, sep=","))
columnname <- colnames(data)
data <- getElement(data, columnname)
x <- seq(1,length(data))

#metadata[[1]][1] == MLP / random
#metadata[[1]][2] == Complex? True/False
#metadata[[1]][3] == Date
metadata = strsplit(columnname, split="_")

plottitle = paste(metadata[[1]][1])
if(metadata[[1]][1] == "MLP"){
  if(metadata[[1]][2] == "True"){
    plottitle = paste(plottitle, "R = Complex ")
  }else{
    plottitle = paste(plottitle, "R = Simple ")
  }
}
plottitle = paste(plottitle, "avg =", mean(data))

plot(x,data, ylab="Points scored", xlab = "Game number", main = plottitle)
