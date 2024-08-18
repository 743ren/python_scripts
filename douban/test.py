import douban_book_parse as db
import base
import write2file as wf

# 短简介
# https://book.douban.com/subject/30400258/
# 无简介
# https://book.douban.com/subject/19696780/ 
book = db.requestBook('https://book.douban.com/subject/34923499/')
wf.write2Md(base.fileSavePath, book)