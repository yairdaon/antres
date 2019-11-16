source('AuxiliaryFunctionsClinicalData.R')
admission <- read.csv('backup/Admission data RandID.csv')
admission$grpd_diagnosis <- combineDiag(admission)
write.csv(admission, "data/admission_r.csv", row.names = FALSE)

antibiotics <- read.csv('backup/Antibiotics RandID.csv')
cultures <- read.csv('backup/Cultures w remarks RandID.csv')
lst <- combineDrugNames(antibiotics, cultures)
antibiotics$com_name <- lst[[1]]
antibiotics$family <- lst[[2]]
cultures$family <- lst[[3]]
write.csv(cultures, "data/cultures_r.csv", row.names = FALSE)
write.csv(antibiotics, "data/antibiotics_r.csv", row.names = FALSE)
