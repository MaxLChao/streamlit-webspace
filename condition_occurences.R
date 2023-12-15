# condition occurences
library(data.table)
library(magrittr)
library(dplyr)
test = fread("tables/EAfromAKSmergedDeath.csv")
persondf = fread("tables/personDF.csv")

conds = lapply(unique(test$person_id), function(i){
  subset = test[person_id == i]
  table(subset$condition_name) %>% names()
})
top_conds = conds %>% unlist() %>% table() %>% sort(. ,decreasing = T)
# looks like most had some type of heart, renal, respiratory failure.
conds_summary = top_conds %>% as.data.table()
colnames(conds_summary) = c("Occurence Name", "Count")
fwrite(conds_summary, "tables/topconds.csv")

# Multimapping Conds
cond_nums = lapply(unique(test$person_id), function(i){
  test[person_id == i] %>% 
    .[,(condition_name)] %>%
    unique() %>%
    length()
  }) %>% unlist()
cond_nums %>% length()
hist(cond_nums)


# occurrences heatmapping
cond_multimaps = lapply(unique(test$person_id), function(i){
  test[person_id == i]  %>% select(person_id, condition_name) %>% unique(.)
}) %>% do.call(rbind,.)
# here I need to convert this to some type of identity matrix: 1100 unique occurrences
# for each patient we count the occurences that are shared together and save this as a data.frame/identity matrix
idmat = matrix(0, nrow = length(unique(cond_multimaps$condition_name)), 
               ncol = length(unique(cond_multimaps$condition_name))) %>% 
  as.data.frame()
rownames(idmat) = unique(cond_multimaps$condition_name)
colnames(idmat) = unique(cond_multimaps$condition_name)

# for loop for person_id
for (x in unique(cond_multimaps$person_id)){
  sub = cond_multimaps[person_id == x]$condition_name
  for (i in sub){
    for (j in sub){
      idmat[i,j] = idmat[i,j] + 1
    }
  }
}
# sort the rows/columns by occurence rates
order_indices <- match(conds_summary$`Occurence Name`, rownames(idmat))
idmat <- idmat[order_indices,]
idmat <- idmat[,order_indices]
# write out for use:
fwrite(idmat, "tables/idmatrix_occ.csv",row.names = T, col.names = T)
