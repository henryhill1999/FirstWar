# import results from csv file
cnt_by_page <- read.csv('res.csv')

# append a column which represents the date as a decimal since 1900
cnt_by_page$date <- cnt_by_page$Year-1900 + (1/12)*cnt_by_page$Month + (1/365)*cnt_by_page$Day

# append a column which represents the total number of place-name mentions for each page
cnt_by_page$sum_mentions <- rowSums(cnt_by_page[,13:261])

# append a column which represents the total number of foreign (non-US) place-name mentions for each page
cnt_by_page$foreign_mentions <- cnt_by_page$sum_mentions-cnt_by_page$US

# append a column which represents the total number of foreign (non-US) place-name mentions for each page
cnt_by_page$foreign_ratio <- cnt_by_page$foreign_mentions/cnt_by_page$sum_mentions

# append a column which represents the country with the most mentions for each page
cnt_by_page$most_mentions <- names(cnt_by_page)[max.col(cnt_by_page[,13:261])+12]

# append a column which represents nPage - page (i.e. # of pages from last page)
cnt_by_page$pagesFromEnd <- cnt_by_page$nPage-cnt_by_page$Page

# append a column which indicates whether a page is first
cnt_by_page$frontPage <- as.numeric(cnt_by_page$Page == 1)

# create a linear regression to model the appearance of placenames over time
model <- lm(sum_mentions ~ date + Page + frontPage + Sun + pagesFromEnd + frontPage*date, data = cnt_by_page)
summary(model)

plot(cnt_by_page$date, cnt_by_page$sum_mentions)

# consider the same model, but only including foreign placenames over time
model <- lm(foreign_mentions ~ date + Page + frontPage + Sun + pagesFromEnd + frontPage*date, data = cnt_by_page)
summary(model)

plot(cnt_by_page$date, cnt_by_page$foreign_mentions)

# consider the ratio
model <- lm(foreign_ratio ~ date + Page + frontPage + Sun + pagesFromEnd + frontPage*date, data = cnt_by_page)
summary(model)

plot(cnt_by_page$date, cnt_by_page$foreign_ratio)

# plot the predictions of a polynomial regression

model <- lm(foreign_ratio ~ poly(date,3) + frontPage*date + Sun + nPage, data = cnt_by_page)
summary(model)

prediction_vals = data.frame(date=c(0:20),
                             Sun=mean(cnt_by_page$Sun),
                             Page=mean(cnt_by_page$Page),
                             nPage=mean(cnt_by_page$nPage),
                             frontPage= mean(cnt_by_page$frontPage),
                             pagesFromEnd=mean(cnt_by_page$pagesFromEnd))

predicted.intervals <- predict(model,prediction_vals,interval='confidence',
                               level=0.99)

plot(cnt_by_page$date, cnt_by_page$foreign_ratio,
     ylab ="Foreign/Domestic Placename Ratio",
     xlab="Years since 1900")
lines(c(0:20),predicted.intervals[,1],col='firebrick1',lwd=3)
lines(c(0:20),predicted.intervals[,2],col='deepskyblue4',lwd=3)
lines(c(0:20),predicted.intervals[,3],col='deepskyblue4',lwd=3)





# FRONT PAGE GRAPH
library(tidyverse)
# filter to only include front page news
front_pages <- filter(cnt_by_page, Page == 1)

model <- lm(foreign_ratio ~ poly(date,3) + Sun + nPage, data = front_pages)
summary(model)

prediction_vals = data.frame(date=c(0:20),
                             Sun= mean(front_pages$Sun),
                             nPage= mean(front_pages$nPage))

predicted.intervals <- predict(model,prediction_vals,interval='confidence',
                               level=0.99)

plot(front_pages$date, front_pages$foreign_ratio,
     ylab ="Foreign/domestic placename ratio",
     xlab="Years since 1900")
lines(c(0:20),predicted.intervals[,1],col='firebrick1',lwd=3)
lines(c(0:20),predicted.intervals[,2],col='deepskyblue4',lwd=3)
lines(c(0:20),predicted.intervals[,3],col='deepskyblue4',lwd=3)




# PRE 1914

cutoff = 14.35

# filter to only include front page news prior to 1914
front_pages_pre <- filter(cnt_by_page, Page == 1, date < cutoff)

model <- lm(foreign_ratio ~ poly(date,3) + Sun + nPage, data = front_pages_pre)
summary(model)

xrng <- c(0:floor(cutoff),cutoff)
prediction_vals_pre = data.frame(date=xrng,
                             Sun= mean(front_pages_pre$Sun),
                             nPage= mean(front_pages_pre$nPage))

predicted.intervals_pre <- predict(model,prediction_vals_pre,interval='confidence',
                               level=0.99)


plot(front_pages$date, front_pages$foreign_ratio,
     ylab ="Foreign/domestic placename ratio",
     xlab="Years since 1900")
lines(xrng,predicted.intervals_pre[,1],col='firebrick1',lwd=3)
lines(xrng,predicted.intervals_pre[,2],col='deepskyblue4',lwd=3)
lines(xrng,predicted.intervals_pre[,3],col='deepskyblue4',lwd=3)

