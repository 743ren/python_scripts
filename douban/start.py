import douban_book_parse as db
import base
import write2file as wf


while True:
    url = input('输入书单或图书地址(q: 退出)：')  # 自己输入不做校验
    if url == 'q':
        break
    elif 'douban.com/doulist' in url:  # 豆列
        db.get_doulie_books(url.strip())
    elif 'book.douban.com/subject' in url:  # 图书
        book = db.get_one_book(url.strip())
        wf.write_2_md(base.file_save_path, book)
