rankhospital <- function(state, outcome_param, num = "best") {
    outcome <- read.csv("outcome-of-care-measures.csv", colClasses="character", na.strings="Not Available")

    HEART_ATTACK <- 11
    HEART_FAILURE <- 17
    PNEUMONIA <- 23
    HOSPITAL_NAME <- 2

    if (outcome_param == "heart attack") {
        col = HEART_ATTACK
    } else if (outcome_param == "heart failure") {
        col = HEART_FAILURE
    } else if (outcome_param == "pneumonia") {
        col = PNEUMONIA
    } else {
        stop("invalid outcome")
    }

    state.idx = outcome$State == state
    if (sum(state.idx) == 0) {
        stop("invalid state")
    }
    data1 = outcome[state.idx,]
    data1[,col] <- as.numeric(data1[,col])

    valid.idx = !is.na(data1[,col])
    if (sum(valid.idx) == 0) {
        stop("invalid state")
    }
    data <- data1[valid.idx,]

    rank = sort(data[,col], index.return=T)$ix
    if (num == "best") {
        i = 1
    } else if (num == "worst") {
        i = length(rank)
    } else if (!is.numeric(num) || num < 1 || num > length(rank)) {
        i = -1
    } else {
        i = num
    }

    if (i == -1) {
        "NA"
    } else {
        data[rank[i], HOSPITAL_NAME]
    }
    ## Read outcome data
    ## Check that state and outcome are valid
    ## Return hospital name in that state with the given rank
    ## 30-day death rate
}

