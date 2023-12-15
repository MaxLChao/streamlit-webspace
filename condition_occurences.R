# condition occurences
test = fread("tables/EAfromAKSmergedDeath.csv")
persondf = fread("tables/personDF.csv")

conds = lapply(unique(test$person_id), function(i){
  subset = test[person_id == i]
  table(subset$condition_name) %>% names()
})
top_conds = conds %>% unlist() %>% table() %>% sort(. ,decreasing = T)
# looks like most had some type of heart, renal, respiratory failure.

#Overview:
