require(stringi)
require(stringr)
setwd("/home/gijs/thesis/TetrisRL/src/outputs/mlp")
MOVINGAVERAGE = 100


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

extractMeta <- function(string, mean){
  
  ### META
  
  #metadata[[1]][1] == MLP / random
  #metadata[[1]][2] == Complex? True/False
  #metadata[[1]][3] == Date
  metadata = strsplit(string, split="_")
  plottitle = paste(metadata[[1]][1])
  if(metadata[[1]][1] == "MLP"){
    if(metadata[[1]][2] == "True"){
      plottitle = paste(plottitle, "R = Complex ")
    }else{
      plottitle = paste(plottitle, "R = Simple ")
    }
  }
  data <- getElement(data, string)
  plottitle = paste(plottitle, "avg =", mean)
  plottitle
}

#read files and extract collumn names
my_files = list.files(pattern="*.txt")
my_data <- lapply(my_files, read.csv, header = TRUE)



#prepare data, columnnames, running averages
columnnames <- 1:length(my_files)
for(i in 1:length(my_files)){
  columnnames[i] <- colnames(my_data[[i]])
}


### MOVING AVG
mov_avg <-vector("list", length(my_files))
my_clean_data <- vector("list", length(my_files))

for(i in 1:length(my_files)){
  my_clean_data[[i]] <- getElement(my_data[[i]],columnnames[i]) 
  mov_avg[[i]] <- movingAverage(data[[i]], MOVINGAVERAGE)
}




### seperate between complex and simple
averageComplex <- vector("double", length(my_clean_data[[1]]))
averageSimple <- vector("double", length(my_clean_data[[1]]))
for(i in 1:length(my_files)){
  string = extractMeta(columnnames[i], mean(my_clean_data[[i]]))
  if(grepl("Complex", string, fixed = TRUE)){
    # complex representation
    averageComplex = averageComplex + my_clean_data[[i]]
  } else if(grepl("Simple", string, fixed = TRUE)){
    averageSimple = averageSimple + my_clean_data[[i]]
  } else{
    print("sldfjlks")
  }
}
averageComplex = averageComplex / (length(my_clean_data) / 2)
averageSimple = averageSimple / (length(my_clean_data) / 2)

## PLOT
x <- seq(1,length(my_clean_data[[1]]))
plot(x,movingAverage(averageComplex, MOVINGAVERAGE), ylab="Points scored", xlab = "Game number", 
     main = "MLP Complex vs Simple representations", type = "l", lty = 1)
#lines(, lty = 2 )
#plot(x, data)
lines(movingAverage(averageSimple, MOVINGAVERAGE), lty = 2)
legend(500, 1, legend = c(paste("Complex avg = ", mean(averageComplex)), paste("Simple avg = ", mean(averageSimple))), lty = c(1,2))

