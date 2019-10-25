library(tidyverse)

setwd("~/Documents/projects/digital-projects-studio/bentley/code/data")

data <- read.csv("AASP-Addreses2019-08.csv")

data$AddressCode..HouseNumber <- str_replace_na(data$AddressCode..HouseNumber, "")

temp <- data %>%
  mutate(address = str_c(AddressCode..HouseNumber, AddressCode..StreetDorm, sep = " "))

temp$address <- trimws(temp$address, which = "left", whitespace = "[ \t\r\n]")

new_data <- temp %>%
  select(Year, address, AddressCode..Lattitude, AddressCode..Longitude) %>%
  group_by(Year, address, AddressCode..Lattitude, AddressCode..Longitude) %>%
  summarise(Count = n())

new_data <- new_data %>%
  rename(Date = Year, latitude = AddressCode..Lattitude, longitude = AddressCode..Longitude)

write.csv(new_data, "newdata.csv", row.names = FALSE)