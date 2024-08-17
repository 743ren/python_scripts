import douban_book_parse as db
import base
import write2file as wf
import bs4

book = db.requestBook('https://book.douban.com/subject/36331624/')
wf.write2Md(base.fileSavePath, book)