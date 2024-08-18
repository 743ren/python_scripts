import base
import write2file as wf
from douban_doulie import Doulie

while True:
    urls = input('输入书单或图书地址，多个地址以英文逗号分隔(q: 退出)：')  # 自己输入不做校验
    if urls == 'q':
        break
    for url in urls.split(','):
        if 'douban.com/doulist' in url:  # 豆列
            Doulie(url.strip()).start_load()
        elif 'book.douban.com/subject' in url:  # 图书
            book = base.load_one_book(url.strip())
            wf.write_2_md(base.file_save_path, book)
