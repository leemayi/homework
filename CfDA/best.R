best <- function(state, outcome_param) {
    ## Read outcome data
    outcome <- read.csv("outcome-of-care-measures.csv", colClasses = "character")

    HEART_ATTACK <- 11
    HEART_FAILURE <- 17
    PNEUMONIA <- 23
    HOSPITAL_NAME <- 2

    outcome[, PNEUMONIA] <- as.numeric(outcome[, PNEUMONIA])

    if (outcome_param == "heart attack") {
        col = HEART_ATTACK
    } else if (outcome_param == "heart failure") {
        col = HEART_FAILURE
    } else if (outcome_param == "pneumonia") {
        col = PNEUMONIA
    } else {
        col = -1
    }

    outcome[,col] <- as.numeric(outcome[, col])
    hos <- outcome[outcome$State==state,]

    attack <- hos[!is.na(hos[,col]),]
    i = sort(attack[,col], index.return=T)$ix[1]

    attack[i, HOSPITAL_NAME]

    ## Check that state and outcome are valid

    ## Return hospital name in that state with lowest 30-day death
    ## rate
}
