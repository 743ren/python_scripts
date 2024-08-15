import bs4
import request_url as ru

'''
解析一本图书的信息，比如 
book = requestBook('https://book.douban.com/subject/34834004/')
book = requestBook('https://book.douban.com/subject/34834004/')
'''

# 解析一本书
def requestBook(url):
  book = {'url': url}
  soup = bs4.BeautifulSoup(ru.requestUrl(url), 'html.parser')

  title = getContent(soup, 'meta[property="og:title"]')
  if title:
    book['title'] = title
    
  author = getContent(soup, 'meta[property="book:author"]')
  if author:
    book['author'] = author
  
  isbn = getContent(soup, 'meta[property="book:isbn"]')
  if isbn:
    book['isbn'] = isbn

  image = getContent(soup, 'meta[property="og:image"]')
  if image:
    book['image'] = image

  rating = soup.select_one('.rating_num')
  if rating:
    rating = rating.text
    if rating:
      rating = rating.strip()
      if rating:
        book['rating'] = rating
  
  for pl in soup.select('.pl'):
    text = pl.text.strip()
    if '原作名' in text:
      originTitle = str(pl.next_sibling).strip()
      if originTitle:
        book['originTitle'] = originTitle
    elif '出版年' in text:
      publishYear = str(pl.next_sibling).strip()[0:4]
      if publishYear:
        book['publishYear'] = publishYear
    elif '页数' in text:
      pages = str(pl.next_sibling).strip()
      if pages:
        book['pages'] = pages

  # 内容简介被包装在多个 p 标签里
  description = ''
  des = soup.select('#link-report > span.all.hidden > div > div > p')
  if des:
    desp = map(lambda p: p.text, des)
    description = list(desp)

    book['description'] = description

  return book

def getContent(soup, css):
  select = soup.select_one(css)
  if select:
    content = select.get('content')
    if content:
      return content.strip()