#face_login.py
#1. 匯入模組與類別
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage,messagebox,VERTICAL
from PIL import Image, ImageTk
#from change import change
from addnewdata import addnewdata,change
from face_socketClient import socket_Client_confirm
from face_function_client import images_path, sc_wd, sc_hi, img_hi, img_wd, text_wd, text_hi
from face_function_client import back_ground, close
from face_object import CreateToolTip

from csvfuntion import array, nullplace, load_and_tmp, printdata,delete_new

import os 

test_infor=0


#2. 定義元件之事件處理函數

#3. 建立最上層視窗, 設定標題與大小
root = tk.Tk()
root.title("頗有深度的奧客稽查員-事件管理")

icon = PhotoImage(file= images_path + 'AI_system.png')
root.tk.call('wm','iconphoto',root._w, icon)
#root.iconbitmap(images_path + 'ai.png')
#root.configure(background='#DDDDDD')

#window sc_wd, sc_hi from face_function_client
bg = "bg0.png" #背景
event_wd = int(sc_wd // 5 * 4)
event_hi = int(sc_hi // 10 * 7)

#color table
photo = Image.open(images_path + bg)
photo = photo.resize((event_wd, event_hi), Image.ANTIALIAS)
ph = ImageTk.PhotoImage(photo)

img_label = tk.Label(root,image=ph)  #图片
img_label.pack()

#1264,915 my_notebook
root.geometry('%sx%s'%(event_wd, event_hi))

# You have to use styles to customize ttk widgets.
bd = ttk.Style()
bd.configure('bd.TButton', borderwidth=0, relief="raised", background='white')


#4. 加入 tk/ttk 元件並指定事件處理函數
p_obr = back_ground(event_wd, event_hi, bg, 0.18, 0.05, text_wd//2*3, text_hi//5*4, "oke_behavior_record.png")
oke_br = ttk.Button(root, style='bd.TButton', image=p_obr)
oke_br.place(relx=0.18,rely=0.05)

load_and_tmp("oke")
printdata("oke")

#oke_click_event

# 指定字体名称、大小、样式
style = ttk.Style()
style.configure("Treeview.Heading", font=('Verdana', 18))
style.configure("Treeview",  rowheight=40, font=('Verdana', 18)) #SOLUTION

global item_text_oke
item_text_oke=[]

def treeviewClick_oke(event):#單擊
    global oke_treeview
    global item_text_oke
    item_text_oke=[]
    for item in oke_treeview.selection():
        item_text_oke = oke_treeview.item(item,"values")
        print(item_text_oke[0])#輸出所選行的第一列的值


def creat_treeview_oke():
    #创建Listbox
    global oke_treeview
    columns=("ID","Behavior")
    oke_treeview = ttk.Treeview(root, height=5, show="headings", columns=columns) #表格 
    oke_vbar = ttk.Scrollbar(root, orient=VERTICAL, command=oke_treeview.yview) #表格的滾軸
    oke_treeview.configure(yscrollcommand = oke_vbar.set)
    
    oke_treeview.column('ID', width=180, anchor='center') 
    oke_treeview.column('Behavior', width=300, anchor='center') 
    oke_treeview.heading('ID',text=array[0][0][0])
    oke_treeview.heading('Behavior', text=array[0][0][1])
    
    count_oke=0
    for i in range(len(array[0])):
        
        if i == 0:
            continue
        if array[0][i][0] == '':
            continue
        oke_treeview.insert('',count_oke,values=(array[0][i][0], array[0][i][1]))
        count_oke+=1
    oke_treeview.bind('<ButtonRelease-1>', treeviewClick_oke)#繫結單擊離開事件===========
    
    oke_treeview.place(relx=0.1,rely=0.15)
    
creat_treeview_oke()

def change_oke():
    global item_text_oke
    if len(item_text_oke) == 0:
        messagebox.showinfo("提示", "請點選想修改之值", parent=root)
    else:
        print(item_text_oke)
        change("oke",int(item_text_oke[0]),item_text_oke[1])
        reload_oke()
def add_oke(root):
    addnewdata("oke",root)
    reload_oke()
    
def reload_oke():
    array[0]=[]
    nullplace[0]=[]
    load_and_tmp("oke")
    printdata("oke")
    creat_treeview_oke()
    
def delete_oke(root):
    global item_text_oke
    if len(item_text_oke) == 0:
        messagebox.showinfo("提示", "請點選想刪除之值", parent=root)
    else:
        if messagebox.askyesno('刪除','是否確定刪除該數值', parent=root) :
            print(item_text_oke)
            delete_new("oke",int(item_text_oke[0]))
            reload_oke()
            item_text_oke=[]
        else:
            messagebox.showinfo("No", "取消刪除", parent=root)
        
        
        
p_ab = back_ground(event_wd, event_hi, bg, 0.60, 0.15, text_wd, text_hi//5*4, "add_behavior.png")
add_behavior = ttk.Button(root, style='bd.TButton', image=p_ab,command=lambda:add_oke(root))
add_behavior.place(relx=0.60,rely=0.15)

p_db = back_ground(event_wd, event_hi, bg, 0.60, 0.27, text_wd, text_hi//5*4, "delete_behavior.png")
delete_behavior = ttk.Button(root, style='bd.TButton', image=p_db,command=lambda:delete_oke(root))
delete_behavior.place(relx=0.60,rely=0.27)

p_cb = back_ground(event_wd, event_hi, bg, 0.60, 0.39, text_wd, text_hi//5*4, "change_behavior.png")
change_behavior = ttk.Button(root, style='bd.TButton', image=p_cb,command=change_oke)
change_behavior.place(relx=0.60,rely=0.39)

p_rr = back_ground(event_wd, event_hi, bg, 0.18, 0.52, text_wd//2*3, text_hi//5*4, "response_record.png")
response_r = ttk.Button(root, style='bd.TButton', image=p_rr)
response_r.place(relx=0.18,rely=0.52)

load_and_tmp("adv")
printdata("adv")

global item_text_adv
item_text_adv=[]

def treeviewClick_adv(event):#單擊
    global adv_treeview
    global item_text_adv
    item_text_adv=[]
    for item in adv_treeview.selection():
        item_text_adv = adv_treeview.item(item,"values")
        print(item_text_adv[0])#輸出所選行的第一列的值

def creat_treeview_adv():
    #创建Listbox
    global adv_treeview
    columns=("ID","Response")
    adv_treeview = ttk.Treeview(root, height=5, show="headings", columns=columns) #表格 
    adv_vbar = ttk.Scrollbar(root, orient=VERTICAL, command=adv_treeview.yview) #表格的滾軸
    adv_treeview.configure(yscrollcommand = adv_vbar.set)
    
    adv_treeview.column('ID', width=180, anchor='center') 
    adv_treeview.column('Response', width=300, anchor='center') 
    adv_treeview.heading('ID',text=array[1][0][0])
    adv_treeview.heading('Response', text=array[1][0][1])
    
    for i in range(len(array[1])):
        if i == 0:
            continue
        if array[1][i][0] == '':
            continue
        adv_treeview.insert('', i,values=(array[1][i][0], array[1][i][1]))
    
    adv_treeview.bind('<ButtonRelease-1>', treeviewClick_adv)#繫結單擊離開事件===========
    
    adv_treeview.place(relx=0.1,rely=0.62)

creat_treeview_adv()

def reload_adv():
    array[1]=[]
    nullplace[1]=[]
    load_and_tmp("adv")
    printdata("adv")
    creat_treeview_adv()

def change_adv():
    global item_text_adv
    if len(item_text_adv) == 0:
        messagebox.showinfo("提示", "請點選想修改之值", parent=root)
    else:
        print(item_text_adv)
        change("adv",int(item_text_adv[0]),item_text_adv[1])
        reload_adv()

def add_adv(root):
    addnewdata("adv",root)
    reload_adv()

def delete_adv(root):
    if messagebox.askyesno('刪除','是否確定刪除該數值', parent=root) :
        global item_text_adv
        print(item_text_adv)
        delete_new("adv",int(item_text_adv[0]))
        item_text_adv=[]
        reload_adv()

    else:
        messagebox.showinfo("No", "取消刪除", parent=root)

#adv_vbar.place(relx=0.1,rely=0.6)
#treeview.grid(row=2, column=0, columnspan=1, sticky="NSEW")
#vbar.grid(row=2, column=1, sticky="NS")
p_am = back_ground(event_wd, event_hi, bg, 0.60, 0.62, text_wd, text_hi//5*4, "add_method.png")
add_method = ttk.Button(root, style='bd.TButton', image=p_am,command=lambda:add_adv(root))
add_method.place(relx=0.60,rely=0.62)

p_dm = back_ground(event_wd, event_hi, bg, 0.60, 0.74, text_wd, text_hi//5*4, "delete_method.png")
delete_method = ttk.Button(root, style='bd.TButton', image=p_dm,command=lambda:delete_adv(root))
delete_method.place(relx=0.60,rely=0.74)

p_cm = back_ground(event_wd, event_hi, bg, 0.60, 0.86, text_wd, text_hi//5*4, "change_method.png")
change_method = ttk.Button(root, style='bd.TButton', image=p_cm,command=change_adv)
change_method.place(relx=0.60,rely=0.86)

pc = back_ground(event_wd, event_hi, bg, 0.82, 0.38, img_wd//5*4, img_hi//5*4, "exit.png")
system_close = ttk.Button(root, style='bd.TButton', image=pc, command=lambda:close(root))
CreateToolTip(system_close, text='離開視窗')
system_close.place(relx=0.82,rely=0.38)




#5. 啟始事件迴圈顯示視窗
root.resizable(width=False, height=False)
root.mainloop()
