# HAcker earth Mothersday Challenge
# importing the train and test data
train_data = read.csv('dataset\\train.csv')
train_d = train_data$original_text
test_data = read.csv('dataset\\test.csv')
test_d = test_data$original_text
dataset = read.csv('Reviews.csv')
 # train_d contains all the original_text

# Creating the corpus
library(tm)
library(SnowballC)
corpus = VCorpus(VectorSource(train_d))
corpus = tm_map(corpus, content_transformer(tolower))
corpus = tm_map(corpus, removeNumbers)
corpus = tm_map(corpus, removePunctuation)
corpus = tm_map(corpus, removeWords, stopwords())
corpus = tm_map(corpus, stemDocument)
corpus = tm_map(corpus, stripWhitespace)
