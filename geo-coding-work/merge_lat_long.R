setwd("~/Documents/Projects & Work/Digital_Projects_Studio/Bentley")

library(tidyverse)

latlong <- read.csv("final_dateaddress_latlong copy2.csv", stringsAsFactors = FALSE)
localaddress <- read.csv("AASP-Local Address.csv", stringsAsFactors = FALSE)

localaddress <- rename(localaddress, address = FullAdress)
localaddress <- rename(localaddress, Latitude = Longitude)
localaddress <- rename(localaddress, Longitude = Lattitude)

localaddress$Longitude <- as.numeric(localaddress$Longitude)
localaddress$Latitude <- as.numeric(localaddress$Latitude)
localaddress["Longitude"] <- round(localaddress$Longitude, 5)

localaddress %>%
  select(Longitude) %>%
  filter(!is.na(Longitude)) %>%
  summarize(count = n())

latlong <- rename(latlong, Longitude = Lon)
latlong <- rename(latlong, Latitude = Lat)

latlong$Latitude<- as.numeric(latlong$Latitude)
latlong$Longitude <- as.numeric(latlong$Longitude)

#localaddress$HouseNumber[is.na(localaddress$HouseNumber)] <- " "

#localaddress_united <- localaddress %>%
#  unite(address, HouseNumber, StreetDorm, sep = " ")

joined <- full_join(localaddress, latlong, by=c("address", "Latitude", "Longitude"))

write.csv(joined, file="joined.csv")
joined %>%
  select(Longitude) %>%
  filter(!is.na(Longitude)) %>%
  summarize(count = n())
