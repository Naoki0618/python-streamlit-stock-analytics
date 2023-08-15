import requests
from bs4 import BeautifulSoup

def get_soup(url):

    # ページの内容を取得
    response = requests.get(url)
    content = response.content

    # BeautifulSoupを使って解析
    soup = BeautifulSoup(content, 'lxml')

    return soup

def get_top10(soup, selector):

    # 暴騰・急騰銘柄TOP 10
    elements = soup.select(selector)

    res_array = []

    trs = elements[0].find_all('tr')
    for tr in trs:
        try:  
            no = tr.contents[1].text
            company_name = tr.contents[5].text
            rate_of_up = tr.contents[9].text
            # print("No：" + str(no) + " 会社名：" + str(company_name) + " 率：" + str(rate_of_up))
            res_array.append([no, company_name, rate_of_up])
        except:
            pass

    return res_array

# # スクレイピング対象のURL
# url = "https://nikkeiyosoku.com/stock/twitter/"
# selector = "body > div:nth-child(5) > div > div.col-sm-12.col-md-9 > div.section > div:nth-child(5) > table > tbody"

# res_array = get_top10(url, selector)
# print(res_array)