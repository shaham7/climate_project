library(forecast)
library(prophet)
library(tidyverse)
library(tseries)

data <- read.csv("processed_data.csv")
head(data)

country_data <- data %>%
  filter(Country == "China") %>%
  arrange(Year)

head(country_data)

ts_data <- ts(country_data$Emissions, 
              start = min(country_data$Year), 
              frequency = 1)
ts_data

plot(ts_data, main = "Time Series of Emissions (China)", ylab = "Emissions", xlab = "Year")

ma_3 <- ma(ts_data, order = 3)
ma_3
ma_5 <- ma(ts_data, order = 5)

plot(ts_data, main = "Original Time Series and 3-Year Moving Average")
lines(ma_3, col = "red")
lines(ma_5, col = "blue")

arima_model <- auto.arima(ts_data, seasonal = FALSE, stepwise = TRUE, approximation = FALSE, trace = TRUE)
summary(arima_model)
