import bs4
import re
from langdetect import detect


class Book:
    def __init__(self, url):
        self.url = url
        self.title = ''
        self.author = ''
        self.isbn = ''
        self.image = ''
        self.rating = ''
        self.sub_title = ''
        self.origin_title = ''
        self.publish_year = ''
        self.pages = ''
        self.description = []

    def init_with_html(self, html):
        soup = bs4.BeautifulSoup(html, 'html.parser')

        if title := self._get_content(soup, 'meta[property="og:title"]'):
            self.title = title

        if author := self._get_content(soup, 'meta[property="book:author"]'):
            self.author = author

        if isbn := self._get_content(soup, 'meta[property="book:isbn"]'):
            self.isbn = isbn

        if image := self._get_content(soup, 'meta[property="og:image"]'):
            self.image = image

        if rating := soup.select_one('.rating_num'):
            if rating := rating.text:
                if rating := rating.strip():
                    self.rating = rating

        for pl in soup.select('.pl'):
            text = pl.text.strip()
            if '副标题' in text:
                if sub_title := str(pl.next_sibling).strip():
                    self.sub_title = sub_title
            if '原作名' in text:
                if origin_title := str(pl.next_sibling).strip():
                    self.origin_title = origin_title
            elif '出版年' in text:
                if publish_year := str(pl.next_sibling).strip()[0:4]:
                    self.publish_year = publish_year
            elif '页数' in text:
                if pages := str(pl.next_sibling).strip():
                    if pages := re.compile(r'\d+').search(pages):
                        self.pages = pages.group()

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
            self.description = description

    def _get_content(self, soup, css):
        if select := soup.select_one(css):
            if content := select.get('content'):
                return content.strip()

    """
    获取导出内容
    """
    def get_export_md(self, tag):
        content_list = []
        content_list.append('---\n')
        content_list.append(f'地址: "{self.url}"\n')
        if self.image:
            content_list.append(f'封面: "{self.image}"\n')
        content_list.append(f'书名: "{self.title}"\n')
        if self.sub_title:
            content_list.append(f'副标题: "{self.sub_title}"\n')
        if self.origin_title:
            content_list.append(f'原作名: "{self.origin_title}"\n')
        if self.author:
            content_list.append(f'作者: "{self.author}"\n')
        if self.isbn:
            content_list.append(f'ISBN: "{self.isbn}"\n')
        if self.rating:
            content_list.append(f'评分: {self.rating}\n')
        if self.pages:
            content_list.append(f'页数: {self.pages}\n')
        if self.publish_year:
            content_list.append(f'出版年: {self.publish_year}\n')

        if tag:
            content_list.append(f'tags: [{tag}]\n')
        else:
            content_list.append('tags: \n')

        # content_list.append(f'状态: []\n')
        # content_list.append(f'来源: \n') EPUB 网络路径或者直接文件地址

        if language := self._get_language():
            content_list.append(f'语言: [{language}]\n')

        content_list.append('---\n\n')
        if self.image:
            content_list.append(f'![{self.title}|400]({self.image})\n\n')
        if self.description:
            content_list.append('## 简介\n\n')
            for des in self.description:
                content_list.append(f'{des.strip()}\n\n')
        return content_list

    """
    外文翻译的书，但是许多是翻译的英文，可能最初并不是英文的，还有些是外语的，但是没有原著名字
    """

    def _get_language(self):
        language = ''
        if re.search(r'\[美\]|\[英\]', self.author):
            language = '英语'
        elif re.search(r'\[法\]', self.author):
            language = '法语'
        elif re.search(r'\[德\]', self.author):
            language = '德语'
        elif re.search(r'\[俄\]', self.author):
            language = '俄语'
        elif re.search(r'\[日\]', self.author):
            language = '日语'
        elif re.search(r'\[韩\]', self.author):
            language = '韩语'
        elif self.origin_title:
            try:
                # 防止书名都是数字这种无法找到语言特征的
                lan = detect(self.origin_title)
                language = {
                    'en': '英语',
                    'fr': '法语',
                    'de': '德语',
                    'ru': '俄语',
                    'ja': '日语',
                    'ko': '韩语'
                }.get(lan, '')
            except Exception:
                pass
        return language
