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
  pyautogui.hotkey('command', 'u')
  sleep(10)
  pyautogui.hotkey('command', 'a')
  sleep(1)
  pyautogui.hotkey('command', 'c')
  text = pyperclip.paste()
  pyautogui.hotkey('command', 'w')
  pyautogui.hotkey('command', 'w')
  return text