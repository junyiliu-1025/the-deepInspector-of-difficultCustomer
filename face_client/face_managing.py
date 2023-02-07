#face_mangaging.py
#1. 匯入模組與類別
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
#from tkinter import *
from PIL import Image, ImageTk

from face_function_client import images_path, sub_wd, sub_hi, img_hi, img_wd
from face_function_client import button_img, back_ground, add_window, add_delete_window,close
from face_object import CreateToolTip
from face_recognize import face_recognition_window
import os

#2. 定義元件之事件處理函數
def file_suspects():
    os.popen("start faces")
    #os.system("nautilus faces/suspects")

def file_oke():
    os.popen("start faces\\train\\okes")

def file_unoke():
    os.popen("start faces\\train\\unokes")

def run_face_event():
    os.popen('python face_event.py')
    
def run_face_recognize():
    os.popen('python face_recognize.py')
    
def management_window(toproot):
    # 3. 建立最上層視窗, 設定標題與大小
    root = tk.Toplevel()
    root.title("頗有深度的奧客稽查員-綜合管理")
    icon = PhotoImage(file= images_path + 'AI_system.png')
    root.tk.call('wm','iconphoto',root._w, icon)
    root.configure(background='#DDDDDD')
    root.geometry('%sx%s' % (sub_wd, sub_hi))
    # color table
    bg = "bg2.png"
    photo = Image.open(images_path + bg)
    photo = photo.resize((sub_wd, sub_hi), Image.ANTIALIAS)
    ph = ImageTk.PhotoImage(photo)

    #window background
    img_label = tk.Label(root, image=ph)  # 图片
    img_label.pack()

    suspects = "faces/suspects"
    okes ="faces/train/okes"
    unokes ="faces/train/unokes"

    # 4. 加入 tk/ttk 元件並指定事件處理函數
    # back_ground(sc_wd, sc_hi, bg, rx, ry, rw, rh, fg)
    
    of = button_img(images_path + "oke.png")
    oke_file = ttk.Button(root, style='bd.TButton', image=of, command=file_oke)
    CreateToolTip(oke_file, text='奧客檔案')
    oke_file.place(relx=0.12,rely=0.05)
    
    oad = back_ground(sub_wd, sub_hi, bg, 0.12, 0.35, img_wd, img_hi, "add_delete.png")
    oke_add = ttk.Button(root, style='bd.TButton', image=oad, command=lambda:add_delete_window(bg,okes,"頗有深度的奧客稽查員-奧客管理",suspects))
    CreateToolTip(oke_add, text='奧客管理')
    oke_add.place(relx=0.12,rely=0.35)

    
    em = back_ground(sub_wd, sub_hi, bg, 0.12, 0.65, img_wd, img_hi, "event_management.png")
    event_management = ttk.Button(root, style='bd.TButton', image=em,command=run_face_event)
    CreateToolTip(event_management, text='事件管理')
    event_management.place(relx=0.12,rely=0.65)
     
    uf = button_img(images_path + "unoke.png")
    unoke_file = ttk.Button(root, style='bd.TButton', image=uf, command=file_unoke)
    CreateToolTip(unoke_file, text='非奧客檔案')
    unoke_file.place(relx=0.42,rely=0.05)
    
    uad = back_ground(sub_wd, sub_hi, bg, 0.42, 0.35, img_wd, img_hi, "add_delete.png")
    unoke_add = ttk.Button(root, style='bd.TButton', image=uad, command=lambda:add_delete_window(bg,unokes,"頗有深度的奧客稽查員-非奧客管理",suspects))
    CreateToolTip(unoke_add, text='非奧客管理')
    unoke_add.place(relx=0.42,rely=0.35)
 
    oi = back_ground(sub_wd, sub_hi, bg, 0.42, 0.65, img_wd, img_hi, "oke_identify.png")
    oke_identify = ttk.Button(root, style='bd.TButton', image=oi,command=face_recognition_window)
    CreateToolTip(oke_identify, text='奧客管理')
    oke_identify.place(relx=0.42,rely=0.65)
    
    sf = back_ground(sub_wd, sub_hi, bg, 0.72, 0.05, img_wd, img_hi, "suspect.png")
    suspect_file = ttk.Button(root, style='bd.TButton', image=sf, command=file_suspects)
    CreateToolTip(suspect_file, text='資料檔案')
    suspect_file.place(relx=0.72, rely=0.05)
    
    sd = back_ground(sub_wd, sub_hi, bg, 0.72, 0.35, img_wd, img_hi, "delete.png")
    suspect_delet = ttk.Button(root, style='bd.TButton', image=sd, command=lambda:add_window(bg,suspects,"頗有深度的奧客稽查員-人臉之管理",""))
    CreateToolTip(suspect_delet, text='人臉之管理')
    suspect_delet.place(relx=0.72, rely=0.35)

    ex = back_ground(sub_wd, sub_hi, bg, 0.72, 0.65, img_wd, img_hi, "exit.png")
    exit = ttk.Button(root, style='bd.TButton', image=ex, command=lambda:close(root))
    CreateToolTip(exit, text='結束程式')
    exit.place(relx=0.72,rely=0.65)

    # 5. 啟始事件迴圈顯示視窗
    root.resizable(width=False, height=False)
    root.mainloop()
    
    