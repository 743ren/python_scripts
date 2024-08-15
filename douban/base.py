import requests
from pathlib import Path

fileSavePath = Path.home()/'Documents/Write/Obsidian/图书馆'

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}

def requestUrl(url):
  res = requests.get(url, headers=headers)
  res.raise_for_status() # 如果出错会抛出 HTTPError
  return res.text