


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
taskTansuo =3

confthreshold   = 0.7
confthreshold_H = 0.91

#关于状态的定义
tansuo_combat    =2
tansuo_explore   =0
tansuo_begin     =11
tansuo_choose    =20
tansuo_ready     =28
tansuo_find      =30
tansuo_end       =33
tansuo_over1     =41
tansuo_over2     =42
statuslast       = -11


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

def click_action_tansuo(taskNow,tansuocnt,status,posbase,offset,w,h):
    #引用的全局变量
    global statuslast
    #在探索界面点击进入,或刷新状态
    if status==tansuo_explore:
        if tansuocnt>0:
            taskNow =taskTansuo
            click_button_lift(posbase,[722,422],110,40)   #默认选择25章节
        else:
            taskNow = -1
            click_button_lift(posbase,[36,72],33,27)      #默认返回庭院
    #在结算界面点击结束,或找到妖怪开战,或奖励小纸人
    elif status==tansuo_end or status==tansuo_ready or status==tansuo_choose or status==tansuo_over1:
        click_button_lift(posbase,offset,w,h)
    #小纸人奖励结算,需独立设置坐标
    elif status==tansuo_over2:
        click_button_lift(posbase,[520,160],99,99)
    #找不到妖怪移动主角
    elif status==tansuo_find:
        click_button_lift(posbase,[530,530],5,5)
    #在开始界面判断任务次数,顺带修正状态
    elif status==tansuo_begin:
        if tansuocnt>0 and statuslast!=tansuo_begin:
            statuslast =status
            taskNow    =taskTansuo
            tansuocnt  =tansuocnt-1
            click_button_lift(posbase,offset,w,h)
        else:
            taskNow = -1
            click_button_lift(posbase,[657,186],27,27)

    #更新状态记录       
    statuslast =status
    #防止误操作这里休停2秒
    time.sleep(2)
    return taskNow,tansuocnt

# 探索相关图片识别并确定状态
def find_status_tansuo(taskNow,tansuocnt,imsrc,posbase):
    #使用的临时状态量
    status = -1
    #检测是否处于战斗状态
    imobj =imobj_combat
    res =ac.find_template(imsrc,imobj)
    if res !=None and res['confidence']>confthreshold :
        status =tansuo_combat
    #检测是否在探索选择界面
    if status<0 :
        imobj =imobj_tansuo0
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =tansuo_explore
    #检测是否有开始按钮
    if status<0 :
        imobj =imobj_tansuo11
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =tansuo_begin
    #检测是否在选择界面       
    if status<0 :
        imobj =imobj_tansuo20
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =tansuo_choose
    if status<0 :
        imobj =imobj_tansuo21
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =tansuo_choose
    if status<0 :
        imobj =imobj_tansuo22
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =tansuo_choose
    #检测是否有准备按钮
    if status<0 :
        imobj =imobj_tansuo2R
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =tansuo_ready
    #检查结算界面1
    if status<0 :
        imobj =imobj_tansuo31
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =tansuo_end
    if status<0 :
        imobj =imobj_tansuo32
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =tansuo_end
    #检查是否在关卡结算界面
    if status<0 :
        imobj =imobj_tansuo41
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold_H :
            status =tansuo_over1
    if status<0 :
        imobj =imobj_tansuo42
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =tansuo_over2
    #如果无任何结果判断是否探索中
    if status<0 :
        imobj =imobj_tansuo30
        res =ac.find_template(imsrc,imobj)
        if res !=None and res['confidence']>confthreshold :
            status =tansuo_find

    # 从结果中读取坐标
    if status >=0 :
        offset =res['result']
        # 在目标范围内做一次随机取点
        rect =imobj.shape
        taskNow,tansuocnt =click_action_tansuo(taskNow,tansuocnt,status,posbase,offset,rect[0],rect[1])
    
    return taskNow,tansuocnt



# 战斗状态目标匹配
imobj_combat  =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\obj_combat.png")
# 探索副本 源图待匹配目标读取
imobj_tansuo0  =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\obj_explore_tansuo.png")
imobj_tansuo11 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\yys_tansuo11_begin.png")
imobj_tansuo20 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\yys_tansuo20_fight.png")
imobj_tansuo21 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\yys_tansuo21_fight.png")
imobj_tansuo22 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\yys_tansuo22_fight.png")
imobj_tansuo2R =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\yys_tansuo28_ready.png")
imobj_tansuo30 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\yys_tansuo30_find.png")
imobj_tansuo31 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\yys_tansuo31_end.png")
imobj_tansuo32 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\yys_tansuo32_end.png")
imobj_tansuo41 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\yys_tansuo41_over.png")
imobj_tansuo42 =ac.imread("C:\\Users\\ShiAokai\\Pictures\\yysm\\yys_tansuo42_over.png")




