
import win32api,win32gui
import time
import numpy as np
from PIL import ImageGrab


classname ="Qt5QWindowIcon"
titlename ="夜神模拟器"
hwnd =win32gui.FindWindow(classname,titlename)
left,top,right,bottom =win32gui.GetWindowRect(hwnd)
print(left,top,right,bottom)



# 每抓取一次屏幕需要的时间约为1s,如果图像尺寸小一些效率就会高一些
beg = time.time()
debug = False

img = ImageGrab.grab(bbox=(left,top,right,bottom))
img.save("C:\\Users\\ShiAokai\\Pictures\\apic_test.png")
img = np.array(img.getdata(), np.uint8).reshape(img.size[1], img.size[0], 3)
end = time.time()
print(end - beg)
