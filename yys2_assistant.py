
'''
2.0及以上版本试图实现多文件函数
这是一个来自远程的更改
'''
import time

import aircv as ac
import numpy as np
import pyautogui
import win32con
from PIL import ImageGrab

import cv2
import win32api
import win32gui
from yys2_fun_qilin  import find_status_qilin,taskQilin
from yys2_fun_yuhun  import find_status_yuhun,taskYuhun
from yys2_fun_tansuo import find_status_tansuo,taskTansuo


# 设置任务次数
qilincnt  =1
yuhuncnt  =3
tansuocnt =3
# 从输入读取，可省略
instr =input("Please input task times : ")
if instr:
    qilincnt,yuhuncnt,tansuocnt =(int(x) for x in instr.split(' '))
else:
    qilincnt  =1
    yuhuncnt  =3
    tansuocnt =3
#(int(x) for x in input("Please input task times : ").split(' '))
#abc =map(int, input("Please input : ").split())


# 获取窗口句柄及位置
clsname ="Qt5QWindowIcon"
tlename ="夜神模拟器"
hwnd =win32gui.FindWindow(clsname,tlename)
if hwnd!=None:
    posbase =win32gui.GetWindowRect(hwnd)
else:
    print("Warning: fail to find the window!!!")
        
# 假定一个初始状态，但随后被更新了
taskNow =-1


while(hwnd != None):
    # 记录时间
    begin_time =time.time()
    #截图
    img =ImageGrab.grab(posbase)
    #从图片格式像素[R,G,B]转化数组
    imary =np.array(img)
    #讲像素通道分离
    [r,g,b] =cv2.split(imary)
    #以oprncv像素格式[B,G,R]重新组成一幅图片并转化为数组
    imsrc =np.array(cv2.merge([b,g,r]))
    '''
    img.save("C:\\Users\\ShiAokai\\Pictures\\yysm\\a_pic_src.png")
    # 读取源图以及待匹配目标
    time.sleep(0.1)
    imsrc =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\a_pic_src.png")
    '''
    # 获取目标相对位置
    if taskNow==taskQilin or qilincnt>0:
        taskNow,qilincnt =find_status_qilin(taskNow,qilincnt,imsrc,posbase)
    elif  taskNow==taskYuhun or yuhuncnt>0:
        taskNow,yuhuncnt =find_status_yuhun(taskNow,yuhuncnt,imsrc,posbase)
    elif  taskNow==taskTansuo or tansuocnt>0:
        taskNow,tansuocnt =find_status_tansuo(taskNow,tansuocnt,imsrc,posbase)
    # 记录一下时间 以供参考
    end_time =time.time()
    if taskNow>=0 :  
        print("Use time:",end_time-begin_time,taskNow)

    if qilincnt<=0 and yuhuncnt<=0 and tansuocnt<=0 and taskNow<0:
        # 移动鼠标至指定位置
        pyautogui.moveTo(posbase[0]+36,posbase[1]+72)
        # 点击鼠标，仅在夜神模拟器实验成功
        pyautogui.click()
        break

print("Well done !!!")
