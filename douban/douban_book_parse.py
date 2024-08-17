import bs4
import base
import write2file as wf
from douban_book import Book

"""
从豆列解析所有图书的信息并写到文档
"""
def requestDoulieBooks(url):
  soup = bs4.BeautifulSoup(base.requestUrl(url), 'html.parser')
  tag = ''
  try:
    tag = soup.select_one('#content > h1 > span').text.split('｜')[1].strip().split()[0].strip()
    if tag == '其它':
      tag = '' # 忽略它
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
          book = requestBook(bookUrl)
          wf.write2Md(base.fileSavePath, book, tag)
    getNextPage(soup)
    
"""获取豆列下一页"""
def getNextPage(soup):
  paginator = soup.select_one('.paginator')
  if paginator:
    next = paginator.select_one('.next')
    if next:
      nextUrl = next.select_one('a')
      if nextUrl:
        nextPage = nextUrl.get('href')
        if nextPage:
          requestDoulieBooks(nextPage)


"""
解析一本图书的信息，比如 
book = requestBook('https://book.douban.com/subject/34834004/')
"""
def requestBook(url):
  book = Book(url)
  soup = bs4.BeautifulSoup(base.requestUrl(url), 'html.parser')

  title = getContent(soup, 'meta[property="og:title"]')
  if title:
    book.title = title
    
  author = getContent(soup, 'meta[property="book:author"]')
  if author:
    book.author = author
  
  isbn = getContent(soup, 'meta[property="book:isbn"]')
  if isbn:
    book.isbn = isbn

  image = getContent(soup, 'meta[property="og:image"]')
  if image:
    book.image = image

  rating = soup.select_one('.rating_num')
  if rating:
    rating = rating.text
    if rating:
      rating = rating.strip()
      if rating:
        book.rating = rating
  
  for pl in soup.select('.pl'):
    text = pl.text.strip()
    if '副标题' in text:
      subTitle = str(pl.next_sibling).strip()
      if subTitle:
        book.subTitle = subTitle
    if '原作名' in text:
      originTitle = str(pl.next_sibling).strip()
      if originTitle:
        book.originTitle = originTitle
    elif '出版年' in text:
      publishYear = str(pl.next_sibling).strip()[0:4]
      if publishYear:
        book.publishYear = publishYear
    elif '页数' in text:
      pages = str(pl.next_sibling).strip()
      if pages:
        book.pages = pages

  # 内容简介被包装在多个 p 标签里
  description = ''
  # 内容简介比较长的情况
  des = soup.select('#link-report > span.all.hidden > div > div > p')
  if not des:
    # 只有很短的简介
    des = soup.select('#link-report > div > div > p')
  if des:
    desp = map(lambda p: p.text, des)
    description = list(desp)
    book.description = description
  print(f'获取图书信息成功 {book.title}')
  return book

def getContent(soup, css):
  select = soup.select_one(css)
  if select:
    content = select.get('content')
    if content:
      return content.strip()