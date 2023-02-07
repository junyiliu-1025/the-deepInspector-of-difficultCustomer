# -*- coding: utf-8 -*-
#face_client.py
#1. 匯入模組與類別
'''
import tkinter as tk
from tkinter import ttk
from tkinter import Canvas, PhotoImage
from PIL import Image, ImageTk

from face_function_client import images_path, sc_wd, sc_hi, img_hi, img_wd, text_wd, text_hi, bg
from face_function_client import file_exit, back_ground, close,face_flagup
from face_managing import management_window
from face_object import CreateToolTip

'''
import tkinter as tk
from tkinter import ttk
from tkinter import Canvas, PhotoImage,Frame
from tkinter import filedialog
from PIL import Image, ImageTk
from face_function_client import images_path, sc_wd, sc_hi, img_hi, img_wd, text_wd, text_hi, bg
from face_function_client import file_exit, back_ground, close
from face_managing import management_window
#from face_processing import select_window
#from face_model import model_window
from face_object import CreateToolTip
from face_prediction_client import prediction_client
import datetime,time
import os
import threading
import webbrowser

def run_face_mail():
    recipient = data['Recipient']
    subject = data['Subject']
    body = data['body_content']
    print(recipient,subject,body)
    webbrowser.open('mailto:?to=' + recipient + '&subject=' + subject + '&body=' + body, new=1)
    
#2. 定義元件之事件處理函數
def run_face_prediction_client():
    
    #os.popen('python face_prediction.py')
    # 建立一個子執行緒
    t = threading.Thread(target = prediction_client)
    
    # 執行該子執行緒
    t.start()
    
def file_model():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()
    if(file_path):
        print(file_path)
        
def run_face_oke():
    os.popen('python face_oke.py')
def run_face_value_set():
    os.popen('python face_value_set_client.py')
def read_file(file):
    project_var = []
    with open(file,'r',encoding='utf-8') as f:
        data = f.readlines()
        for i in data:
            data = i.strip('\n').split(':')
            project_var.append(data)
    return dict(project_var)
data = read_file('face_variable.txt')
#2. 定義元件之事件處理函數
#建立與確認檔案
file_exit()

#3. 建立最上層視窗, 設定標題與大小
root = tk.Tk()
root.title("頗有深度的奧客稽查員-Client")

icon = PhotoImage(file= images_path + 'AI_system.png')
root.tk.call('wm','iconphoto',root._w, icon)
#root.iconbitmap(images_path + 'ai.png')
#root.configure(background='#DDDDDD')

#window sc_wd, sc_hi from face_function
#背景 bg = "bg.jpg" from face_function


#color table
photo = Image.open(images_path + bg)
photo = photo.resize((sc_wd, sc_hi), Image.ANTIALIAS)
ph = ImageTk.PhotoImage(photo)

img_label = tk.Label(root,image=ph)  #图片
img_label.pack()

#1264,915 my_notebook
root.geometry('%sx%s'%(sc_wd, sc_hi))

# You have to use styles to customize ttk widgets.
#s = ttk.Style()
#s.configure('my.TButton', font=('Helvetica', 24), width=10, borderwidth=0, relief="raised", background='white')
bd = ttk.Style()
bd.configure('bd.TButton', borderwidth=0, relief="raised", background='white')

#back_ground(sc_wd, sc_hi, bg, rx, ry, rw, rh, fg)

pcanvas = back_ground(sc_wd, sc_hi, bg, 0.1, 0.04, sc_wd // 10 * 6 , sc_hi // 10 * 8, "prediction.png")
canvas = Canvas(root, bg="white", width = sc_wd // 10 * 6 , height = sc_hi // 10 * 8)
canvas.create_image( 3, 3, image=pcanvas, anchor=tk.NW)
canvas.place(relx=0.1,rely=0.04)

#button_click
pselet = back_ground(sc_wd, sc_hi, bg, 0.15, 0.88, text_wd, text_hi, "immediate_prediction.png")
selet = ttk.Button(root, text='即時預測', style='bd.TButton', image=pselet, command=run_face_prediction_client).place(relx=0.15,rely=0.88)

pvalue = back_ground(sc_wd, sc_hi, bg, 0.50, 0.88, text_wd, text_hi, "value_set.png")
value = ttk.Button(root, text='數值設定', style='bd.TButton', image=pvalue,command=run_face_value_set).place(relx=0.50,rely=0.88)

#4. 加入 tk/ttk 元件並指定事件處理函數
pf = back_ground(sc_wd, sc_hi, bg, 0.75, 0.04, img_wd, img_hi, "file_management.png")
file_management = ttk.Button(root, style='bd.TButton', image=pf, command=run_face_oke)
CreateToolTip(file_management, text='檔案管理')
file_management.place(relx=0.75,rely=0.04)

pb = back_ground(sc_wd, sc_hi, bg, 0.75, 0.32, img_wd, img_hi, "face_management.png")
face_management = ttk.Button(root, style='bd.TButton', image=pb, command=lambda:management_window(root))
CreateToolTip(face_management, text='綜合管理')
face_management.place(relx=0.75,rely=0.32)

pn = back_ground(sc_wd, sc_hi, bg, 0.75, 0.60, img_wd, img_hi, "notice_boss.png")
notice_boss = ttk.Button(root, style='bd.TButton', image=pn,command=run_face_mail)
CreateToolTip(notice_boss, text='通知主管')
notice_boss.place(relx=0.75,rely=0.60)

pe = back_ground(sc_wd, sc_hi, bg, 0.75, 0.88, text_wd, text_hi, "end.png")
end = ttk.Button(root, text='結束程式', style='bd.TButton',  image=pe, command=lambda:close(root)).place(relx=0.75,rely=0.88)

tt =  int(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
#print(today)
print(tt)

timer_face = []

def fun_timer():
    path = "faces\\suspects\\"
   
    # 读取path文件夹下所有文件的名字
    imagelist = os.listdir(path)
    images = []  # 先存储所有的图像的名称
    
    for imgname in imagelist:
            filemt = time.localtime(os.stat(path + imgname).st_mtime)
            f_tt = int(time.strftime('%Y%m%d%H%M%S',filemt))
            if f_tt - tt > 1: #大於今天
                #print(time.strftime('%Y%m%d%H%M%S',filemt))
                images.append(imgname)
                images.sort(reverse=True)  # 對讀取的路徑進行反排序
            if len(images) == 25:
                break
    
    k = 0.17
    j = 0.13
    
    for i in range(1,len(images)+1):
        img = Image.open(path + "/" + str(images[i - 1]))
        img = img.resize((120, 120), Image.ANTIALIAS)
        p = ImageTk.PhotoImage(img)
    
        b = tk.Label(root, text=images[i - 1], image=p, width=120, height=120)
        b.image = p # keep a reference!
        b.place(relx=k, rely=j)
        k += 0.092
        
        if (i % 5 == 0):
            k = 0.17
            j += 0.127

    global timer
    timer = threading.Timer(3, fun_timer) #每s
    timer.start()

timer = threading.Timer(1, fun_timer)
timer.start()

def fun_timer_del(): 
    
    for b in timer_face:
       del b #清理擷取圖
    timer_face.clear() #清理
    
    global timer_del
    timer_del = threading.Timer(10, fun_timer_del) #每s
    timer_del.start()
    
    
timer_del = threading.Timer(2, fun_timer_del)
timer_del.start()

#5. 啟始事件迴圈顯示視窗
root.resizable(width=False, height=False)
root.mainloop()
