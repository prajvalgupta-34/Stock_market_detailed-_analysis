import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
import datetime

# 1. Extract: Fetch data for top tech stocks
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=730) # Last 2 years

df_list = []
for ticker in tickers:
    # Using Ticker().history() as it is more stable against yfinance updates
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date)
    
    # Keep only the essential columns
    data = data[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
    data['Ticker'] = ticker
    df_list.append(data)

# 2. Transform: Clean and format the dataset
df = pd.concat(df_list)
df.reset_index(inplace=True)

# Standardize column names (Now explicitly 7 columns)
df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Ticker']

# Remove timezone from Date to prevent MySQL errors later
df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize(None)

# Calculate daily return percentage
df.dropna(inplace=True)
df['Daily_Return_Pct'] = df.groupby('Ticker')['Close'].pct_change() * 100

# 3. Load: Push to MySQL Database or CSV
engine = create_engine('mysql+pymysql://root:password@localhost/stock_analytics')
try:
    df.to_sql('stock_prices', con=engine, if_exists='replace', index=False)
    print("ETL Pipeline Executed Successfully. Data loaded to MySQL.")
except Exception as e:
    print("Database connection skipped for GitHub representation. Saving to CSV instead.")
    df.to_csv('cleaned_stock_data.csv', index=False)
    print("Success! 'cleaned_stock_data.csv' has been generated.")