import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
# Using object notation
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )

st.title('株式情報を取得して表示するアプリ')

ticker = st.text_input('株式コードを入力してください')
stock = yf.Ticker(ticker + ".T")

if not stock.history(period='1d').empty:
    st.subheader('株価情報')

    # 株価情報を表示
    info_col1, info_col2, info_col3 = st.columns(3)
    try:
        with info_col1:
            st.write('前日終値')
            st.write(stock.info['regularMarketPreviousClose'])
    except:
        pass
    try:
        with info_col2:
            st.write('始値')
            st.write(stock.info['regularMarketOpen'])
    except:
        pass
    try:            
        with info_col3:
            st.write('終値')
            st.write(stock.info['regularMarketPrice'])
    except:
        pass

    # 指標を表示
    st.subheader('指標')
    indicators = ['marketCap', 'trailingPE', 'forwardPE', 'priceToSalesTrailing12Months', 'priceToBook']
    indicator_values = [stock.info[indicator] for indicator in indicators]
    indicator_col1, indicator_col2, indicator_col3 = st.columns(3)
    with indicator_col1:
        st.write('時価総額')
        st.write(indicator_values[0])
        st.write('直近1年間の利益率')
        st.write(indicator_values[1])
    with indicator_col2:
        st.write('今後1年間の利益率')
        st.write(indicator_values[2])
        st.write('直近12か月間の売上高')
        st.write(indicator_values[3])
    with indicator_col3:
        st.write('P/BV')
        st.write(indicator_values[4])

    # 株価のグラフを表示
    st.subheader('株価のグラフ')
    period = st.selectbox('期間を選択', ['1日', '1週間', '1ヶ月', '3ヶ月', '6ヶ月', '1年', '2年', '5年', '最大'])
    if period == '1日':
        interval = '5m'
        period = '1d'
    else:
        interval = '1d'
        if period == '最大':
            period = 'max'
        else:
            period = period.replace('ヶ月', 'mo').replace('週間', 'wk').replace('年', 'y')+'期間'
    data = stock.history(period=period, interval=interval)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=data.index,
                                  open=data['Open'],
                                  high=data['High'],
                                  low=data['Low'],
                                  close=data['Close'],
                                  name='株価'))
    fig.update_layout(title='株価のグラフ',
                      xaxis_title='日付',
                      yaxis_title='株価',
                      xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)
else:
    st.write('株式コードが無効です。')
