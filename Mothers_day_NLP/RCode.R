# Natural Language Processing

# Importing the dataset
dataset_original = read.csv('Reviews.csv')

# Cleaning the texts
# install.packages('tm')
# install.packages('SnowballC')
library(tm)
library(SnowballC)
corpus = VCorpus(VectorSource(dataset_original$original_text))
corpus = tm_map(corpus, content_transformer(tolower))
corpus = tm_map(corpus, removeNumbers)
corpus = tm_map(corpus, removePunctuation)
corpus = tm_map(corpus, removeWords, stopwords())
corpus = tm_map(corpus, stemDocument)
corpus = tm_map(corpus, stripWhitespace)
s
# Creating the Bag of Words model
dtm = DocumentTermMatrix(corpus)
dtm = removeSparseTerms(dtm, 0.999)
dataset = as.data.frame(as.matrix(dtm))
dataset$sentiment_class = dataset_original$sentiment_class

dataset$sentiment_class[is.na(dataset$sentiment_class)] <- 0
# 
# Encoding the target feature as factor
dataset$sentiment_class = factor(dataset$sentiment_class, levels = c(-1, 0, 1))

# Splitting the dataset into the Training set and Test set
# install.packages('caTools')
library(caTools)
set.seed(123)
training_set = dataset[1:3235, ]
test_set = dataset[3236:4622, ]
# test_set['sentiment_class'] = 0
# split = sample.split(dataset$sentiment_class, SplitRatio = 0.65)
# training_set = subset(dataset, split == TRUE)
# test_set = subset(dataset, split == FALSE)

# Fitting Random Forest Classification to the Training set
# install.packages('randomForest')
library(randomForest)
set.seed(123)
classifier = randomForest(x = training_set[-1512],
                          y = training_set$sentiment_class,
                          ntree = 10) #25

# Predicting the Test set results
y_pred = predict(classifier, newdata = training_set[-1512])
# Making the Confusion Matrix
cm = table(training_set[, 1513], y_pred)
library(MLmetrics)
F1_Score(training_set[, 1513], y_pred)
y_pred_test = predict(classifier, newdata = test_set[-1512])
x = read.csv('dataset\\test.csv')
df <- data.frame(id = x$id,sentiment_class = y_pred_test)
# df$sentiment_class <- sapply(df$sentiment_class, as.numeric)
write.csv(df,'Submission_file_R.csv',row.names = FALSE, col.names = FALSE)
df2 = read.csv('submission_file2.csv')