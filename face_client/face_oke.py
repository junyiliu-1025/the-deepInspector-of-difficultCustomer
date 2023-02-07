#face_file_management.py
#1. 匯入模組與類別
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage,Canvas,Scrollbar,Frame,Text
from tkinter import END,DISABLED
#from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

from face_function_client import images_path, sub_wd, sub_hi, text_wd, text_hi, img_hi, img_wd
from face_function_client import back_ground, face_managing
from face_object import CreateToolTip
from face_socketClient import socket_Client,socket_Client_model
import os
import shutil
import datetime


# 引入字体模块
import tkinter.font as tkFont

#2. 定義元件之事件處理函數
def upload_window(kind, images, root, frm, cnv):
    global path_c
    
    if messagebox.askyesno("Upload", "確定上傳麼?", parent=root):
        # messagebox.showinfo("Yes", "上傳成功", parent=root)
        images.sort()  # 排序
        
        if(images):
            ##messagebox.showinfo("Upload", "上傳中(請稍後", parent=root)
            # 指定字体名称、大小、样式
            ft = tkFont.Font(size=16, weight=tkFont.BOLD)
            textbox = Text(root, font=ft, width=25, height=15, background='white')
            textbox.place(relx=0.715, rely=0.01) 
            ## Frame in textbox
            frmbox = Frame(textbox)
            ## Update display to get correct dimensions
            frmbox.update_idletasks()
            
            for file in images:
                socket_Client(kind,path_c+'/'+file)
                print(file)
                # 顯示圖片資訊
                textbox.insert(END," 圖片"+file[-10:]+"已上傳\n")
                os.remove(path_c+'/'+file)
                frmbox.update_idletasks()
                
            # 禁止輸入
            textbox.config(state=DISABLED)
            images.clear()    
            face_managing(path_c, images, root, frm, cnv)    
        else:
            messagebox.showinfo("Upload", "未選擇上傳之圖片", parent=root)
    else:
        messagebox.showinfo("No", "上傳取消", parent=root)

def upload_all(kind,root,frm,cnv):
    global path_c
    if messagebox.askyesno("Upload", "確定上傳麼?", parent=root):
        # messagebox.showinfo("Yes", "上傳成功", parent=root)
        foldername = os.listdir(path_c)
        files_folder = [i for i in foldername]
        files_folder.sort()  # 排序
        
        if(files_folder):
            ##messagebox.showinfo("Upload", "上傳中(請稍後", parent=root)
            # 指定字体名称、大小、样式
            ft = tkFont.Font(size=16, weight=tkFont.BOLD)
            textbox = Text(root, font=ft, width=25, height=15, background='white')
            textbox.place(relx=0.715, rely=0.01) 
            ## Frame in textbox
            frmbox = Frame(textbox)
            ## Update display to get correct dimensions
            frmbox.update_idletasks()
            
            for file in files_folder:
                socket_Client(kind,path_c+'/'+file)
                print(file)
                # 顯示圖片資訊
                textbox.insert(END," 圖片"+file[-10:]+"已上傳\n")
                os.remove(path_c+'/'+file)
                frmbox.update_idletasks()
                
            # 禁止輸入
            textbox.config(state=DISABLED)
            files_folder.clear()    
            face_managing(path_c, files_folder, root, frm, cnv)
        else:
            messagebox.showinfo("Upload", "未選擇上傳之圖片", parent=root)
    else:
        messagebox.showinfo("No", "上傳取消", parent=root)
        
def change_path(path, arry, root, frm, cnv):
    global path_c,kind
    path_c = path
    if path == './faces/train/okes':
        kind = '1'
    else:
        kind = '2'
    face_managing(path_c, arry, root, frm, cnv)   
    
def run_face_unoke(root):
    os.popen('python face_unoke.py')
    root.withdraw()

arry = []
global path_c
path_c = './faces/train/okes'
kind = '1'
def close():
    arry.clear()
    root.destroy()

## Main window
root = tk.Tk()
root.title("頗有深度的奧客稽查員-奧客檔案管理")

icon = PhotoImage(file= images_path + 'AI_system.png')
root.tk.call('wm','iconphoto',root._w, icon)
# root.configure(background='#DDDDDD')
root.geometry('%sx%s' % (sub_wd, sub_hi))

## Grid sizing behavior in window
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

## Canvas
cnv = Canvas(root)
cnv.grid(row=0, column=0, sticky='nswe')
vScroll = Scrollbar(root, command=cnv.yview)
vScroll.grid(row=0, column=1, sticky='ns')
cnv.configure(yscrollcommand=vScroll.set)

# color Canvas
bg = "bg3.png"
photo = Image.open(images_path + bg)
photo = photo.resize((sub_wd, sub_hi), Image.ANTIALIAS)
ph = ImageTk.PhotoImage(photo)
img_label = tk.Label(cnv, image=ph)  # 图片
img_label.pack(padx=10,pady=0)

## Frame in canvas
frm = Frame(cnv)
frm.config(bg='#DDDDDD')

## This puts the frame in the canvas's scrollable zone
cnv.create_window(0, 0, window=frm, anchor='nw')

pm = back_ground(sub_wd, sub_hi, bg, 0.755, 0.2, img_wd, img_hi, "model_download.png")
face_model = ttk.Button(root, style='bd.TButton', image=pm,command=lambda:socket_Client_model(root))
CreateToolTip(face_model, text='下載模型')
face_model.place(relx=0.75, rely=0.2)
'''     
pok = back_ground(sub_wd, sub_hi, bg, 0.755, 0.605, text_wd, text_hi, "oke_file.png")
pok_picture = ttk.Button(root, text="奧客檔案", style='bd.TButton', image=pok,command=lambda:change_path('./faces/train/okes', arry, root, frm, cnv))
pok_picture.place(relx=0.75, rely=0.60)
'''
punok = back_ground(sub_wd, sub_hi, bg, 0.755, 0.605, text_wd, text_hi, "unoke_file.png")
punok_picture = ttk.Button(root, text="非奧客檔", style='bd.TButton', image=punok,command=lambda:run_face_unoke(root))
punok_picture.place(relx=0.75, rely=0.60)


pt = back_ground(sub_wd, sub_hi, bg, 0.755, 0.705, text_wd, text_hi, "total_upload.png")
total_upload_picture = ttk.Button(root, text="全圖上傳", style='bd.TButton', image=pt,command=lambda:upload_all(kind,root,frm,cnv))
total_upload_picture.place(relx=0.75, rely=0.70)

pu = back_ground(sub_wd, sub_hi, bg, 0.755, 0.805, text_wd, text_hi, "upload_picture.png")
upload_picture = ttk.Button(root, text="上傳圖片", style='bd.TButton', image=pu, command=lambda:upload_window(kind,arry,root,frm,cnv))
upload_picture.place(relx=0.75, rely=0.80)

pe = back_ground(sub_wd, sub_hi, bg, 0.755, 0.905, text_wd, text_hi, "exit_window.png")
exit_window = ttk.Button(root, text="關閉視窗", style='bd.TButton', image=pe, command=close)
exit_window.place(relx=0.75,rely=0.90)

#face_function_client
face_managing(path_c, arry, root, frm, cnv)
     




