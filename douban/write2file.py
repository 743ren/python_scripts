from pathlib import Path
from douban_book import Book
from langdetect import detect
import datetime
import re

"""
将书籍信息写入 markdown 文件，大部分作为 obsidian 用的文档属性
"""

# rememberCmd = ''

def write2Md(path: Path, book: Book, tag = ''):

  mdPath = getFinalPath(path, book)
  if not mdPath:
    return

  with open(mdPath, 'w', encoding='UTF-8') as f:
    f.write('---\n')
    f.write(f'地址: "{book.url}"\n')
    if book.image:
      f.write(f'封面: "{book.image}"\n')
    f.write(f'书名: "{book.title}"\n')
    if book.subTitle:
      f.write(f'副标题: "{book.subTitle}"\n')
    if book.originTitle:
      f.write(f'原作名: "{book.originTitle}"\n')
    if book.author:
      f.write(f'作者: "{book.author}"\n')
    if book.isbn:
      f.write(f'ISBN: "{book.isbn}"\n')
    if book.rating:
      f.write(f'评分: {book.rating}\n')
    if book.pages:
      f.write(f'页数: {book.pages}\n')
    if book.publishYear:
      f.write(f'出版年: {book.publishYear}\n')

    if tag:
      f.write(f'tags: [{tag}]\n')
    else:
      f.write(f'tags: \n')

    # f.write(f'状态: []\n')
    # f.write(f'来源: \n') EPUB 网络路径或者直接文件地址

    # language = getLanguage(book)
    if language := getLanguage(book):
      f.write(f'语言: [{language}]\n')

    f.write('---\n\n')
    if book.image:
      f.write(f'![{book.title}|400]({book.image})\n\n')
    if book.description:
      f.write(f'## 简介\n\n')
      for des in book.description:
        f.write(f'{des}\n\n')

def getFinalPath(path: Path, book: Book):
  # global rememberCmd
  mdPath = path/f'{book.title}.md'
  if mdPath.exists():
    # if rememberCmd:
    #   cmd = rememberCmd
    # else:
    #   cmd = input('存在同名文件如何处理？(a: 覆盖, b: 跳过, c: 改名，命令后面加 r 表示记住):')
    
    # if cmd.startswith('a'):
    #   mdPath.unlink()
    # elif cmd.startswith('b'):
    #   return ''
    # elif cmd.startswith('c'):
      mdPath = path/f'{book.title}_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.md'
    # if cmd.endswith('r'):
    #   rememberCmd = cmd
  return mdPath

"""
外文翻译的书，但是许多是翻译的英文，可能最初并不是英文的，还有些是外语的，但是没有原著名字
"""
def getLanguage(book: Book):
  language = ''
  if re.search(r'\[美\]|\[英\]', book.author):
    language = '英语'
  elif re.search(r'\[法\]', book.author):
    language = '法语'
  elif re.search(r'\[德\]', book.author):
    language = '德语'
  elif re.search(r'\[俄\]', book.author):
    language = '俄语'
  elif re.search(r'\[日\]', book.author):
    language = '日语'
  elif re.search(r'\[韩\]', book.author):
    language = '韩语'
  elif book.originTitle:
    try:
      lan = detect(book.originTitle) # 防止书名都是数字这种无法找到语言特征的
      language = {
        'en': '英语', 
        'fr': '法语', 
        'de': '德语', 
        'ru': '俄语',
        'ja': '日语',
        'ko': '韩语'
      }.get(lan, '')
    except:
      pass
  return language  