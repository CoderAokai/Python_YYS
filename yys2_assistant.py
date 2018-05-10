
'''
2.0及以上版本试图实现多文件函数
'''




from yys2_function import *




# 假定一个初始状态，但随后被更新了
statusNow =-1

while(hwnd != None) :
    # 记录时间
    begin_time =time.time()
    # 截取指定位置屏幕并保存
    img =ImageGrab.grab(posbase)
    img.save("\\yysm\\yys_src.png")
    # 读取源图以及待匹配目标
    imsrc =ac.imread("\\yysm\\yys_src.png")
    # 获取目标相对位置
    statusNow,posaim =find_status_yuhun(statusNow,imsrc)
    # 记录一下时间 以供参考
    end_time =time.time()
    if statusNow>=0 :  
        print("Use time:",end_time-begin_time,statusNow)
    # 确定执行何种动作
    click_action(statusNow,posaim)