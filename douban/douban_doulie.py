import bs4
import base
from douban_book import Book
import write2file as wf


class Doulie:
    def __init__(self, first_page_url):
        self.first_page_url = first_page_url
        self.name = ''
        self.tag = ''
        self.counter = 0

    """开始解析豆列"""
    def start_load(self):
        html_first = base.get_html_text(self.first_page_url)
        soup = bs4.BeautifulSoup(html_first, 'html.parser')
        if name := soup.select_one('#content > h1 > span'):
            name = name.text.strip()
            self.name = name

            self.tag = ''
            try:
                if '｜' in name:
                    self.tag = name.split('｜')[1].strip().split()[0].strip()
                elif '|' in name: 
                    self.tag = name.split('|')[1].strip().split()[0].strip()
            except Exception:
                pass
            if self.tag in base.exclude_tags:
                self.tag = ''
        self.load_books(soup)

    def load_books(self, soup):
        if items := soup.select('.doulist-item'):
            for item in items:
                if title := item.select_one('.title'):
                    if title := title.select_one('a'):
                        book_url = title.get('href')
                        book = base.load_one_book(book_url)
                        self.counter += 1
                        print(f'---{self.counter}---')
                        print(f'《{book.title}》获取成功')
                        dir_name = self.tag if self.tag else self.name
                        wf.write_2_md(base.file_save_path/dir_name, book, self.tag)
                        print(f'《{book.title}》写入文件成功')
            if next_page_url := self._get_next_page(soup):
                html_next = base.get_html_text(next_page_url)
                soup_next = bs4.BeautifulSoup(html_next, 'html.parser')
                self.load_books(soup_next)
            


    """获取豆列下一页"""
    def _get_next_page(self, soup):
        next_page_url = ''
        if paginator := soup.select_one('.paginator'):
            if next := paginator.select_one('.next'):
                if next_url := next.select_one('a'):
                    next_page_url = next_url.get('href')
        return next_page_url
