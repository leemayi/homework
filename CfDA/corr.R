corr <- function(directory, threshold = 0) {
    ## 'directory' is a character vector of length 1 indicating
    ## the location of the CSV files

    ## 'threshold' is a numeric vector of length 1 indicating the
    ## number of completely observed observations (on all
    ## variables) required to compute the correlation between
    ## nitrate and sulfate; the default is 0

    ## Return a numeric vector of correlations

    correlation <- function(id) {
        data <- getmonitor(id, directory);
        idx = complete.cases(data$sulfate, data$nitrate);
        if (sum(idx) > threshold) {
            clean <- data[idx, ];
            cor(clean$sulfate, clean$nitrate);
        } else
            NA;
    }

    ret <- sapply(1:332, correlation);
    idx <- !is.na(ret);
    if (sum(idx) == 0)
        c()
    else
        ret[idx];
}
