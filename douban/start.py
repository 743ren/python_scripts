import douban_book_parse as db

while True:
  doulie = input('输入豆列地址(q: 退出): ') # 自己输入不做校验
  if doulie == 'q':
    break
  else:
    db.requestDoulieBooks(doulie.strip())