import time

import aircv as ac
import pyautogui
import win32con
from PIL import ImageGrab

import cv2
import win32api
import win32gui


#img =ImageGrab.grab(posbase)
#img.save("C:\\Users\\ShiAokai\\Pictures\\yysm\\a_pic_src.png")
#读取源图以及待匹配目标
#imsrc =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\a_pic_src.png")
imsrc =ac.imread("C:\\Users\\ShiAokai\\Pictures\\apic_tansuo_over.png")

imobj_tansuo41 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\yys_tansuo41_over.png")


imobj =imobj_tansuo41

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
