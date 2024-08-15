import bs4
import request_url as ru
import book_from_douban

'''
从豆列解析所有图书的信息
'''

def requestBooks(url):
  soup = bs4.BeautifulSoup(ru.requestUrl(url), 'html.parser')

  items = soup.select('.doulist-item')
  if items:
    for item in items:
      title = item.select_one('.title')
      if title:
        title = title.select_one('a')
        if title:
          bookUrl = title.get('href')
          book = book_from_douban.requestBook(bookUrl)
          


requestBooks('https://www.douban.com/doulist/130417194/')
