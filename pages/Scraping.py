import streamlit as st
import API.scraping as sc
import pandas as pd
import time

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


if st.sidebar.button('投資信託構成銘柄'):

    fund_path = []

    for page_index in range(5):
        time.sleep(1)

        url = "https://itf.minkabu.jp/ranking/popular?fund_type=index&page=" + str(page_index + 1)
        selector = "#rankingList > div.pageCon_plate.page-return-cache > div:nth-child(3) > div.ly_content_wrapper.size_m > div > div.md_table_wrapper.ranking_table > div.md_table_wrapper > table > tbody"

        trs = sc.get_html(url, selector, 'a')

        if trs is None:
            continue

        for tr in trs:
            try:
                print(tr.attrs['class'])
                fund_path.append([tr.attrs['href'], tr.text])
            except:
                pass

    res_composition_list = []

    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)

    percent_complete = 0.0
    for index, fund in enumerate(fund_path):
        time.sleep(1)

        url = "https://itf.minkabu.jp" + fund[0] + "/detailed_info"
        selector = "#detailed_info_table > div.pdf_detailed_info > div.md_card.md_box.detailed_box.all_detailed_infos.ly_content_wrapper.loading_table > div.detailedInfo_table2_box.detail_stock_box > table > tbody"

        trs = sc.get_html(url, selector, 'tr')

        if trs is None:
            continue

        for tr in trs:
            try:
                tds = tr.find_all('td')
                company_code = tds[1].text.replace('\n', '')
                company_name = tds[2].text.replace('\n', '')

                sc.update_array(res_composition_list, company_code, company_name, fund[1])

            except:
                pass
            
        percent_complete += 1/len(fund_path)
        if percent_complete <= 1:
            my_bar.progress(percent_complete, text=progress_text)
            
    my_bar.empty()

    print(res_composition_list)


    # 1列目を基準に降順でソート
    res_composition_list = sorted(res_composition_list, key=lambda x: x[2], reverse=True)

    st.header("投資信託構成銘柄ランキング")
    res_array = pd.DataFrame(
        data=res_composition_list,
        columns=[
            "ティッカー",
            "会社名",
            "カウント",
            "採用投信"
        ]
    )
    st.dataframe(res_array)