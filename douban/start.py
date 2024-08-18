import douban_book_parse as db
import base
import write2file as wf

# while True:
#   doulie = input('输入豆列地址(q: 退出): ') # 自己输入不做校验
#   if doulie == 'q':
#     break
#   else:
#     db.requestDoulieBooks(doulie.strip())
while True:
  url = input('输入书单或图书地址(q: 退出)：') # 自己输入不做校验
  if url == 'q':
    break
  elif 'douban.com/doulist' in url: # 豆列
    db.requestDoulieBooks(url.strip())
  elif 'book.douban.com/subject' in url: # 图书
    book = db.requestBook(url.strip())
    wf.write2Md(base.fileSavePath, book)