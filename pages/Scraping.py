import streamlit as st
import API.scraping as sc
import pandas as pd

# ページの幅を1200ピクセルに設定
st.set_page_config(layout="wide")

if st.sidebar.button('上昇率・下降率TOP10'):

    info_col1, info_col2 = st.columns(2)
    with info_col1:

        url = "https://nikkeiyosoku.com/stock/twitter/"
        soup = sc.get_soup(url)

        selector = "body > div:nth-child(5) > div > div.col-sm-12.col-md-9 > div.section > div:nth-child(5) > table > tbody"

        res_array = sc.get_top10(soup, selector)
        res_array = pd.DataFrame(
            data=res_array,
            columns=[
                "No",
                "company_name",
                "rate"
            ]
        )
        print(res_array)
        # "No"列を削除
        res_array = res_array.drop(columns=["No"])

        # インデックスを 1 から始める
        res_array.index = range(1, len(res_array) + 1)

        st.header("上昇率ランキング")
        st.dataframe(res_array)

    with info_col2:

        selector = "body > div:nth-child(5) > div > div.col-sm-12.col-md-9 > div.section > div:nth-child(7) > table > tbody"

        res_array = sc.get_top10(soup, selector)
        res_array = pd.DataFrame(
            data=res_array,
            columns=[
                "No",
                "company_name",
                "rate"
            ]
        )
        print(res_array)
        # "No"列を削除
        res_array = res_array.drop(columns=["No"])

        # インデックスを 1 から始める
        res_array.index = range(1, len(res_array) + 1)

        st.header("下降率ランキング")
        st.dataframe(res_array)
