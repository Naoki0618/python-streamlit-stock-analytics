import yfinance as yf
import pandas as pd
import streamlit as st


# 株式情報からデータフレームを作成する
class StockDataFrame:

    # ヘッダーのみ作成
    def __init__(self):

        self.df = pd.DataFrame(
            columns=['証券コード', '社名', '時価総額', '現在株価', '目標株価', 'PER', 'PBR', '配当利回', '資本比率', 'MS評価', 'is_widget']
            )

        self.chart_df = []

    def add_data(self, sss):

        if sss.isalpha():
            stock = yf.Ticker(sss)
        else:
            stock = yf.Ticker(sss + ".T")

        info = stock.info
        try:
            marketCap = round(info.get('marketCap', 'N/A') / 1000000, 0)
        except:
            marketCap = 'N/A'
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
            '時価総額': marketCap,
            '現在株価': info.get('currentPrice', 'N/A'),
            '目標株価': info.get('targetMeanPrice', 'N/A'),
            'PER': trailingPE,
            'PBR': priceToBook,
            '配当利回': dividend_payout_ratio,
            '資本比率': info.get('debtToEquity', 'N/A'),
            'MS評価': info.get('industry', 'N/A'),
            'is_widget': True
        }
        new_row = pd.Series({
            "証券コード": stock_data['証券コード'],
            "社名": stock_data['社名'],
            "時価総額": stock_data['時価総額'],
            "現在株価": stock_data['現在株価'],
            "目標株価": stock_data['目標株価'],
            "PER": stock_data['PER'],
            "PBR": stock_data['PBR'],
            "配当利回": stock_data['配当利回'],
            "資本比率": stock_data['資本比率'],
            "MS評価": stock_data['MS評価'],
            'is_widget': True})
        self.df = self.df.append(
            new_row, ignore_index=True)

    # インスタンス情報をもとにデータフレームを表示
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
