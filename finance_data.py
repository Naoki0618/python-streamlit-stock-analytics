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
            hist['Company'] = tkr.info['longName'] # 企業名をカラムに追加する
            hist = hist.set_index('Company', append=True) # 企業名をインデックスに移動する
            df = pd.concat([df, hist])

        if flg == 1:
            # 列ラベルから日付部分を抽出
            dates = df.columns.to_list()
            dates = [pd.to_datetime(date).date() for date in dates]

            # 列ラベルを日付に変更
            df.columns = dates

        return df
            
    def all_get_data(months, tickers):
        df = pd.DataFrame()
        for company in tickers:
            tkr = yf.Ticker(company + ".T")
            hist = tkr.history(period=f'{months}mo')
            hist['Company'] = tkr.info['longName'] # 企業名をカラムに追加する
            hist = hist.set_index(['Company', hist.index]) # 企業名と日付をインデックスに移動する
            df = pd.concat([df, hist])

        return df