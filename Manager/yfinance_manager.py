import yfinance as yf
import streamlit as st
import pandas as pd


class YfinanceManager:

    # 銘柄情報を取得
    def __init__(self, ticker):
        self.ticker = ticker
        if ticker.isalpha():
            stock = yf.Ticker(ticker)
        else:
            stock = yf.Ticker(ticker + ".T")

        self.info = stock.info

    # 銘柄のセクター、価格等を表示
    def display_info(self):

        st.write(self.info.get("longName"))

        st.divider()

        st.subheader(':blue[セクター情報]')
        info_col1, info_col2 = st.columns(2)
        with info_col1:
            st.caption('industry')
            st.write(self.info['industry'])
        with info_col2:
            st.caption('sector')
            st.write(self.info['sector'])

        st.divider()

        # 株価情報を表示
        st.subheader(':blue[株価情報]')
        info_col1, info_col2, info_col3 = st.columns(3)
        finish_value = self.info['regularMarketPreviousClose']
        open_value = self.info['regularMarketOpen']
        high_value = self.info['dayHigh']
        low_value = self.info['dayLow']
        with info_col1:
            st.metric("始値", open_value, open_value - finish_value)
        with info_col2:
            st.metric("高値", high_value, high_value - finish_value)
        with info_col3:
            st.metric("安値", low_value, low_value - finish_value)

        try:
            st.write('配当金')
            st.write(self.info['dividendRate'])
        except:
            pass
