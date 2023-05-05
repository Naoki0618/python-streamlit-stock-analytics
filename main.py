import streamlit as st
import yfinance as yf
import pandas as pd
from yahooquery import Ticker
import plotly.graph_objs as go
import csv
import os
import altair as alt
import numpy as np
import pandas as pd
import locale

from API.yahoo_query import YahooQuery
from API.finance_data import FinanceData
from Manager.favorite_manager import FavoriteManager
from Manager.yfinance_manager import YfinanceManager
from Widget.stock_chart import StockAltairChart, StockAltairChartSimple
from Widget.stock_data_frame import StockDataFrame



@st.cache_data
def get_symbols():
    with open(os.getcwd() + u'/Data/value_list.txt', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        symbols = [row[0] for row in reader]

    return symbols


# ページの幅を1200ピクセルに設定
st.set_page_config(layout="wide")

# ロケールを設定する（日本語を指定）
locale.setlocale(locale.LC_NUMERIC, 'ja_JP')

### data ###################################################################

# 株価リストを取得
symbols = get_symbols()
symbols = [""] + symbols

### Sidebar ###################################################################
main, favorite = st.sidebar.tabs(["main", "favorite"])

with main:
    # mainタブの処理
    ticker = st.selectbox(
        'Please select a stock symbol',
        symbols,
    )

    if ticker != "":

        cticker = YfinanceManager(ticker)
        cticker.display_info()

with favorite:
    file_path = os.getcwd() + "/Data/favorites.csv"

    # 1. CSVファイルからお気に入り情報を読み込む
    favorites_df = FavoriteManager.load_favorites(file_path)
    favorites = FavoriteManager.parse_favorites(favorites_df)

    # 2. お気に入り情報を編集する
    favorites = FavoriteManager.edit_favorites(favorites)

    if favorites != None:
        # 3. お気に入り情報を更新する
        FavoriteManager.update_favorites(favorites, file_path)

    # 4. お気に入りを呼び出す
    if favorites != None:
        selected_codes = FavoriteManager.select_favorites(favorites)

    # 5. 結果を表示する
    st.write("Selected Securities:", selected_codes)

### Main ######################################################################
options_multiselect = []
if 'prev_tickers' not in st.session_state:
    st.session_state.prev_tickers = []

if 'tickers' not in st.session_state:
    st.session_state.tickers = []

if ticker not in st.session_state.tickers:
    st.session_state.tickers.append(ticker)

if len(selected_codes) != 0:
    for code in selected_codes:
        if not code in st.session_state.tickers:
            st.session_state.tickers.append(code)

# options_multiselectに含まれるtickerを更新するために、
# 新しいリストを作成してからoptions_multiselectを更新する
selected_tickers = st.session_state.tickers.copy()
if ticker not in selected_tickers:
    selected_tickers.append(ticker)
if st.session_state.tickers[0] == '' and len(st.session_state.tickers) == 1:
    options_multiselect = st.multiselect(
        'Selected stock symbols',
        symbols,
        key='color_multiselect'
        )

else:
    selected_tickers = [x for x in selected_tickers if x != '']
    options_multiselect = st.multiselect(
        'Selected stock symbols',
        symbols,
        selected_tickers,
        key='color_multiselect'
    )

# options_multiselectから選択されなくなったtickerを削除する
unselected_tickers = set(st.session_state.tickers) - set(options_multiselect)
if unselected_tickers:
    for unselected_ticker in unselected_tickers:
        st.session_state.tickers.remove(unselected_ticker)

Cstock_df = StockDataFrame()

# 新しい行を作成し、データフレームに追加する
for sss in options_multiselect:
    try:
        Cstock_df.add_data(sss)
    except Exception as e:
        print(e)
        st.error(sss + 'は何かしらの情報を取得できません', icon="🚨")

Cstock_df.display_dataframe()

try:

    st.divider()
    # info_col1, info_col2 = st.columns(2)
    # with info_col1:
    months = st.slider(':blue[月数]', 1, 100, 2)
    # with info_col2:
        # ymin, ymax = st.slider(':blue[株価範囲]', 0.0, 10000.0, (1000.0, 5000.0))

    # 株価のグラフを表示　##################################
    tickers = Cstock_df.get_info('証券コード')
    is_widget = Cstock_df.get_info('is_widget')

    #　チェックボックスがONのものだけを抽出
    tickers = [tickers[i] for i in range(len(tickers)) if is_widget[i]]

    # 初期データ
    Ctickers_data = FinanceData(tickers)
    tickers_close_value = Ctickers_data.get_data(months, "Close", 0)
    tickers_volume_value = Ctickers_data.get_data(months, "Volume", 0)
    
    tickers_close_value = tickers_close_value.loc[tickers]
    tickers_volume_value = tickers_volume_value.loc[tickers]

    # データの整形
    tickers_close_value = tickers_close_value.T.reset_index()
    tickers_close_value = pd.melt(tickers_close_value, id_vars=['Date']).rename(
        columns={'value': 'Close', 'variable': 'Name'}
    )
    tickers_volume_value = tickers_volume_value.T.reset_index()
    tickers_volume_value = pd.melt(tickers_volume_value, id_vars=['Date']).rename(
        columns={'value': 'Volume', 'variable': 'Name'}
    )

    color_scale = alt.Scale(range=["#003f5c", "#bc5090", "#ffa600"])

    chart_close = StockAltairChart(data=tickers_close_value, x="Date", y="Close", color="Name", title="Value Chart")
    chart_volume = StockAltairChart(data=tickers_volume_value, x="Date", y="Volume", color="Name", title="Volume Chart")

    info_col1, info_col2 = st.columns(2)
    with info_col1:
        st.subheader(":blue[Value Chart]")
        chart_close.display_chart()
    with info_col2:
        st.subheader(":blue[Volume Chart]")
        chart_volume.display_chart()
    
    CyahooQuery = YahooQuery(tickers)
    subsets_vm = CyahooQuery.get_valuation_measures()
    subsets_is = CyahooQuery.get_income_statement()

    charts_pbr = StockAltairChartSimple()
    charts_per = StockAltairChartSimple()
    charts_revenue = StockAltairChartSimple()
    charts_income = StockAltairChartSimple()
    
    for subset in subsets_vm:
        try:
            charts_pbr.add_chart(subset, "PbRatio")
        except:
            pass
        try:
            charts_per.add_chart(subset, "PeRatio")
        except:
            pass
    for subset in subsets_is:
        charts_revenue.add_bar_chart(subset, "TotalRevenue")
        try:
            charts_income.add_bar_chart(subset, "TotalOperatingIncomeAsReported")
        except:
            pass

    info_col1, info_col2 = st.columns(2)
    with info_col1:
        st.subheader(":blue[PBR]")
        charts_pbr.display_chart()
    with info_col2:
        st.subheader(":blue[PER]")
        try:
            charts_per.display_chart()
        except:
            pass    
    
    info_col1, info_col2 = st.columns(2)
    with info_col1:
        st.subheader(":blue[売上高]")
        charts_revenue.display_chart()
    with info_col2:
        st.subheader(":blue[営業利益]")
        charts_income.display_chart()

    data_income = Ctickers_data.get_data(months, "Dividends", 1)
    data_income = Ctickers_data.remove_all_zero_col(data_income)
    st.write("### :blue[配当実績]", data_income.sort_index())

except Exception as e:
    print("****************************************************")
    print(e)
    print("****************************************************")
    st.stop()
