from pathlib import Path
from douban_book import Book
import datetime

"""
将书籍信息写入 markdown 文件，大部分作为 obsidian 用的文档属性
"""

# rememberCmd = ''


def write_2_md(path: Path, book: Book, tag: str = ''):
    if not path.exists():
        path.mkdir(parents=True)

    mdPath = getFinalPath(path, book)
    if not mdPath:
        return

    with open(mdPath, 'w', encoding='UTF-8') as f:
        f.writelines(book.get_export_md(tag))


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
