require(stringi)
require(stringr)
setwd("/home/gijs/thesis/TetrisRL/src/outputs")

# x: the vector
# n: the number of samples
# centered: if FALSE, then average current sample and previous (n-1) samples
#           if TRUE, then average symmetrically in past and future. (If n is even, use one more sample from future.)
movingAverage <- function(x, n=1, centered=FALSE) {
  
  if (centered) {
    before <- floor  ((n-1)/2)
    after  <- ceiling((n-1)/2)
  } else {
    before <- n-1
    after  <- 0
  }
  
  # Track the sum and count of number of non-NA items
  s     <- rep(0, length(x))
  count <- rep(0, length(x))
  
  # Add the centered data 
  new <- x
  # Add to count list wherever there isn't a 
  count <- count + !is.na(new)
  # Now replace NA_s with 0_s and add to total
  new[is.na(new)] <- 0
  s <- s + new
  
  # Add the data from before
  i <- 1
  while (i <= before) {
    # This is the vector with offset values to add
    new   <- c(rep(NA, i), x[1:(length(x)-i)])
    
    count <- count + !is.na(new)
    new[is.na(new)] <- 0
    s <- s + new
    
    i <- i+1
  }
  
  # Add the data from after
  i <- 1
  while (i <= after) {
    # This is the vector with offset values to add
    new   <- c(x[(i+1):length(x)], rep(NA, i))
    
    count <- count + !is.na(new)
    new[is.na(new)] <- 0
    s <- s + new
    
    i <- i+1
  }
  
  # return sum divided by count
  s/count
}


filename = file.choose()

data <-as.data.frame(read.table(filename, header = TRUE, sep=","))
columnname <- colnames(data)
data <- getElement(data, columnname)
x <- seq(1,length(data))


### MOVING AVG
mov_avg <- movingAverage(data, 20)




### META

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





## PLOT
plot(x,data, ylab="Points scored", xlab = "Game number", main = plottitle)
lines(mov_avg, lty = 2 )
legend(320, 2, legend = "Moving average", lty = 2)
