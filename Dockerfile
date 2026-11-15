# Base Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY data_ingestion.py .

# Install required libraries
RUN pip install yfinance pandas sqlalchemy pymysql

# Command to run the ETL script
CMD ["python", "data_ingestion.py"]