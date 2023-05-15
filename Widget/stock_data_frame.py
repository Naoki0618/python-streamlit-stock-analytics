import yfinance as yf
import pandas as pd
import streamlit as st
from API.bs4_stock_data import BsStockData


# 株式情報からデータフレームを作成する
class StockDataFrame:

    # データフレームを作成
    def __init__(self, tickers_info):

        self.df = pd.DataFrame(
            columns=['証券コード', '社名', '時価総額(千万)', '現在株価', '目標株価', 'PER', 'PBR', 'ROE', '配当利回', '借入率', 'A評価', '信用倍率', 'is_widget']
            )

        self.tickers_info = tickers_info
        self.create_data()

    def create_data(self):

        for ticker in self.tickers_info:
            try:
                marketCap = str(round(ticker.info.get('marketCap', 'N/A') / 10000000, 0))
            except Exception as e:
                print(e)
                marketCap = 'N/A'
            try:
                trailingPE = round(ticker.info.get('trailingPE', 'N/A'), 2)
            except Exception as e:
                print(e)
                trailingPE = 'N/A'
            try:
                forwardPE = round(ticker.info.get('forwardPE', 'N/A'), 2)
            except Exception as e:
                print(e)
                forwardPE = 'N/A'
            try:
                priceToBook = round(ticker.info.get('priceToBook', 'N/A'), 2)
            except Exception as e:
                print(e)
                priceToBook = 'N/A'
            try:
                returnOnEquity = str(round(ticker.info.get('returnOnEquity', 'N/A')*100, 2)) + '%'
            except Exception as e:
                print(e)
                returnOnEquity = 'N/A'
            try:
                trailing_annual_dividend_yield = ticker.info.get(
                    'trailingAnnualDividendYield')
                if trailing_annual_dividend_yield is not None:
                    dividend_payout_ratio = round(
                        trailing_annual_dividend_yield * 100, 2)
                else:
                    print(e)
                    dividend_payout_ratio = 'N/A'
            except Exception as e:
                print(e)
                dividend_payout_ratio = 'N/A'

            try:    
                recommendationMean = ticker.info.get("recommendationMean")
            except Exception as e:
                print(e)
                recommendationMean = 'N/A'

            try:    
                symbol = ticker.info.get('symbol', 'N/A').replace(".T", "")
            except Exception as e:
                print(e)
                symbol = 'N/A'
            try:
                credit_ratio = BsStockData.scrape_website(symbol)
            except Exception as e:
                print(e)
                credit_ratio = 'N/A'
                
            try:
                stock_data = {
                    '証券コード': symbol,
                    '社名': ticker.info.get('longName', 'N/A'),
                    '時価総額(千万)': marketCap,
                    '現在株価': ticker.info.get('currentPrice', 'N/A'),
                    '目標株価': ticker.info.get('targetMeanPrice', 'N/A'),
                    'PER': trailingPE,
                    'PBR': priceToBook,
                    'ROE': returnOnEquity,
                    '配当利回': dividend_payout_ratio,
                    '借入率': ticker.info.get('debtToEquity', 'N/A'),
                    'A評価': recommendationMean,
                    '信用倍率': credit_ratio,
                    'is_widget': True
                }
                new_row = pd.Series({
                    "証券コード": stock_data['証券コード'],
                    "社名": stock_data['社名'],
                    "時価総額(千万)": stock_data['時価総額(千万)'],
                    "現在株価": stock_data['現在株価'],
                    "目標株価": stock_data['目標株価'],
                    "PER": stock_data['PER'],
                    "PBR": stock_data['PBR'],
                    "ROE": stock_data['ROE'],
                    "配当利回": stock_data['配当利回'],
                    "借入率": stock_data['借入率'],
                    "A評価": stock_data['A評価'],
                    "信用倍率": stock_data['信用倍率'],
                    'is_widget': True})
                self.df = self.df.append(
                    new_row, ignore_index=True)
            except Exception as e:
                print(e)

    # インスタンス情報をもとにデータフレームを表示
    def display_dataframe(self):

        edited_df = st.experimental_data_editor(self.df)

        # データエディターで編集された値を取得する
        edited_df_dict = edited_df.to_dict(orient='records')
        # 編集後の値を select_symbols_df に反映する
        self.df = pd.DataFrame.from_records(edited_df_dict)

        # st.session_state.cstock = self.df

    def all_false_widget(self):
        # edited_df = st.experimental_data_editor(self.df)
        
        edited_df_dict = st.experimental_data_editor(self.df)

        # データエディターで編集された値を取得する
        # edited_df_dict['is_widget'] = False
        edited_df_dict = edited_df_dict.to_dict(orient='records')
        # 編集後の値を select_symbols_df に反映する
        self.df = pd.DataFrame.from_records(edited_df_dict)
        

    def change_dataframe(self):
        # データエディターで編集された値を取得する
        edited_df_dict = edited_df.to_dict(orient='records')
        # 編集後の値を select_symbols_df に反映する
        self.df = pd.DataFrame.from_records(edited_df_dict)

    def get_info(self, value):
        return self.df[value]

    def get_info_all(self, value):
        return self.df
