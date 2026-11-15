import streamlit as st
import pandas as pd

st.set_page_config(page_title="Quant Stock ETL", layout="wide")
st.title("📈 Automated Quant Stock Data Pipeline")
st.write("Live data feed from the automated ETL pipeline (GitHub Actions CI/CD).")

try:
    df = pd.read_csv("cleaned_stock_data.csv")
    
    st.subheader("Data Warehouse Preview (Latest Records)")
    st.dataframe(df.tail(15))
    
    st.subheader("Closing Price Trend")
    st.line_chart(data=df, x="Date", y="Close", color="Ticker")
    
except FileNotFoundError:
    st.warning("Pipeline is syncing data. Please wait for the next CRON job.")