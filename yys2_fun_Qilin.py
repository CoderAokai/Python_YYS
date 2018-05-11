


import random
import time

import aircv as ac
import pyautogui
import win32con
from PIL import ImageGrab

import cv2
import win32api
import win32gui

#刷麒麟的任务编码
taskQilin =1

confthreshold  = 0.7
confthresholdH = 0.9

# 这种状态值的定义
qilin_explore   =0
qilin_combat    =222
qilin_choose    =14
qilin_begin     =24
qilin_ready     =28
qilin_end1      =31
qilin_end2      =32
statuslast      = -11

# 根据状态，定义一个动作函数
def click_button_lift(posbase,offset,w,h):
    #取随机量
    posaim =(int(posbase[0]+offset[0]+w*(random.random()-0.5)*0.3),int(posbase[1]+offset[1]+h*(random.random()-0.5)*0.3))
    # 移动鼠标至指定位置
    pyautogui.moveTo(posaim[0],posaim[1])
    # 点击鼠标，仅在夜神模拟器实验成功
    pyautogui.click()

def click_action_qilin(taskNow,qilincnt,status,posbase,offset,w,h):
    #引用的全局变量
    global statuslast
    #在探索界面点击进入,或重置状态
    if status==qilin_explore:
        if qilincnt>0:
            taskNow =taskQilin
            click_button_lift(posbase,offset,w,h)
        else:
            taskNow = -1
    #在结算界面点击结束
    elif status==qilin_end1 or status==qilin_end2 or status==qilin_ready:
        click_button_lift(posbase,offset,w,h)
    #在开始界面判断任务次数,顺带修正状态
    elif status==qilin_begin:
        if qilincnt>0:
            click_button_lift(posbase,offset,w,h)
        else:
            taskNow = -1
            click_button_lift(posbase,[657,186],27,27)
    #在选择界面判断任务次数,并修正任务状态
    elif status==qilin_choose:
        if qilincnt>0:
            taskNow =taskQilin
            click_button_lift(posbase,offset,w,h)
        elif 0:
            taskNow = -1
            click_button_lift(posbase,[675,540],180,50)  #[675,540],180,50
    #从另外一个状态进入的战斗,任务次数削减1
    elif status==qilin_combat and statuslast!=status:
        qilincnt =qilincnt-1

    #更新状态记录       
    statuslast =status

    return taskNow,qilincnt

# 麒麟相关图片识别并确定状态
def find_status_qilin(taskNow,qilincnt,imsrc,posbase):
    #使用的临时状态量
    status = -1
    #检测是否处于战斗状态
    imobj =imobj_combat
    res =ac.find_template(imsrc,imobj)
    if res !=None and res['confidence']>confthreshold :
        status =qilin_combat
    #检测是否在探索选择界面
    if status<0 :
        imobj =imobj_qilin0
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =qilin_explore
    #检测是否有开始按钮
    if status<0 :
        imobj =imobj_qilin24
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =qilin_begin
    #检测是否在选择界面       
    if status<0 :
        imobj =imobj_qilin14
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =qilin_choose
    #检测是否有准备按钮
    if status<0 :
        imobj =imobj_qilin2R
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =qilin_ready
    #检查结算界面1
    if status<0 :
        imobj =imobj_qilin31
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =qilin_end2
    #检查结算界面2        
    if status<0 :
        imobj =imobj_qilin32
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =qilin_end2
    # 从结果中读取坐标
    if status >=0 :
        offset =res['result']
        # 在目标范围内做一次随机取点
        w,h,r =imobj.shape
        taskNow,qilincnt =click_action_qilin(taskNow,qilincnt,status,posbase,offset,w,h)
    #防止误操作这里休停2秒
    time.sleep(2)
    
    return taskNow,qilincnt



# 截取指定位置屏幕并保存并重新载入
imobj_combat  =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\obj_combat.png")
# 麒麟副本 源图待匹配目标读取
imobj_qilin0  =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\obj_explore_juexing.png")
imobj_qilin14 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\yys_qilin14_choose.png")
imobj_qilin24 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\yys_qilin24_begin.png")
imobj_qilin2R =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\yys_qilin28_ready.png")
imobj_qilin31 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\yys_qilin31_end.png")
imobj_qilin32 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\yys_qilin32_end.png")



