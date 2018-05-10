


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
    if status ==status_choose:
        time.sleep(2)

# 麒麟相关图片识别并确定状态
def find_status_qilin(statusNow,imsrc):
    status = -1
    imobj =imobj_combat
    res =ac.find_template(imsrc,imobj)
    if res !=None and res['confidence']>confthreshold :
        status =status_combat
        print("---This is in battle Q...")

    if status<0 :
        imobj =imobj_qilin0
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =status_explore
            print("---This is in explore Q...")

    if status<0 :
        imobj =imobj_qilin14
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =status_choose
            print("---There choose qilin Q4...")

    if status<0 :
        imobj =imobj_qilin24
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =status_begin
            print("---There is a battle begin Q...")

    if status<0 :
        imobj =imobj_qilin31
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =status_end2
            print("---This is in end Q1...")

    if status<0 :
        imobj =imobj_qilin32
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =status_end2
            print("---This is in end Q2...")
    # 从结果中读取坐标
    if status >=0:
        statusNow =status
        pos =res['result']
        # 在目标范围内做一次随机取点
        w,h,r =imobj.shape
        posaim =(int(posbase[0]+pos[0]+w*(random.random()-0.5)*0.3),int(posbase[1]+pos[1]+h*(random.random()-0.5)*0.3))
        print(posaim,res['confidence'])
    else:
        posaim =(int(posbase[0]),int(posbase[1]))

    return status,posaim

# 御魂相关图片识别并确定状态
def find_status_yuhun(statusNow,imsrc):
    status = -1
    imobj =imobj_combat
    res =ac.find_template(imsrc,imobj)
    if res !=None and res['confidence']>confthreshold :
        status =status_combat
        print("---This is in battle Y...")

    if status<0 :
        imobj =imobj_yuhun0
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =status_explore
            print("---This is in explore Y...")
    '''
    if status<0 :
        imobj =imobj_yuhun11
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =status_choose
            print("---There choose yuhun Y1...")
    '''
    if status<0 :
        imobj =imobj_yuhun21
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthresholdH :
            status =status_begin
            print("---There is a battle begin Y1...")

    if status<0 :
        imobj =imobj_yuhun22
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthresholdH :
            status =status_begin
            print("---There is a battle begin Y2...")

    if status<0 :
        imobj =imobj_yuhun31
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =status_end1
            print("---This is in end Y1...")

    if status<0 :
        imobj =imobj_yuhun32
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =status_end2
            print("---This is in end Y3...")

    if status<0 :
        imobj =imobj_yuhun33
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =status_end2
            print("---This is in end Y2...")
    # 从结果中读取坐标
    if status >=0:
        statusNow =status
        pos =res['result']
        # 在目标范围内做一次随机取点
        w,h,r =imobj.shape
        posaim =(int(posbase[0]+pos[0]+w*(random.random()-0.5)*0.3),int(posbase[1]+pos[1]+h*(random.random()-0.5)*0.3))
        print(posaim,res['confidence'])
    else:
        posaim =(int(posbase[0]),int(posbase[1]))

    return status,posaim

# 获取窗口句柄及位置
clsname ="Qt5QWindowIcon"
tlename ="夜神模拟器"
hwnd =win32gui.FindWindow(clsname,tlename)
posbase =win32gui.GetWindowRect(hwnd)
# 截取指定位置屏幕并保存并重新载入
imobj_combat  =ac.imread("\\yysm\\obj_combat.png")

# 麒麟副本 源图待匹配目标读取
imobj_qilin0  =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yys\\obj_explore_juexing.png")
imobj_qilin14 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yys\\yys_qilin14_choose.png")
imobj_qilin24 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yys\\yys_qilin24_begin.png")
imobj_qilin31 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yys\\yys_qilin31_end.png")
imobj_qilin32 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yys\\yys_qilin32_end.png")
# 御魂副本 源图待匹配目标读取
imobj_yuhun0  =ac.imread("\\yysm\\obj_explore_yuhun.png")
imobj_yuhun11 =ac.imread("\\yysm\\yys_yuhun11_choose.png")
imobj_yuhun21 =ac.imread("\\yysm\\yys_yuhun21_begin.png")
imobj_yuhun22 =ac.imread("\\yysm\\yys_yuhun22_begin.png")
imobj_yuhun31 =ac.imread("\\yysm\\yys_yuhun31_end.png")
imobj_yuhun32 =ac.imread("\\yysm\\yys_yuhun32_end.png")
imobj_yuhun33 =ac.imread("\\yysm\\yys_yuhun33_end.png")



