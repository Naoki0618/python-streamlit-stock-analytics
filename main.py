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

from valuation_measures import ValuationMeasures as vm
from finance_data import FinanceData as fd
from file_operation import FileOperation as ff


@st.cache_data
def get_symbols():
    with open(os.getcwd() + u'/value_list.txt', newline='') as csvfile:
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
ticker = st.sidebar.selectbox(
    'Please select a stock symbol',
    symbols,
)

if ticker == "":
    st.stop()

stock = yf.Ticker(ticker + ".T")
info = stock.info
st.sidebar.write(info.get("longName"))

### Sidebar ###################################################################
if len(ticker) != 0:

    st.sidebar.divider()

    st.sidebar.subheader(':blue[セクター情報]')
    info_col1, info_col2 = st.sidebar.columns(2)
    with info_col1:
        st.sidebar.caption('industry')
        st.sidebar.write(stock.info['industry'])
    with info_col2:
        st.sidebar.caption('sector')
        st.sidebar.write(stock.info['sector'])

    st.sidebar.divider()
    # 株価情報を表示
    st.sidebar.subheader(':blue[株価情報]')
    info_col1, info_col2, info_col3 = st.sidebar.columns(3)
    finish_value = stock.info['regularMarketPreviousClose']
    open_value = stock.info['regularMarketOpen']
    high_value = stock.info['dayHigh']
    low_value = stock.info['dayLow']
    with info_col1:
        st.sidebar.metric("始値", open_value, open_value - finish_value)
    with info_col2:
        st.sidebar.metric("高値", high_value, high_value - finish_value)
    with info_col3:
        st.sidebar.metric("安値", low_value, low_value - finish_value)

    try:
        st.sidebar.write('配当金')
        st.sidebar.write(stock.info['dividendRate'])
    except:
        pass

else:
    st.write('株式コードが無効です。')

### Main ######################################################################
options_multiselect = []
if 'prev_tickers' not in st.session_state:
    st.session_state.prev_tickers = []

if 'tickers' not in st.session_state:
    st.session_state.tickers = []

if ticker not in st.session_state.tickers:
    st.session_state.tickers.append(ticker)

# options_multiselectに含まれるtickerを更新するために、
# 新しいリストを作成してからoptions_multiselectを更新する
selected_tickers = st.session_state.tickers.copy()
if ticker not in selected_tickers:
    selected_tickers.append(ticker)
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

select_symbols_df = pd.DataFrame(
    columns=['証券コード', '社名', '時価総額', '予想PER', 'PER', 'PBR', '配当性向', "is_widget"])


# 新しい行を作成し、データフレームに追加する
for sss in options_multiselect:
    try:
        stock = yf.Ticker(sss + ".T")
        info = stock.info

        try:
            trailingPE = round(info.get('trailingPE', 'N/A'), 2)
        except:
            trailingPE = 'N/A'
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
            '時価総額': info.get('marketCap', 'N/A'),
            '予想PER': round(info.get('forwardPE', 'N/A'), 2),
            'PER': trailingPE,
            'PBR': priceToBook,
            '配当性向': dividend_payout_ratio,
            "is_widget": True
        }
        new_row = pd.Series({"証券コード": stock_data['証券コード'], "社名": stock_data['社名'], "時価総額": stock_data['時価総額'], "予想PER": stock_data['予想PER'],
                            "PER": stock_data['PER'], "PBR": stock_data['PBR'], "配当性向": stock_data['配当性向'], "is_widget": True})
        select_symbols_df = select_symbols_df.append(
            new_row, ignore_index=True)
    except:
        st.error(sss + 'は何かしらの情報を取得できません', icon="🚨")

edited_df = st.experimental_data_editor(select_symbols_df)

# データエディターで編集された値を取得する
edited_df_dict = edited_df.to_dict(orient='records')
# 編集後の値を select_symbols_df に反映する
select_symbols_df = pd.DataFrame.from_records(edited_df_dict)

try:

    st.divider()
    info_col1, info_col2 = st.columns(2)
    with info_col1:
        months = st.slider(':blue[月数]', 1, 100, 2)
    with info_col2:
        ymin, ymax = st.slider(':blue[株価範囲]', 0.0, 10000.0, (1000.0, 5000.0))

    # 株価のグラフを表示
    tickers = select_symbols_df['証券コード']
    tickers_close_value = fd.get_data(months, tickers, "Close", 0)
    value_chart_data = tickers_close_value.loc[tickers]
    st.subheader(":blue[Value Chart]")

    # データの整形
    value_chart_data = value_chart_data.T.reset_index()
    value_chart_data = pd.melt(value_chart_data, id_vars=['Date']).rename(
        columns={'value': 'Prices(YEN)'}
    )

    color_scale = alt.Scale(range=["#003f5c", "#bc5090", "#ffa600"])
    chart = (
        alt.Chart(value_chart_data)
        .mark_line(opacity=0.8, clip=True)
        .encode(
            x="Date:T",
            y=alt.Y("Prices(YEN):Q", stack=None,
                    scale=alt.Scale(domain=[ymin, ymax])),
            color='Name:N',
        )
        .configure_axis(
            gridOpacity=0.2,
        )
        .configure_legend(
            titleFontSize=12,

            labelFontSize=11,
            symbolType="circle",
            symbolSize=100,
            padding=5,
            cornerRadius=5,
            strokeColor="gray",
            strokeWidth=1,
        )
    )

    st.altair_chart(chart.interactive(), use_container_width=True)

    subsets = vm.get_valuation_measures(tickers)
    charts_pbr = []
    charts_per = []
    for subset in subsets:
        chart_pbr = alt.Chart(subset).mark_line().encode(
            x='asOfDate',
            y=alt.Y('PbRatio', scale=alt.Scale(
                domain=[subset['PbRatio'].min()-0.1, subset['PbRatio'].max()+0.1])),
            color='symbol:N',  # 列 'symbol' をカラーに設定
            tooltip=['symbol', 'asOfDate', 'PbRatio']  # ツールチップに表示する列を指定
        )
        charts_pbr.append(chart_pbr)
        chart_per = alt.Chart(subset).mark_line().encode(
            x='asOfDate',
            y=alt.Y('PeRatio', scale=alt.Scale(
                domain=[subset['PeRatio'].min()-0.1, subset['PeRatio'].max()+0.1])),
            color='symbol:N',  # 列 'symbol' をカラーに設定
            tooltip=['symbol', 'asOfDate', 'PeRatio']  # ツールチップに表示する列を指定
        )
        charts_per.append(chart_per)
    info_col1, info_col2 = st.columns(2)
    with info_col1:
        st.subheader(":blue[PBR]")
        st.altair_chart(alt.layer(*charts_pbr), use_container_width=True)
    with info_col2:
        st.subheader(":blue[PER]")
        st.altair_chart(alt.layer(*charts_per), use_container_width=True)

    df_income = fd.get_data(months, tickers, "Dividends", 1)
    data_income = df_income.loc[tickers]
    data_income = ff.remove_all_zero_col(data_income)
    st.write("### :blue[配当実績]", data_income.sort_index())

except:
    st.stop()
