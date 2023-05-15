from yahooquery import Ticker


class YahooQuery:

    def __init__(self, symbols):

        self.symbols_info = []
        for symbol in symbols:
            if symbol.isalpha():
                info = Ticker(symbol)
            else:
                info = Ticker(symbol + ".T")
            self.symbols_info.append(info)

    def get_valuation_measures(self):

        try:
            subsets = []
            for info in self.symbols_info:

                # 財務諸表を取得
                valuation_measures = info.valuation_measures

                # 行と列を入れ替えたDataFrameを作成
                valuation_measures_t = valuation_measures.T
                #
                # 目的の列のみを抽出
                try:
                    subset_v = valuation_measures_t.loc[[
                        'asOfDate', 'periodType', 'PbRatio', 'PeRatio', 'MarketCap']]
                except:
                    try:
                        subset_v = valuation_measures_t.loc[[
                            'asOfDate', 'periodType', 'PbRatio', 'MarketCap']]
                    except:
                        subset_v = valuation_measures_t.loc[[
                            'asOfDate', 'periodType', 'MarketCap']]


                subset_v_t = subset_v.T
                # subset_v_t = subset_v_t.loc[subset_v_t['periodType'] == '3M'].copy()
                subset_v_t['symbol'] = valuation_measures_t.columns[0].replace(".T","")  # 証券コードを列 'symbol' に追加
                subsets.append(subset_v_t)

        except Exception as e:
            print("get_valuation_measures")
            print(e)
        return subsets

    def get_income_statement(self):

        subsets = []
        try:
            for info in self.symbols_info:
                # yahooqueryでTickerオブジェクトを作成

                # 財務諸表を取得
                income_statement = info.income_statement()

                # 行と列を入れ替えたDataFrameを作成
                income_statement_t = income_statement.T
                #
                # 目的の列のみを抽出
                try:
                    subset_v = income_statement_t.loc[[
                        'asOfDate', 'periodType', 'TotalOperatingIncomeAsReported', 'TotalRevenue']]
                except:
                    subset_v = income_statement_t.loc[[
                        'asOfDate', 'periodType', 'TotalRevenue']]

                subset_v_t = subset_v.T
                # subset_v_t = subset_v_t.loc[subset_v_t['periodType'] == '12M'].copy()
                subset_v_t['symbol'] = income_statement_t.columns[0].replace(".T","")  # 証券コードを列 'symbol' に追加
                subsets.append(subset_v_t)

        except Exception as e:
            print("get_income_statement")
            print(e)  

        return subsets