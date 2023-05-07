import yfinance as yf
import pandas as pd


class FinanceData:

    def __init__(self, tickers):
        self.tickers = tickers
        self.tickers_info = []
        for company in self.tickers:

            try:
                if company.isalpha():
                    tkr = yf.Ticker(company)
                else:
                    tkr = yf.Ticker(company + ".T")
                self.tickers_info.append(tkr)
            except:
                st.error(company + 'は何かしらの情報を取得できません', icon="🚨")


    def get_data(self, months, column, flg, ddd):
        df = pd.DataFrame()
        for tkr in self.tickers_info:
            
            if ddd == "day":
                hist = tkr.history(period=f'{months}d')
            elif ddd == "month":
                hist = tkr.history(period=f'{months}mo')
            else:
                hist = tkr.history(period=f'{months}y')

            hist = hist[[column]]
            hist.columns = [tkr.ticker.replace(".T","")]
            hist = hist.T
            hist.index.name = 'Name'
            hist['Company'] = tkr.info['longName']  # 企業名をカラムに追加する
            hist = hist.set_index('Company', append=True)  # 企業名をインデックスに移動する
            df = pd.concat([df, hist])

        if flg == 1:
            # 列ラベルから日付部分を抽出
            dates = df.columns.to_list()
            dates = [pd.to_datetime(date).date() for date in dates]

            # 列ラベルを日付に変更
            df.columns = dates

        return df

    def all_get_data(self, months, tickers):
        df = pd.DataFrame()
        for company in tickers:
            tkr = yf.Ticker(company + ".T")
            hist = tkr.history(period=f'{months}mo')
            hist['Company'] = tkr.info['longName']  # 企業名をカラムに追加する
            hist = hist.set_index(['Company', hist.index]
                                  )  # 企業名と日付をインデックスに移動する
            df = pd.concat([df, hist])

        return df

    def remove_all_zero_col(self, df):
        """全て0の列を削除"""
        df = df.copy()
        for col in df.columns:
            if (df[col] == 0).all():
                df.drop(col, axis=1, inplace=True)
        return df
