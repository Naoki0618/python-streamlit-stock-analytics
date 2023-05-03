from yahooquery import Ticker


class ValuationMeasures():

    def get_valuation_measures(symbols):

        subsets = []
        for symbol in symbols:
            # yahooqueryでTickerオブジェクトを作成
            sy = Ticker(symbol + ".T")

            # 財務諸表を取得
            valuation_measures = sy.valuation_measures

            # 行と列を入れ替えたDataFrameを作成
            valuation_measures_t = valuation_measures.T
            #
            # 目的の列のみを抽出
            subset_v = valuation_measures_t.loc[[
                'asOfDate', 'PbRatio', 'PeRatio']]

            subset_v_t = subset_v.T
            subset_v_t['symbol'] = symbol  # 証券コードを列 'symbol' に追加
            subsets.append(subset_v_t)

        return subsets
