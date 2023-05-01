import yfinance as yf
import pandas as pd


class FinanceData():

    def get_data(months, tickers, column, flg):
        df = pd.DataFrame()
        for company in tickers:
            tkr = yf.Ticker(company + ".T")
            hist = tkr.history(period=f'{months}mo')
            hist = hist[[column]]
            hist.columns = [company]
            hist = hist.T
            hist.index.name = 'Name'
            df = pd.concat([df, hist])

        if flg == 1:
            # 列ラベルから日付部分を抽出
            dates = df.columns.to_list()
            dates = [pd.to_datetime(date).date() for date in dates]

            # 列ラベルを日付に変更
            df.columns = dates

        return df
