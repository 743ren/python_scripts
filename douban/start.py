import douban_book_parse as db
import base
import write2file as wf

while True:
  doulie = input('输入豆列地址(q: 退出): ') # 自己输入不做校验
  if doulie == 'q':
    break
  else:
    db.requestDoulieBooks(doulie.strip())

# book = db.requestBook('https://book.douban.com/subject/36331624/')
# wf.write2Md(base.fileSavePath, book)