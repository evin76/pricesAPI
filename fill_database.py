#берем цену на товар из chaicoffee
from bs4 import BeautifulSoup
#from selenium import webdriver
import requests
product_urls = [
    "https://chaicoffee.ru/index.php?route=product/category&path=108_59&ff35=296,295,311,272,268,304,328,287",
    "https://chaicoffee.ru/index.php?route=product/category&path=91_69",
    "https://chaicoffee.ru/index.php?route=product/category&path=122",
    "https://chaicoffee.ru/index.php?route=product/category&path=123",
    "https://chaicoffee.ru/index.php?route=product/category&path=252"
]

def get_page(url):
    return requests.get(url=url,headers=headers)

headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"}
pages = []
[pages.append(get_page(url)) for url in product_urls]

titles = []
prices = []
urls = []

for page in pages:
    soup = BeautifulSoup(page.content, "lxml")
    titles_page = soup.find_all("div", class_="name")
    prices_page = soup.find_all("span", class_="price-normal")
    urls_page = soup.find_all("a", class_="product-img has-second-image", href=True)
    titles = titles + titles_page[:len(urls_page)]
    prices = prices + prices_page[:len(urls_page)]
    urls = urls + urls_page

items = []
for title in titles:
    items.append([title.get_text()])
    #print(title.get_text())
for i in range(len(prices)):
    price = prices[i]
    price_int = int(price.get_text().replace("р.", ""))
    items[i].append(price.get_text())
    items[i].append(price_int)
    #print(price.get_text())
for i in range(len(urls)):
    url = urls[i]["href"]
    #print(url)
    items[i].append(url)
#print(items)
##################################################################################
#items[i][0] - name
#items[i][1] - prices
#items[i][2] - price_int
#items[i][3] - url, can be absent
##################################################################################
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()

class Price(Base):
    __tablename__ = "price"
    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime)
    name = Column(String(64))
    price = Column(String(64))
    price_int = Column(Numeric(10, 2))
    url = Column(String(64))

    def __repr__(self):
        return f"{self.name} | {self.price}"

engine = create_engine("sqlite:///database.sqlite")
Base.metadata.create_all(engine)

session = Session(bind=engine)
#exists = session.query(Price).filter(Price.name==title).all()
for item in items:
    title = item[0]
    price = item[1]
    price_int = item[2]
    url = ""
    if len(item) == 4:
        url = item[3]
    exists = session.query(Price).filter(Price.name==title).order_by(Price.datetime.desc()).first()
    if not exists:
        session.add(Price(name=title, datetime=datetime.now(), price=price, price_int=price_int, url=url))
        session.commit()
    else:
        if exists.price_int != price_int:
            session.add(Price(name=title, datetime=datetime.now(), price=price, price_int=price_int, url=url))
            session.commit()

query_items = session.query(Price).all()
#for item in query_items:
#    print(item)
