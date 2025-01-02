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

forecast_periods <- 10
arima_forecast <- forecast(arima_model, h = forecast_periods)
plot(arima_forecast)

prophet_data <- data.frame(
  ds = as.Date(paste0(country_data$Year, "-01-01")),
  y = country_data$Emissions
)
head(prophet_data)

prophet_model <- prophet(prophet_data)

future_dates <- make_future_dataframe(prophet_model, periods = forecast_periods, freq = "year")
future_dates

prophet_forecast <- predict(prophet_model, future_dates)

plot(prophet_model, prophet_forecast)

prophet_forecast


actual <- tail(prophet_data$y, forecast_periods)

predicted <- tail(prophet_forecast$yhat, forecast_periods)
predicted

calculate_forecast_metrics <- function(actual, predicted) {
  rmse <- sqrt(mean((actual - predicted)^2))
  mae <- mean(abs(actual - predicted))
  mape <- mean(abs((actual - predicted)/actual)) * 100
  return(data.frame(RMSE = rmse, MAE = mae, MAPE = mape))
}
calculate_forecast_metrics(actual, predicted)

