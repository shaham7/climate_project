library(forecast)
library(prophet)
library(tidyverse)
library(tseries)

data <- read.csv("processed_data.csv")

analyze_climate_timeseries <- function(data, target_col, country) {
  
  # filter data by country
  country_data <- data %>%
    filter(Country == country) %>%
    arrange(Year)
  
  # create time series data
  ts_data <- ts(country_data[[target_col]], start = min(country_data$Year), frequency = 1)
  
  # create ARIMA model
  arima_model <- auto.arima(ts_data, seasonal = FALSE, stepwise = TRUE, approximation = FALSE)
  
  # generate forecasts
  forecast_periods <- 12
  arima_forecast <- forecast(arima_model, h = forecast_periods)
  
  # prepare prophet data, strict with format
  prophet_data <- data.frame(ds = as.Date(paste0(country_data$Year, "-01-01")), y = country_data[[target_col]])
  
  # create prophet model
  prophet_model <- prophet(prophet_data)
  future_dates <- make_future_dataframe(prophet_model, periods = forecast_periods, freq = "year")
  prophet_forecast <- predict(prophet_model, future_dates)
  
  return(list(
    arima_model = arima_model,
    arima_forecast = arima_forecast,
    prophet_model = prophet_model,
    prophet_forecast = prophet_forecast
  ))
}

#results <- analyze_climate_timeseries(data, "GDP_per_capita", "China")

calculate_forecast_metrics <- function(actual, predicted) {
  rmse <- sqrt(mean((actual - predicted)^2))
  mae <- mean(abs(actual - predicted))
  mape <- mean(abs((actual - predicted)/actual)) * 100
  
  return(data.frame(
    RMSE = rmse,
    MAE = mae,
    MAPE = mape
  ))
}


create_ts_plots <- function(analysis_results, country, target_col, forecast_end_year) {
  
  # ARIMA forecast
  forecast_data <- data.frame(
    Year = time(analysis_results$arima_forecast$mean),
    Forecast = as.vector(analysis_results$arima_forecast$mean),
    Lower = as.vector(analysis_results$arima_forecast$lower[, 2]),
    Upper = as.vector(analysis_results$arima_forecast$upper[, 2])
  )
  
  arima_forecast_plot <- ggplot(forecast_data, aes(x = Year)) +
    geom_line(aes(y = Forecast), color = "blue") +
    geom_ribbon(aes(ymin = Lower, ymax = Upper), alpha = 0.2, fill = "lightblue") +
    theme_minimal() +
    ggtitle(paste("ARIMA Forecast of", target_col, "for", country, "(Until", forecast_end_year, ")")) +
    labs(y = "Value", x = "Year") +
    theme(
      plot.title = element_text(face = "bold", size = 14, hjust = 0.5),
      axis.title.x = element_text(size = 12, face = "bold"),
      axis.title.y = element_text(size = 12, face = "bold"),
      axis.text = element_text(size = 10)
    )
  
  # prophet forecast
  prophet_forecast_data <- analysis_results$prophet_forecast
  prophet_forecast_data$ds <- as.Date(prophet_forecast_data$ds)
  years_to_highlight <- as.Date(c("2025-01-01", "2030-01-01", "2035-01-01"))
  
  prophet_plot <- ggplot(prophet_forecast_data, aes(x = ds)) +
    geom_line(aes(y = yhat), color = "red") +
    geom_ribbon(aes(ymin = yhat_lower, ymax = yhat_upper), alpha = 0.2, fill = "pink") +
    geom_point(data = prophet_forecast_data %>% filter(ds %in% years_to_highlight),
               aes(y = yhat), color = "darkred", size = 2) +
    geom_text(data = prophet_forecast_data %>% filter(ds %in% years_to_highlight),
              aes(y = yhat, label = round(yhat, 2)),
              hjust = -0.2, vjust = 0.5, size = 3, color = "black") +
    theme_minimal() +
    ggtitle(paste("Prophet Forecast of", target_col, "for", country, "(Until", forecast_end_year, ")")) +
    labs(y = "Value", x = "Year") +
    theme(
      plot.title = element_text(face = "bold", size = 14, hjust = 0.5),
      axis.title.x = element_text(size = 12, face = "bold"),
      axis.title.y = element_text(size = 12, face = "bold"),
      axis.text = element_text(size = 10)
    ) +
    scale_x_date(date_breaks = "10 years", date_labels = "%Y")
  
  return(list(
    arima_forecast_plot = arima_forecast_plot,
    prophet_forecast_plot = prophet_plot
  ))
}


generate_forecast_plot <- function(data, target_col, country, forecast_periods = 12) {

  analysis_results <- analyze_climate_timeseries(data, target_col, country)
  last_year <- max(as.numeric(format(analysis_results$prophet_forecast$ds, "%Y")))

  plots <- create_ts_plots(analysis_results, country, target_col, last_year)
  
  return(plots)
}

results <- generate_forecast_plot(data, "Global_Temperature", "World")
print(results)
