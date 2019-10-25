setwd("~/Documents/Projects & Work/Digital_Projects_Studio/Bentley")

library(tidyverse)

localaddress <- read.csv("data/AASP-Local Address.csv", stringsAsFactors = FALSE)

localaddress <- rename(localaddress, address = FullAdress)
localaddress <- rename(localaddress, Latitude = Longitude)
localaddress <- rename(localaddress, Longitude = Lattitude)

localaddress$Longitude <- as.numeric(localaddress$Longitude)
localaddress$Latitude <- as.numeric(localaddress$Latitude)

filtered <- localaddress %>%
  filter(is.na(Latitude)) %>%
  select(-c(Latitude, Longitude))

write.csv(filtered, "missing_latlong.csv")
