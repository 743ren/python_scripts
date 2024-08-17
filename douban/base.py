import requests
from pathlib import Path
import random

fileSavePath = Path.home()/'Documents/Write/Obsidian/图书馆'

agents = [
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
]

http = [
	"http://218.75.102.198:8000", 
	"http://153.101.67.170:9002" 
	"http://47.94.207.215:3128" 
	"http://58.99.117.143:80" 
	"http://154.203.132.55:8080" 
	"http://154.90.49.103:9090" 
	"http://103.59.45.53:8080" 
	"http://103.36.136.138:8090" 
	"http://39.102.214.199:9080" 
	"http://203.19.38.114:1080" 
	"http://47.243.92.199:3128" 
	"http://47.242.47.64:8888" 
]

proxy = { 
	 "http": http[random.randrange(0, len(http))], 
	#  "https": "https://211.136.128.154:53281" 
}

def requestUrl(url, headers={}):
  headers['User-Agent'] = agents[random.randrange(0, len(agents))]
  res = requests.get(url, headers=headers, proxies=proxy)
  print(res.status_code)
  res.raise_for_status() # 如果出错会抛出 HTTPError
  return res.text