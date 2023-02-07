# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 01:03:44 2019

@author: chun8
"""

#face_login.py
#1. 匯入模組與類別
import tkinter as tk
import socket
from tkinter import ttk
from tkinter import PhotoImage,messagebox,Text,END
from PIL import Image, ImageTk

from face_function import images_path, sc_wd, sc_hi, img_hi, img_wd, text_wd, text_hi
from face_function import back_ground, close
from face_object import CreateToolTip

# 引入字体模块
import tkinter.font as tkFont

import os 

#2. 定義元件之事件處理函數
def file_client_run():
    os.popen("python face_client.py")


def read_file(file):
    project_var = []
    with open(file,'r',encoding='utf-8') as f:
        data = f.readlines()
        for i in data:
            data = i.strip('\n').split(':')
            project_var.append(data)
    return dict(project_var)

def change_variables(file,old,new): 
    file_data = ""
    with open(file,'r+',encoding='utf-8') as f:
        for line in f.readlines():
            if(line.find(old+':')==0):
                line = old+':%s' % (new) + '\n'
            file_data += line
    with open(file,"w+",encoding='utf-8') as f:
        f.write(file_data)

def save_setcomplete(ip,warning,aumin,aumax):
    if aumin.replace(' ','') == '' or aumax.replace(' ','') == '' or warning.replace(' ','') == '':
        messagebox.showinfo('頗有深度的奧客稽查員','數值請不要留空白')
    elif int(aumin) > int(aumax) or int(aumin) <0 or int(aumax)>100 or int(warning) < 0 or int(warning) > 100:
        messagebox.showinfo('頗有深度的奧客稽查員','請輸入正確範圍')
    elif aumin.isdigit() or aumax.isdigit():
        messagebox.showinfo('頗有深度的奧客稽查員','請輸入正確格式')
    else:
        messagebox.showinfo('頗有深度的澳客稽查員','修改成功')
        with open('face_variable.txt','w') as f:
            f.write('oke_warning:'+str(warning)+'\naut_capture_min:'+str(aumin)+'\naut_capture_max:'+str(aumax))

def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ss.connect(('8.8.8.8', 80))
        ip = ss.getsockname()[0]
    finally:
        ss.close()

    return ip

#file_client_run()
data = read_file('face_variable.txt')

#3. 建立最上層視窗, 設定標題與大小
root = tk.Tk()
root.title("頗有深度的奧客稽查員-數值設定")

icon = PhotoImage(file= images_path + 'AI_system.png')
root.tk.call('wm','iconphoto',root._w, icon)
#root.iconbitmap(images_path + 'ai.png')
#root.configure(background='#DDDDDD')

#window sc_wd, sc_hi from face_function_client
bg = "bg4.png" #背景
login_wd = int(sc_wd // 10 * 6)
login_hi = int(sc_hi // 5 * 2)

#color table
photo = Image.open(images_path + bg)
photo = photo.resize((login_wd, login_hi), Image.ANTIALIAS)
ph = ImageTk.PhotoImage(photo)

img_label = tk.Label(root,image=ph)  #图片
img_label.pack()

#1264,915 my_notebook
root.geometry('%sx%s'%(login_wd, login_hi))

# You have to use styles to customize ttk widgets.
#s = ttk.Style()
#s.configure('my.TButton', font=('Helvetica', 24), width=10, borderwidth=0, relief="raised", background='white')
bd = ttk.Style()
bd.configure('bd.TButton', borderwidth=0, relief="raised", background='white')

style = ttk.Style()
style.configure('Test.TLabel', background= 'white') 

#button_click

#4. 加入 tk/ttk 元件並指定事件處理函數
#back_ground(sc_wd, sc_hi, bg, rx, ry, rw, rh, fg)
#ip = tk.Text(root,height=3,width=10)

ip_label = ttk.Label(root,font=('Verdana',20), style='Test.TLabel', text=" Server IP: ")
ip_label.place(relx=0.15,rely=0.05)
ip_address = tk.StringVar(value=get_host_ip())
ip = ttk.Entry(root,font=('Verdana',20),textvariable=ip_address, state='disabled')
ip.place(relx=0.35,rely=0.05)


# 指定字体名称、大小、样式

#body_data = tk.StringVar(value="在嘉義市南京路分店第8桌有需要處理的顧客")


oke_warning = ttk.Label(root,font=('Verdana',20), style='Test.TLabel', text=" 奧客警告值: ")
oke_warning.place(relx=0.15,rely=0.25)

warning_data = tk.StringVar(value=data['oke_warning'])
warning_value = ttk.Entry(root,font=('Verdana',20),textvariable = warning_data, width = 4)
warning_value.place(relx=0.35,rely=0.25)

aut_capture = ttk.Label(root,font=('Verdana',20), style='Test.TLabel', text=" 自動擷取範圍設定 ")
aut_capture.place(relx=0.15,rely=0.45)

min_Label = ttk.Label(root,font=('Verdana',20), style='Test.TLabel', text=" 數值小於: ")
min_Label.place(relx=0.15,rely=0.65)
min_value = tk.StringVar(value=data['aut_capture_min'])
min_entry =  ttk.Entry(root,font=('Verdana',20),textvariable = min_value, width = 4)
min_entry.place(relx=0.35,rely=0.65)

max_Label = ttk.Label(root,font=('Verdana',20), style='Test.TLabel', text=" 數值大於: ")
max_Label.place(relx=0.15,rely=0.85)
max_value = tk.StringVar(value=data['aut_capture_max'])
max_entry =  ttk.Entry(root,font=('Verdana',20),textvariable = max_value, width = 4)
max_entry.place(relx=0.35,rely=0.85)

#body_data = tk.StringVar(value="有奧客出現，請求現場協助")
#body_content = ttk.Entry(root,font=('Verdana',20),textvariable = subject_data)
#body_content.place(relx=0.35,rely=0.50)


#pl = back_ground(login_wd, login_hi, bg, 0.16, 0.83, img_wd, img_hi //5 * 2, "login.png")
#system_login = ttk.Button(root, style='bd.TButton', image=pl,command=lambda:socket_Client_confirm(ip.get(),root))
#system_login.place(relx=0.16,rely=0.83)

p_sf = back_ground(login_wd, login_hi, bg, 0.7, 0.30, text_wd//7*6, text_hi//7*6, "set_finish.png")
set_f = ttk.Button(root, style='bd.TButton', image=p_sf, command=lambda:save_setcomplete(ip.get(), warning_value.get(),
                                                                                         min_entry.get(),max_entry.get()) )
set_f.place(relx=0.7,rely=0.30)

pc = back_ground(login_wd, login_hi, bg, 0.7, 0.7, img_wd//7*6, img_hi//7*6, "exit.png")
system_close = ttk.Button(root, style='bd.TButton', image=pc, command=lambda:close(root))
CreateToolTip(system_close, text='離開視窗')
system_close.place(relx=0.7,rely=0.5)

#5. 啟始事件迴圈顯示視窗
root.resizable(width=False, height=False)
root.mainloop()
