import bs4
import base
import write2file as wf
from douban_book import Book
import re

counter = 0

"""
从豆列解析所有图书的信息并写到文档
"""


def get_doulie_books(url):
    global counter

    soup = bs4.BeautifulSoup(base.get_html_text(url), 'html.parser')

    # 全局的tag不知怎么后来就 None了
    tag_name = ''
    try:
        tag = soup.select_one('#content > h1 > span')
        if tag:
            tag = tag.text.strip()
            if tag not in base.exclude_tags:
                if '｜' in tag:
                    tag_name = tag.split('｜')[1].strip().split()[0].strip()
                elif '|' in tag: 
                    tag_name = tag.split('|')[1].strip().split()[0].strip()
    except Exception:
        pass

    items = soup.select('.doulist-item')
    if items:
        for item in items:
            title = item.select_one('.title')
            if title:
                title = title.select_one('a')
                if title:
                    book_url = title.get('href')
                    book = get_one_book(book_url)
                    counter += 1
                    print(f'---{counter}---')
                    print(f'《{book.title}》获取成功')
                    wf.write_2_md(base.file_save_path, book, tag_name)
                    print(f'《{book.title}》写入文件成功')
        get_next_page(soup)


"""获取豆列下一页"""


def get_next_page(soup):
    next_page_url = ''
    paginator = soup.select_one('.paginator')
    if paginator:
        next = paginator.select_one('.next')
        if next:
            next_url = next.select_one('a')
            if next_url:
                next_page_url = next_url.get('href')
    if next_page_url:
        get_doulie_books(next_page_url)
    else:
        global counter
        counter = 0


"""
解析一本图书的信息，比如 
book = requestBook('https://book.douban.com/subject/34834004/')
"""


def get_one_book(url):
    book = Book(url)
    soup = bs4.BeautifulSoup(base.get_html_text(url), 'html.parser')

    title = get_content(soup, 'meta[property="og:title"]')
    if title:
        book.title = title
      
    author = get_content(soup, 'meta[property="book:author"]')
    if author:
        book.author = author
    
    isbn = get_content(soup, 'meta[property="book:isbn"]')
    if isbn:
        book.isbn = isbn

    image = get_content(soup, 'meta[property="og:image"]')
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
            sub_title = str(pl.next_sibling).strip()
            if sub_title:
                book.sub_title = sub_title
        if '原作名' in text:
            origin_title = str(pl.next_sibling).strip()
            if origin_title:
                book.origin_title = origin_title
        elif '出版年' in text:
            publish_year = str(pl.next_sibling).strip()[0:4]
            if publish_year:
                book.publish_year = publish_year
        elif '页数' in text:
            pages = str(pl.next_sibling).strip()
            if pages:
                pages = re.compile('\d+').search(pages)
                if pages:
                    book.pages = pages.group()

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
    return book


def get_content(soup, css):
    select = soup.select_one(css)
    if select:
        content = select.get('content')
        if content:
            return content.strip()
