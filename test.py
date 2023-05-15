import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
from API.bs4_stock_data import BsStockData


li = BsStockData.scrape_website(9104)
print(li)