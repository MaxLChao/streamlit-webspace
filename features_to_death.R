# mapping death to features
library(data.table)
library(magrittr)
library(dplyr)
library(caret)
test = fread("tables/EAfromAKSmergedDeath.csv")
persondf = fread("tables/personDF.csv")
library(Hmisc)

cleaned = persondf %>% select(gender_source_value, race_source_value, death, age)
# Split Sex
# shitty OHE cuz caret wasn't working with the gcc incompatibilities with the M2 chip.
# Fuck ME lmfao.
OHE = function(colname){
  df = matrix(0, 
              nrow=nrow(cleaned), 
              ncol = length(unique(cleaned[,get(colname)])))
  for (i in 1:ncol(df)){
    df[which(cleaned[,get(colname)] == unique(cleaned[,get(colname)])[i]),i] = 1
  }
  colnames(df) = unique(cleaned[,get(colname)])
  return(df)
}
# df = matrix(0, nrow=nrow(cleaned), ncol = length(unique(cleaned$gender_source_value)))
# for (i in 1:ncol(df)){
#   df[which(cleaned$gender_source_value == unique(cleaned$gender_source_value)[i]),i] = 1
# }
# colnames(df) = unique(cleaned$gender_source_value)


sex = OHE("gender_source_value")
#Race
race = OHE("race_source_value")
colnames(race)[6] = "NA"
#Age
final = cleaned %>% select(-c("gender_source_value", 
                      "race_source_value")) %>% 
  cbind(.,sex) %>% cbind(.,race) 

corrmat = rcorr(as.matrix(final))
corrs = cbind(corrmat$r[1,], corrmat$P[1,]) %>% as.data.frame()
colnames(corrs) = c("Correlation to death: (r)", "P-Value: (Uncorrected Pearson)")
fwrite(corrs, row.names = T, col.names = T, file = "tables/corrmat_death.csv")


# Sex death status count 
# Male 0  1.6
# Male 1  18
countframes = function(colname){
  df = matrix(0, 
              nrow=length(unique(persondf[,get(colname)]))*2, 
              ncol = 3) %>% as.data.frame()
  colnames(df) = c(colname, "death", "count")
  df[,1] = rep(unique(persondf[,get(colname)]), 2) %>% sort()
  df[,2] = rep(c(0,1), length(unique(persondf[,get(colname)])))
  for (i in 1:nrow(df)){
    df[i,3] = persondf[get(colname) == df[i,][[1]] & 
                         death ==df[i,][[2]],] %>% 
      nrow()
  }
  return(df)
}
# Get it to the right format and write out to a table:
sexlong = countframes("gender_source_value")
racelong = countframes("race_source_value")
racelong[1,1:2] = "NA"
colnames(sexlong)[1] = "sex"
colnames(racelong)[1] = "race"
# write out:
fwrite(sexlong, "tables/sex_barplot.csv")
fwrite(racelong, "tables/race_barplot.csv")

#Occurences