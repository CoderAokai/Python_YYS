import time

import aircv as ac
import cv2
import numpy as np
import pyautogui
import win32con
from PIL import ImageGrab

import win32api
import win32gui

# 获取窗口句柄及位置
clsname ="Qt5QWindowIcon"
tlename ="夜神模拟器"
hwnd =win32gui.FindWindow(clsname,tlename)
if hwnd!=None:
    posbase =win32gui.GetWindowRect(hwnd)
else:
    print("Warning: fail to find the window!!!")

#截图
img =ImageGrab.grab(posbase)
#从图片格式像素[R,G,B]转化数组
imary =np.array(img)
#讲像素通道分离
[r,g,b] =cv2.split(imary)
#以oprncv像素格式[B,G,R]重新组成一幅图片并转化为数组
imsrc =np.array(cv2.merge([b,g,r]))

#img.save("C:\\Users\\ShiAokai\\Pictures\\yysm\\a_pic_src.png")
#读取源图以及待匹配目标
#imsrc =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\a_pic_src.png")
#imsrc =ac.imread("C:\\Users\\ShiAokai\\Pictures\\apic_tansuo_over.png")

imobj_yuhun0  =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\obj_explore_yuhun.png")
imobj_tansuo41 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\yys_tansuo41_over.png")


imobj =imobj_yuhun0

[w,h,r] =imobj.shape

pos =ac.find_template(imsrc,imobj)

rec =pos['rectangle']
whr =pos['result']

print(pos['confidence'])

color =(0,255,0)
linwidth=5

cv2.rectangle(imsrc,rec[0],rec[3],color,linwidth)

cv2.imshow('obj',imsrc)

cv2.waitkey(0)

cv2.destroyAllWindows()
