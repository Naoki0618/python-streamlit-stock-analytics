import requests
from bs4 import BeautifulSoup

class BsStockData:

    def scrape_website(symbol):
        
        url = "https://www.nikkei.com/nkd/company/history/trust/?scode=" + str(symbol)
        # URLからHTMLを取得
        response = requests.get(url)
        html_content = response.text

        # BeautifulSoupを使ってHTMLを解析
        soup = BeautifulSoup(html_content, 'html.parser')

        val = soup.find_all('td', class_="a-taR a-wordBreakAll")

        return val[2].text