# POST 1914

# filter to only include front page news post 1914
front_pages_post <- filter(cnt_by_page, Page == 1, date >= 14)

model <- lm(foreign_ratio ~ poly(date,3) + Sun + nPage, data = front_pages_post)
summary(model)

xrng <- c(cutoff,ceiling(cutoff):20)
prediction_vals_post = data.frame(date=xrng,
                             Sun= mean(front_pages_post$Sun),
                             nPage= mean(front_pages_post$nPage))

predicted.intervals_post <- predict(model,prediction_vals_post,interval='confidence',
                               level=0.99)

lines(xrng,predicted.intervals_post[,1],col='firebrick1',lwd=3)
lines(xrng,predicted.intervals_post[,2],col='deepskyblue4',lwd=3)
lines(xrng,predicted.intervals_post[,3],col='deepskyblue4',lwd=3)






# try with all pages
# PRE 1914

cutoff = 14.3

# filter to only include news prior to 1914
front_pages_pre <- filter(cnt_by_page, date < cutoff)

model <- lm(foreign_ratio ~ poly(date,3) + Sun + nPage, data = front_pages_pre)
summary(model)

xrng <- c(0:floor(cutoff),cutoff)
prediction_vals_pre = data.frame(date=xrng,
                                 Sun= mean(front_pages_pre$Sun),
                                 nPage= mean(front_pages_pre$nPage))

predicted.intervals_pre <- predict(model,prediction_vals_pre,interval='confidence',
                                   level=0.99)


plot(cnt_by_page$date, cnt_by_page$foreign_ratio,
     ylab ="Foreign/domestic placename ratio",
     xlab="Years since 1900")
lines(xrng,predicted.intervals_pre[,1],col='firebrick1',lwd=3)
lines(xrng,predicted.intervals_pre[,2],col='deepskyblue4',lwd=3)
lines(xrng,predicted.intervals_pre[,3],col='deepskyblue4',lwd=3)

# POST 1914

# filter to only include news post 1914
front_pages_post <- filter(front_pages, date >= 14)

model <- lm(foreign_ratio ~ poly(date,3) + Sun + nPage, data = front_pages_post)
summary(model)

xrng <- c(cutoff,ceiling(cutoff):20)
prediction_vals_post = data.frame(date=xrng,
                                  Sun= mean(front_pages_post$Sun),
                                  nPage= mean(front_pages_post$nPage))

predicted.intervals_post <- predict(model,prediction_vals_post,interval='confidence',
                                    level=0.99)

plot(front_pages_post$date, front_pages_post$foreign_ratio,
     ylab ="Foreign/domestic placename ratio",
     xlab="Years since 1900")

lines(xrng,predicted.intervals_post[,1],col='firebrick1',lwd=3)
lines(xrng,predicted.intervals_post[,2],col='deepskyblue4',lwd=3)
lines(xrng,predicted.intervals_post[,3],col='deepskyblue4',lwd=3)





# group front pages by year
by_year <- data.frame(matrix(ncol = 250, nrow = 0),stringsAsFactors = FALSE)
names(by_year) <- c(c('Year'),names(cnt_by_page)[13:261])

top_10 <- data.frame(matrix(ncol = 11, nrow = 0),stringsAsFactors = FALSE)
names(top_10) <- c(c('Year'),c(1:10))

for (y in 1900:1919) {
  pages_in_year <- filter(cnt_by_page, Year == y)
  
  x <- c()
  names(x) <- c()
  
  x <- c(y,colSums(pages_in_year[,13:261]))
  names(x) <- c(c('Year'),names(pages_in_year)[13:261])
  
  by_year <- rbind(by_year,x)
  
  top <- c(c(y),names(sort(x[2:length(x)],decreasing=TRUE)[0:10]))
  names(top) <- c(c('Year'),c(1:10))
  
  top_10 <- rbind(top_10,top,stringsAsFactors = FALSE)
  names(top_10) <-c(c('Year'),c(1:10))
}


# limited to front page
# group front pages by year
by_year <- data.frame(matrix(ncol = 250, nrow = 0),stringsAsFactors = FALSE)
names(by_year) <- c(c('Year'),names(front_pages)[13:261])

top_10_front <- data.frame(matrix(ncol = 11, nrow = 0),stringsAsFactors = FALSE)
names(top_10) <- c(c('Year'),c(1:10))

for (y in 1900:1919) {
  pages_in_year <- filter(front_pages, Page == 1, Year == y)
  
  x <- c()
  names(x) <- c()
  
  x <- c(y,colSums(pages_in_year[,13:261]))
  names(x) <- c(c('Year'),names(pages_in_year)[13:261])
  
  by_year <- rbind(by_year,x)
  
  top <- c(c(y),names(sort(x[2:length(x)],decreasing=TRUE)[0:10]))
  names(top) <- c(c('Year'),c(1:10))
  
  top_10_front <- rbind(top_10_front,top,stringsAsFactors = FALSE)
  names(top_10_front) <-c(c('Year'),c(1:10))
}


