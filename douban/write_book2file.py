from pathlib import Path
from douban_book import Book
from langdetect import detect

'''
将书籍信息写入 markdown 文件，大部分作为 obsidian 用的文档属性
'''

def write2File(path: Path, book: Book, tag: str):
  with open(Path(path, f'{book.title}.md'), 'w', encoding='UTF-8') as f:
    f.write('---\n')
    f.write(f'地址: "{book.url}"\n')
    if book.image:
      f.write(f'封面: "{book.image}"\n')
    f.write(f'书名: "{book.title}"\n')
    if book.originTitle:
      f.write(f'原作: "{book.originTitle}"\n')
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
    f.write(f'成书年: \n')

    if tag:
      f.write(f'tags: [{tag}]\n')
    else:
      f.write(f'tags: \n')

    f.write(f'状态: []\n')
    # f.write(f'来源: \n') EPUB 网络路径或者直接文件地址
    
    language = getLanguage(book)
    if language:
      f.write(f'语言: [{language}]\n')

    f.write('---\n\n')
    if book.image:
      f.write(f'![{book.title}|400]({book.image})\n\n')
    if book.description:
      f.write(f'## 简介\n')
      for des in book.description:
        f.write(f'{des}\n\n')
    
    print(f'{book.title} 写到 markdown 文件成功')

'''
外文翻译的书，但是许多是翻译的英文，可能最初并不是英文的，还有些是外语的，但是没有原著名字
'''
def getLanguage(book: Book):
  language = ''
  if book.originTitle:
    lan = detect(book.originTitle)
    if lan == 'en':
      language = '英语'
    elif lan == 'fr':
      language = '法语'
    elif lan == 'de':
      language = '德语'
    elif lan == 'ru':
      language = '俄语'
    elif lan == 'ja':
      language = '日语'
    elif lan == 'ko':
      language = '韩语'
  return language  