import yfinance as yf
import streamlit as st
import pandas as pd


class YfinanceManager:

    # 銘柄情報を取得
    def __init__(self, ticker):
        self.ticker = ticker
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

# 株式情報からデータフレームを作成する


class StockDataFrame:

    # 　ヘッダーのみ作成
    def __init__(self):

        self.df = pd.DataFrame(
            columns=['証券コード', '社名', 'マーケット', '時価総額', '予想PER', 'PER', 'PBR', '配当利回', "is_widget"])

    # 　要素追加
    def add_data(self, sss):

        stock = yf.Ticker(sss + ".T")
        info = stock.info
        try:
            trailingPE = round(info.get('trailingPE', 'N/A'), 2)
        except:
            trailingPE = 'N/A'
        try:
            forwardPE = round(info.get('forwardPE', 'N/A'), 2)
        except:
            forwardPE = 'N/A'
        try:
            priceToBook = round(info.get('priceToBook', 'N/A'), 2)
        except:
            priceToBook = 'N/A'
        try:
            trailing_annual_dividend_yield = info.get(
                'trailingAnnualDividendYield')
            if trailing_annual_dividend_yield is not None:
                dividend_payout_ratio = round(
                    trailing_annual_dividend_yield * 100, 2)
            else:
                dividend_payout_ratio = 'N/A'
        except:
            dividend_payout_ratio = 'N/A'

        stock_data = {
            '証券コード': sss,
            '社名': info.get('longName', 'N/A'),
            'マーケット': info.get('market', 'N/A'),
            '時価総額': info.get('marketCap', 'N/A'),
            '予想PER': forwardPE,
            'PER': trailingPE,
            'PBR': priceToBook,
            '配当利回': dividend_payout_ratio,
            "is_widget": True
        }
        new_row = pd.Series({
            "証券コード": stock_data['証券コード'],
            "社名": stock_data['社名'],
            "マーケット": stock_data['マーケット'],
            "時価総額": stock_data['時価総額'],
            "予想PER": stock_data['予想PER'],
            "PER": stock_data['PER'],
            "PBR": stock_data['PBR'],
            "配当利回": stock_data['配当利回'],
            "is_widget": True})
        self.df = self.df.append(
            new_row, ignore_index=True)

    # 　インスタンス情報をもとにデータフレームを表示
    def display_dataframe(self):

        edited_df = st.experimental_data_editor(self.df)

        # データエディターで編集された値を取得する
        edited_df_dict = edited_df.to_dict(orient='records')
        # 編集後の値を select_symbols_df に反映する
        self.df = pd.DataFrame.from_records(edited_df_dict)

    def get_info(self, value):
        return self.df[value]

    def get_info_all(self, value):
        return self.df