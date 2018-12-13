library(tidyverse)

#read in PageRank vector data from python
ranks <- read_tsv("sortedPageRank.txt")

#create 1-502 rank label
ranks <- ranks%>%
  mutate(num_rank = 1:n())

#plot rank and inlink density
ranks%>%
  ggplot(aes(x = rank))+
  geom_density()+
  labs(title = "Density Plot of PageRanks", x = "PageRank", y = "Density")

ranks%>%
  ggplot(aes(x = num_in))+
  geom_density()+
  labs(title = "Density Plot of Inlinks", x = "Number Inlinks", y = "Density")

#filter for urls not from Twitter
non_twitter <- ranks%>%
  filter(!grepl("twitter", url))

#plot rank and inlink density
non_twitter%>%
  ggplot(aes(x = rank))+
  geom_density()+
  labs(title = "Density Plot of PageRanks without Twitter Pages", x = "PageRank", y = "Density")

non-twitters%>%
  ggplot(aes(x = num_in))+
  geom_density()+
  labs(title = "Density Plot of Inlinks without Twitter", x = "Number Inlinks", y = "Density")

#remove chatbot pages
non_olark <- non_twitter%>%
  filter(!grepl("olark", url))

