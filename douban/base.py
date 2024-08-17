from pathlib import Path
import pyautogui
import webbrowser
from time import sleep
import pyperclip

fileSavePath = Path.home()/'Documents/Write/Obsidian/图书馆'

def requestUrl(url):
  webbrowser.open(url) # 浏览器打开网页
  sleep(5) # 等待网页加载
  wh = pyautogui.size()
  pyautogui.click(wh.width/4, wh.height/2) # 点击鼠标，让浏览器高亮
  pyautogui.hotkey('command', 'u') # 打开源代码页面
  sleep(10) # 等待源代码加载出来
  pyautogui.hotkey('command', 'a') # 全选
  sleep(1)
  pyautogui.hotkey('command', 'c') # 复制
  text = pyperclip.paste() # 从剪贴板取出源代码
  pyautogui.hotkey('command', 'w') # 关闭源代码窗口
  pyautogui.hotkey('command', 'w') # 关闭网页窗口
  return text