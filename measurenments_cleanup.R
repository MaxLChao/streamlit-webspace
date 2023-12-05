library(data.table)
library(magrittr)
p = fread("~/Downloads/1m_meas_wname.csv")
persondf = fread("~/Downloads/personDF.csv")
birthyears = stringr::str_extract(persondf$birth_datetime, pattern = "[0-9]+") %>% as.numeric()
deathyears = stringr::str_extract(persondf$death_date, pattern = "[0-9]+") %>% as.numeric()
persondf$birthyear = birthyears
persondf$deathyear = deathyears

age = lapply(1:length(birthyears), function(i){
  if (is.na(deathyears[i])){
    2023 - birthyears[i]
  }else {
    deathyears[i] - birthyears[i]
  }
}) %>% unlist()
persondf$age = age

wdp = p[!is.na(p$measurement_date)]
dates = wdp$measurement_date %>% stringr::str_split_fixed(., pattern = "-",n = 3) %>% as.data.frame()
colnames(dates) = c("year", "month", "day")
wdp = cbind(wdp, dates)
fwrite(wdp, "~/Downloads/meas_w_date.csv")

table(wdp$person_id) %>% sort(., decreasing = T) %>% .[.>10] %>% .[.<30]
wdp[person_id == "44710"]

# ok looks like we need to map back to the dates: 
# these probably need to be converted into a json of some sort

# probably need to write these to a json:
library(jsonlite)

# here we need to create a for loop of jsons with each patient
# allow a selection of these patients 

# for patients who have died
sdp = wdp[which(persondf[death == 1]$person_id %in% wdp$person_id)]

table(sdp$person_id) %>% sort(., decreasing = T) %>% head()
# more than 1 entry:
p_ids = table(sdp$person_id) %>% sort(., decreasing = T) %>% .[.>1] %>% names()
# looking into the concepts
table(sdp[person_id %in% p_ids]$measurement_name)
# this is the filter we should filter for
pdf_timeline = persondf[!is.na(persondf$death_date)] %>% .[person_id %in% p_ids]

sdp = sdp[person_id %in% pdf_timeline$person_id]

sdp$person_id %>% table() %>% sort()
# from here we take a selection of like 4 or so
sdp %>% dplyr::select(-c(measurement_concept_id, measurement_time, 
                       measurement_datetime, measurement_date, operator_concept_id,
                       value_as_concept_id, unit_concept_id, measurement_id, range_high, range_low,
                       visit_occurrence_id))
f_p = persondf[person_id %in% sdp$person_id]
f_p_dates = stringr::str_split_fixed(f_p$death_date, pattern = "-", n=3) %>% 
  .[,2:3] %>% data.table()
colnames(f_p_dates) = c("deathmonth", "deathday")
f_p = cbind(f_p,f_p_dates)
# generate:
# formatting needs to match:
# https://github.com/NUKnightLab/TimelineJS3/blob/master/website/templates/examples/houston/timeline3.json

# need to create a nested list
# first we have title
dp_ids = c("36855","8933", "4084","4")
for (x in dp_ids){
  # set up entry:
  json_meas = list()
  json_meas$title$text$headline = "Patient Timeline Summary:"
  json_meas$title$text$text = paste0("ID: ",f_p[person_id ==x]$person_id,"\n ",
                                     "Age: ",f_p[person_id ==x]$age, "\n ",
                                     "Sex: ", f_p[person_id ==x]$gender_source_value, "\n ",
                                     "Race: ", f_p[person_id ==x]$race_source_value, "\n ",
                                     "Death Status: Yes \n ",
                              "\n Taken from the measurements csv, mapping concept names to the measurement concept ids. 
                              Values were filtered for dates. Note that these are NOT all inclusive and dates may be missing"
                              )
  iter = sdp[person_id ==x]
  events = lapply(1:(nrow(iter)+1),function(i){
    if (i < nrow(iter)+1){
    list(
    start_date = list(month = iter[i,]$month,
                      day =iter[i,]$day,
                      year = iter[i,]$year),
    text = list(headline = iter[i,]$concept_class_id,
                text = iter[i,]$measurement_name)
    
    )
    } else{
      list(
        start_date = list(month = f_p[person_id ==x]$deathmonth,
                          day =f_p[person_id ==x]$deathday,
                          year = f_p[person_id ==x]$deathyear),
        text = list(headline = "Death",
                    text = "Patient Expired")
      )
    }
  })
  json_meas$events = events
  jsonlite::write_json(json_meas, 
                       paste0("~/Documents/code/streamlit-webspace/json/",
                              x, ".json")
                       )
}

# take one person that is alive


# for json$meas_events ... we have to map deeper for each concept
# "start_date": {
#   "month": "8",
#   "day": "9",
#   "year": "1963"
# },
# "text": {
#   "headline": "A Musical Heritage",
#   "text": "<p>Born in New Jersey on August 9th, 1963, Houston grew up surrounded by the music business. Her mother is gospel singer Cissy Houston and her cousins are Dee Dee and Dionne Warwick.</p>"
# }


