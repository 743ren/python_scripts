import douban_book_parse as db
import base
import write2file as wf

# 短简介
# https://book.douban.com/subject/30400258/
# 无简介
# https://book.douban.com/subject/19696780/ 
book = db.get_one_book('https://book.douban.com/subject/34923499/')
wf.write_2_md(base.file_save_path, book)
