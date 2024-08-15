import bs4
import request_url as ru
import book_from_douban
from pathlib import Path
import write_book2file as wb

'''
从豆列解析所有图书的信息并写到文档
'''

path = Path.home()/'Documents/Write/Obsidian/图书馆'

def requestBooks(url):
  soup = bs4.BeautifulSoup(ru.requestUrl(url), 'html.parser')
  tag = ''
  try:
    tag = soup.select_one('#content > h1 > span').text.split('|')[1].strip()
  except:
    pass

  items = soup.select('.doulist-item')
  if items:
    for item in items:
      title = item.select_one('.title')
      if title:
        title = title.select_one('a')
        if title:
          bookUrl = title.get('href')
          book = book_from_douban.requestBook(bookUrl)
          wb.write2File(path, book, tag)
    getNextPage(soup)
    
'''获取下一页'''
def getNextPage(soup):
  paginator = soup.select_one('.paginator')
  if paginator:
    next = paginator.select_one('.next')
    if next:
      nextUrl = next.select_one('a')
      if nextUrl:
        nextPage = nextUrl.get('href')
        if nextPage:
          requestBooks(nextPage)
