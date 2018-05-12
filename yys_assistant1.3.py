


import random
import time

import aircv as ac
import pyautogui
import win32con
from PIL import ImageGrab

import cv2
import win32api
import win32gui

confthreshold  = 0.8
confthresholdH = 0.9

status_combat    =2
status_explore   =0
status_choose    =14
status_begin     =142
status_end1      =31
status_end2      =32
status_end3      =33


# 自定义一个单击函数
def clickLeftCur():  
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN|win32con.MOUSEEVENTF_LEFTUP, 0, 0)
# 根据状态，定义一个动作函数
def click_action(status,posaim):
    if status>=0 and status !=status_combat and status !=status_explore: 
        # 移动鼠标至指定位置
        pyautogui.moveTo(posaim[0],posaim[1])
        # 点击鼠标，仅在夜神模拟器实验成功
        pyautogui.click()
    if status ==status_choose or status==status_explore:
        time.sleep(2)

# 御魂相关图片识别并确定状态
def find_status_yuhun(statusNow,imsrc):
    status = -1
    imobj =imobj_combat
    res =ac.find_template(imsrc,imobj)
    if res !=None and res['confidence']>confthreshold :
        status =status_combat
    #探索自动进入御魂
    if status<0 :
        imobj =imobj_yuhun0
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =status_explore
    '''
    if status<0 :
        imobj =imobj_yuhun11
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =status_choose
            print("---There choose yuhun Y1...")
    '''
    #御魂单刷开始界面
    if status<0 :
        imobj =imobj_yuhun21
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthresholdH :
            status =status_begin
    #御魂组队开始界面
    if status<0 :
        imobj =imobj_yuhun22
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthresholdH :
            status =status_begin
    #御魂结算界面1
    if status<0 :
        imobj =imobj_yuhun31
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =status_end1
    #御魂结算界面2
    if status<0 :
        imobj =imobj_yuhun32
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =status_end2
    # 从结果中读取坐标
    if status >=0:
        statusNow =status
        pos =res['result']
        # 在目标范围内做一次随机取点
        w,h,r =imobj.shape
        posaim =(int(posbase[0]+pos[0]+w*(random.random()-0.5)*0.3),int(posbase[1]+pos[1]+h*(random.random()-0.5)*0.3))
        #print(posaim,res['confidence'])
    else:
        posaim =(int(posbase[0]),int(posbase[1]))

    return status,posaim

# 获取窗口句柄及位置
clsname ="Qt5QWindowIcon"
tlename ="夜神模拟器"
hwnd =win32gui.FindWindow(clsname,tlename)
posbase =win32gui.GetWindowRect(hwnd)
# 截取指定位置屏幕并保存并重新载入
imobj_combat  =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\obj_combat.png")

# 御魂副本 源图待匹配目标读取
imobj_yuhun0  =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\obj_explore_yuhun.png")
imobj_yuhun11 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\yys_yuhun11_choose.png")
imobj_yuhun21 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\yys_yuhun21_begin.png")
imobj_yuhun22 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\yys_yuhun22_begin.png")
imobj_yuhun31 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\yys_yuhun31_end.png")
imobj_yuhun32 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\yys_yuhun32_end.png")
#imobj_yuhun33 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\yys_yuhun33_end.png")
# 假定一个初始状态，但随后被更新了
statusNow =-1
# 记录时间
begin_time =time.time()
last_time  =time.time()
while(hwnd != None) :
    # 截取指定位置屏幕并保存
    img =ImageGrab.grab(posbase)
    img.save("C:\\Users\\ShiAokai\\Pictures\\yysm\\yys_src.png")
    # 读取源图以及待匹配目标
    imsrc =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\yys_src.png")
    # 获取目标相对位置
    statusNow,posaim =find_status_yuhun(statusNow,imsrc)
    # 记录一下时间 以供参考
    end_time =time.time()
    if statusNow>=0 and end_time-last_time>10:
        last_time =end_time  
        print("Use time:",end_time-begin_time,statusNow)
    # 确定执行何种动作
    click_action(statusNow,posaim)
