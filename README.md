# 📈 Automated Stock Market ETL & Advanced Analytics Pipeline

## 🎯 Project Overview
This project is an end-to-end Data Engineering and Analytics pipeline designed to extract real-time financial data, transform it using Python, analyze it using Advanced MySQL, and visualize the insights through an interactive Power BI dashboard. It demonstrates production-level database management, quantitative analysis, and business intelligence skills.

## 📊 Power BI Dashboard
![Power BI Dashboard](dashboard_preview.png)

## 🛠️ Tech Stack & Architecture
* **Data Ingestion & Transformation:** Python (`yfinance`, `pandas`, `SQLAlchemy`)
* **Database & Advanced Analytics:** MySQL (Window Functions, CTEs, Stored Procedures, Views)
* **Data Visualization & Business Intelligence:** Power BI (DAX, Interactive KPIs, Slicers)

## 💡 Key Features & Technical Implementations

### 1. Python ETL Pipeline (`data_ingestion.py`)
* Automatically extracts the last 2 years of historical stock data for top tech companies (AAPL, AMZN, GOOGL, MSFT) using the `yfinance` API.
* Performs data cleaning, handles missing values, and calculates the Daily Return Percentage.
* Connects to a local MySQL instance using `SQLAlchemy` to load the cleaned time-series data dynamically.

### 2. Advanced SQL Engineering (`advanced_analytics.sql`)
* **Window Functions:** Engineered 50-day and 200-day Simple Moving Averages (SMA) using `OVER`, `PARTITION BY`, and `ROWS BETWEEN` to identify technical breakout signals.
* **Common Table Expressions (CTEs):** Designed views to isolate and rank the top 5 best-performing trading days for each individual stock.
* **Stored Procedures:** Created automated routines to generate weekly price volatility and volume aggregation reports, utilizing `STDDEV()` and temporal grouping.

### 3. Power BI & DAX Integration (`Stock_Market_Dashboard.pbix`)
* **Custom DAX Measures:** Implemented dynamic calculations for:
  * `Total_Volume = SUM('cleaned_stock_data'[Volume])`
  * `Avg_Daily_Return = AVERAGE('cleaned_stock_data'[Daily_Return_Pct])`
  * `Max_Close_Price = MAX('cleaned_stock_data'[Close])`
  * `SMA_50 = CALCULATE(AVERAGE('cleaned_stock_data'[Close]), DATESINPERIOD('cleaned_stock_data'[Date], MAX('cleaned_stock_data'[Date]), -50, DAY))`
* **Interactive Visuals:** Built a dynamic KPI dashboard utilizing slicers for individual ticker analysis and time-series line charts for volatility and SMA crossover tracking.

## 🚀 How to Run Locally
1. Run `python data_ingestion.py` to fetch the latest market data and load it into your database (or generate a CSV fallback).
2. Execute `advanced_analytics.sql` in MySQL Workbench to generate the analytical views and stored procedures.
3. Open `Stock_Market_Dashboard.pbix` in Power BI Desktop to interact with the visualizations.