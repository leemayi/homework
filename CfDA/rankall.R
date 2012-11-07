rankall <- function(outcome_param, num = "best") {
    outcome <- read.csv("outcome-of-care-measures.csv", colClasses="character", na.strings="Not Available")

    HEART_ATTACK <- 11
    HEART_FAILURE <- 17
    PNEUMONIA <- 23
    HOSPITAL_NAME <- 2
    STATE <- 7

    if (outcome_param == "heart attack") {
        col = HEART_ATTACK
    } else if (outcome_param == "heart failure") {
        col = HEART_FAILURE
    } else if (outcome_param == "pneumonia") {
        col = PNEUMONIA
    } else {
        stop("invalid outcome")
    }

    rank <- function(group) {
        group[1]
    }

    tapply(outcome, outcome$State, rank)
}

