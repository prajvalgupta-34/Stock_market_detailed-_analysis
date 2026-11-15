import streamlit as st
import pandas as pd

st.set_page_config(page_title="Quant Stock ETL", layout="wide")
st.title("📈 Automated Quant Stock Data Pipeline")
st.write("Live data feed from the automated ETL pipeline (GitHub Actions CI/CD).")

try:
    df = pd.read_csv("cleaned_stock_data.csv")
    
    # --- UPGRADE 1: Interactive Ticker Selection ---
    st.subheader("Data Warehouse Preview")
    
    # Dropdown to filter data
    tickers = df['Ticker'].unique()
    selected_tickers = st.multiselect("Select Tickers to analyze:", options=tickers, default=tickers)
    
    # Filter dataframe based on selection and sort by newest dates
    filtered_df = df[df['Ticker'].isin(selected_tickers)]
    st.dataframe(filtered_df.sort_values(by='Date', ascending=False).head(20))
    
    # --- UPGRADE 2: Advanced Quant Metrics Visualization ---
    st.subheader("Quantitative Risk & Return Analytics")
    
    # Radio buttons to switch between basic and advanced metrics
    metric = st.radio(
        "Select Metric to Visualize on Y-Axis:", 
        ["Cumulative_Return", "Drawdown_Pct", "Close"],
        horizontal=True
    )
    
    st.line_chart(data=filtered_df, x="Date", y=metric, color="Ticker")
    
except FileNotFoundError:
    st.warning("Pipeline is syncing data. Please wait for the next CRON job.")