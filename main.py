import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

st.title("📊 Credit / Stock Risk Analysis Platform")

ticker = st.text_input("Enter stock ticker (example: RELIANCE.NS):", "RELIANCE.NS")

if ticker:
    data = yf.Ticker(ticker).history(period="1mo")
    st.write("### Stock Data (Last 5 rows)")
    st.write(data.tail())

    st.line_chart(data["Close"])

