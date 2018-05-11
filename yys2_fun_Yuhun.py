


import random
import time

import aircv as ac
import pyautogui
import win32con
from PIL import ImageGrab

import cv2
import win32api
import win32gui

#刷御魂的任务编码
taskYuhun =2

confthreshold  = 0.7
confthresholdH = 0.9

#关于状态的定义
yuhun_combat    =2
yuhun_explore   =0
yuhun_choose    =11
yuhun_begin     =21
yuhun_ready     =28
yuhun_end1      =31
yuhun_end2      =32
statuslast      = -11


# 自定义一个单击函数
#def clickLeftCur():  
#    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN|win32con.MOUSEEVENTF_LEFTUP, 0, 0)

# 根据状态，定义一个动作函数
def click_button_lift(posbase,offset,w,h):
    #取随机量
    posaim =(int(posbase[0]+offset[0]+w*(random.random()-0.5)*0.3),int(posbase[1]+offset[1]+h*(random.random()-0.5)*0.3))
    # 移动鼠标至指定位置
    pyautogui.moveTo(posaim[0],posaim[1])
    # 点击鼠标，仅在夜神模拟器实验成功
    pyautogui.click()

def click_action_yuhun(taskNow,yuhuncnt,status,posbase,offset,w,h):
    #引用的全局变量
    global statuslast
    #在探索界面点击进入,或刷新状态
    if status==yuhun_explore:
        if yuhuncnt>0:
            taskNow =taskYuhun
            click_button_lift(posbase,offset,w,h)
        else:
            taskNow = -1
    #在结算界面点击结束
    elif status==yuhun_end1 or status==yuhun_end2 or status==yuhun_ready:
        click_button_lift(posbase,offset,w,h)
    #在开始界面判断任务次数,顺带修正状态
    elif status==yuhun_begin:
        if yuhuncnt>0:
            click_button_lift(posbase,offset,w,h)
        else:
            taskNow = -1
            click_button_lift(posbase,[657,186],27,27)
    #在选择界面判断任务次数,并修正任务状态
    elif status==yuhun_choose:
        if yuhuncnt>0:
            taskNow =taskYuhun
            click_button_lift(posbase,[250,350],180,30)  #选择与开始界面不冲突的地方
        elif 0:
            taskNow = -1
            click_button_lift(posbase,[675,540],180,50)  #[675,540],180,50
    #从另外一个状态进入的战斗,任务次数削减1
    elif status==yuhun_combat and statuslast!=status:
        yuhuncnt =yuhuncnt-1

    #更新状态记录       
    statuslast =status
    #防止误操作这里休停2秒
    time.sleep(2)
    return taskNow,yuhuncnt

# 御魂相关图片识别并确定状态
def find_status_yuhun(taskNow,yuhuncnt,imsrc,posbase):
    #使用的临时状态量
    status = -1
    #检测是否处于战斗状态
    imobj =imobj_combat
    res =ac.find_template(imsrc,imobj)
    if res !=None and res['confidence']>confthreshold :
        status =yuhun_combat
    #检测是否在探索选择界面
    if status<0 :
        imobj =imobj_yuhun0
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =yuhun_explore
    #检测是否有开始按钮
    if status<0 :
        imobj =imobj_yuhun21
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =yuhun_begin
    #检测是否在选择界面       
    if status<0 :
        imobj =imobj_yuhun11
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =yuhun_choose
    #检测是否有准备按钮
    if status<0 :
        imobj =imobj_yuhun2R
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =yuhun_ready
    #检查结算界面1
    if status<0 :
        imobj =imobj_yuhun31
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =yuhun_end2
    #检查结算界面2        
    if status<0 :
        imobj =imobj_yuhun32
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =yuhun_end2
    # 从结果中读取坐标
    if status >=0 :
        offset =res['result']
        # 在目标范围内做一次随机取点
        rect =imobj.shape
        taskNow,yuhuncnt =click_action_yuhun(taskNow,yuhuncnt,status,posbase,offset,rect[0],rect[1])
    
    return taskNow,yuhuncnt



# 战斗状态目标匹配
imobj_combat  =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\obj_combat.png")
# 麒麟副本 源图待匹配目标读取
imobj_yuhun0  =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\obj_explore_yuhun.png")
imobj_yuhun11 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\yys_yuhun11_choose.png")
imobj_yuhun21 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\yys_yuhun21_begin.png")
imobj_yuhun2R =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\yys_yuhun28_ready.png")
imobj_yuhun31 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\yys_yuhun31_end.png")
imobj_yuhun32 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\yys_yuhun32_end.png")




