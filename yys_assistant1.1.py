
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

status_yh_choose =121
status_ts_choose =131

# 自定义一个单击函数
def clickLeftCur():  
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN|win32con.MOUSEEVENTF_LEFTUP, 0, 0)
# 根据状态，定义一个动作函数
def click_action(status,posaim):
    if status>=0 and status !=status_combat and status !=status_explore and statusNow !=status_yh_choose and status !=status_ts_choose: 
        # 移动鼠标至指定位置
        pyautogui.moveTo(posaim[0],posaim[1])
        # 点击鼠标，仅在夜神模拟器实验成功
        pyautogui.click()
    if status ==status_ts_choose:
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

    if status<0 :
        imobj =imobj_yuhun11
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =status_choose
            print("---There choose yuhun Y1...")
            if statusNow ==status_choose:
                status =status_yh_choose

    if status<0 :
        imobj =imobj_yuhun21
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthresholdH :
            status =status_begin
            print("---There is a battle begin Y...")

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
# 探索相关图片识别并确定状态
def find_status_tansuo(statusNow,imsrc):
    status = -1
    imobj =imobj_combat
    res =ac.find_template(imsrc,imobj)
    if res !=None and res['confidence']>confthreshold :
        status =status_combat
        print("---This is in battle t...")

    if status<0 :
        imobj =imobj_tansuo10
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =status_begin
            print("---There is a battle begin t...")
    
    if status<0 :
        imobj =imobj_tansuo13
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold-0.1 :
            status =status_ts_choose
            print("---There choose tansuo t3...")    

    if status<0 :
        imobj =imobj_tansuo11
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold-0.1 :
            status =status_ts_choose
            print("---There choose tansuo t1...")

    if status<0 :
        imobj =imobj_tansuo12
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold-0.1 :
            status =status_ts_choose
            print("---There choose tansuo t2...")

    if status<0 :
        imobj =imobj_tansuo31
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =status_end2
            print("---This is in end t1...")

    if status<0 :
        imobj =imobj_yuhun32
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =status_end2
            print("---This is in end t2...")
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
    # 如果是第二次进入choose则可执行点击
    if statusNow==status_ts_choose:
        status =status_choose

    return status,posaim

# 获取窗口句柄及位置
clsname ="Qt5QWindowIcon"
tlename ="夜神模拟器"
hwnd =win32gui.FindWindow(clsname,tlename)
posbase =win32gui.GetWindowRect(hwnd)
# 截取指定位置屏幕并保存并重新载入
img =ImageGrab.grab(posbase)
img.save("C:\\Users\\ShiAokai\\Pictures\\yys\\yysys_src.png")
imsrc =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yys\\yysys_src.png")
imobj_combat  =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yys\\obj_combat.png")
# 麒麟副本 源图待匹配目标读取
imobj_qilin0  =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yys\\obj_explore_juexing.png")
imobj_qilin14 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yys\\yys_qilin14_choose.png")
imobj_qilin24 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yys\\yys_qilin24_begin.png")
imobj_qilin31 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yys\\yys_qilin31_end.png")
imobj_qilin32 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yys\\yys_qilin32_end.png")
# 御魂副本 源图待匹配目标读取
imobj_yuhun0  =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yys\\obj_explore_yuhun.png")
imobj_yuhun11 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yys\\yys_yuhun11_choose.png")
imobj_yuhun21 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yys\\yys_yuhun21_begin.png")
imobj_yuhun31 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yys\\yys_yuhun31_end.png")
imobj_yuhun32 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yys\\yys_yuhun32_end.png")
# 探索副本 待匹配图
imobj_tansuo10 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yys\\yys_tansuo10_begin.png")
imobj_tansuo11 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yys\\yys_tansuo11_choose.png")
imobj_tansuo12 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yys\\yys_tansuo12_choose.png")
imobj_tansuo13 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yys\\yys_tansuo13_choose.png")
imobj_tansuo30 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yys\\yys_tansuo30_end.png")
imobj_tansuo31 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yys\\yys_tansuo31_end.png")
imobj_tansuo32 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yys\\yys_tansuo32_end.png")


# 假定一个初始状态，但随后被更新了
statusNow =-1

while(hwnd != None) :
    # 记录时间
    begin_time =time.time()
    # 截取指定位置屏幕并保存
    img =ImageGrab.grab(posbase)
    img.save("C:\\Users\\ShiAokai\\Pictures\\yys\\yys_src.png")
    # 读取源图以及待匹配目标
    imsrc =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yys\\yys_src.png")
    # 获取目标相对位置
    statusNow,posaim =find_status_qilin(statusNow,imsrc)
    if statusNow <0:
        statusNow,posaim =find_status_yuhun(statusNow,imsrc)
    if statusNow <0:
        statusNow,posaim =find_status_tansuo(statusNow,imsrc)
    # 记录一下时间 以供参考
    end_time =time.time()
    if statusNow>=0 :  
        print("Use time:",end_time-begin_time,statusNow)

    # 确定执行何种动作
    click_action(statusNow,posaim)
    # 休眠0.1秒
    time.sleep(0.1) 
