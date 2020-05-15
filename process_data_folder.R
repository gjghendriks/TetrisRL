require(stringi)
require(stringr)

MOVINGAVERAGE = 100

# function to calculate the moving average
movingAverage = function(x, n=1, centered=FALSE) {
  
  # x: the vector
  # n: the number of samples
  # centered: if FALSE, then average current sample and previous (n-1) samples
  #           if TRUE, then average symmetrically in past and future. (If n is even, use one more sample from future.)
  if (centered) {
    before = floor  ((n-1)/2)
    after  = ceiling((n-1)/2)
  } else {
    before = n-1
    after  = 0
  }
  
  # Track the sum and count of number of non-NA items
  s     = rep(0, length(x))
  count = rep(0, length(x))
  
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


# function to plot one folder of datapoints
processFolder <- function(folderString, lineType){
  #browser()
  setwd(paste("/home/gijs/thesis/TetrisRL/src/outputs", folderString, sep = ""))
  
  #read files
  my_files = list.files(pattern="*.txt")
  my_data <- lapply(my_files, read.csv, header = TRUE)
  
  #extract columnnames
  columnnames <- 1:length(my_files)
  for(i in 1:length(my_files)){
    columnnames[i] <- colnames(my_data[[i]])
  }
  
  ### clean_data
  my_clean_data <- vector("list", length(my_files))
  for(i in 1:length(my_files)){
    my_clean_data[[i]] <- getElement(my_data[[i]],columnnames[i]);
  }
  
  ### average over different runs
  averagedData <- rep(0, 3000)
  for(i in 1:length(my_files)){
    for(j in 1:3000){
      averagedData[j] = averagedData[j] + my_clean_data[[i]][j]
    }
  }
  averagedData = averagedData / length(my_files)
  
  
  
  
  

  #plot
  x <- seq(1,3000)
  lines(x, movingAverage(averagedData, MOVINGAVERAGE), lty = lineType, col = lineType)
  #plot(x,movingAverage(averagedData, MOVINGAVERAGE), ylab="Points scored", xlab = "Game number", 
  #     main = "MLP Complex vs Simple representations", type = "l", lty = 2, xlim = c(0,3000), ylim = c(0,40))
  #lines(, lty = 2 )
  #plot(x, data)
  
  
  
}
plot(NULL,NULL, xlim = c(1,3000), ylim = c(1, 30), xlab = "Epochs", ylab = "Score") 
title("State representations")
legend(2300, 29, legend = c("diff", "diff max holes wells", "holes", "holes wells", "max", "wells", "every"), lty = c(1, 2,3,4,5,6,7), col = c(1, 2,3,4,5,6,7))
processFolder("/diff_", 1)
processFolder("/diff_max_holes_wells_", 2)
processFolder("/holes_", 3)
processFolder("/holes_wells_", 4)
processFolder("/max_", 5)
processFolder("/wells_", 6)
processFolder("/MLP Everything turned on", 7)



