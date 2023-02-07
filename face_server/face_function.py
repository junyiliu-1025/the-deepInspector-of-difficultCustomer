#face_function.py
#1. 匯入模組與類別
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage,Canvas, Scrollbar, Frame
from tkinter import messagebox
from PIL import Image, ImageTk

import os
import shutil
import screeninfo
import datetime

#window
screen = screeninfo.get_monitors()[0]
sc_wd =int(screen.width // 10 * 7)
sc_hi =int(screen.height // 10 * 9)

#sub_window
sub_wd = 1250
sub_hi = 800

#img_button
img_wd = 200
img_hi = 200

#text_button
text_wd = 200
text_hi = 60

#face_button
face_wd = 180
face_hi = 180

#train data
data_wd = 92
data_hi = 112

#pictures_path
images_path = "images/"

# 背景
bg = "bg1.png"

    
#2. 定義元件之事件處理函數
def close(root):
	root.destroy()

def mkdir(file):
    folder = os.path.exists(file)
    # 判断是否存在文件夹如果不存在则创建为文件夹
    if not folder:
        # makedirs 创建文件时如果路径不存在会创建这个路径
        os.makedirs(file)
        print("建立資料夾%s" % file)
    else:
        print(str(file)+ "資料夾已存在")

def file_exit():
    # 臉部目錄
    file = "faces"
    mkdir(file)
    # 未擷取目錄
    file = "faces/unfaces"
    mkdir(file)
    # 嫌疑人資料夾
    file = "faces/suspects"
    mkdir(file)
    # 訓練資料夾
    file = "faces/train"
    mkdir(file)
    # 奧客資料夾
    file = "faces/train/okes"
    mkdir(file)
    # 非奧客資料夾
    file = "faces/train/unokes"
    mkdir(file)
    # 模型目錄
    file = "models"
    mkdir(file)
    # 圖片目錄
    file = "images_client"
    mkdir(file)
#不必去背圖
def button_img(path):
    img = Image.open(path)
    img = img.resize((img_wd, img_hi), Image.ANTIALIAS)
    p = ImageTk.PhotoImage(img)
    return p

#去背圖
def back_ground(sc_wd, sc_hi, bg, rx, ry, rw, rh, fg):
        # 加载原始图片
        bg_img = Image.open(images_path + bg)
        bg_img = bg_img.resize((sc_wd, sc_hi), Image.ANTIALIAS)
        # bg_img.show()

        # 裁切區域的相對位置
        x = int(sc_wd * rx) + 5
        y = int(sc_hi * ry) + 5

        # 裁切區域的長度與寬度
        w = rw
        h = rh

        # 裁切 左上右下
        background = bg_img.crop((x, y, x + w, y + h))
        background = background.resize((w, h), Image.ANTIALIAS)

        # 素材
        foreground = Image.open(images_path +fg)
        foreground = foreground.resize((w, h), Image.ANTIALIAS)

        # 合成
        background.paste(foreground, (0, 0), foreground)
        background = background.resize((rw, rh), Image.ANTIALIAS)
        p = ImageTk.PhotoImage(background)
        # background.show()
        return p

def add_window(bg, path, title, root):
    add = []
    
    if root != "": #關閉自己
        root.destroy()
    
    def close():
        add.clear()
        sub_root.destroy()
        
    def os_add(dst):
        if messagebox.askyesno("Add", "確定新增麼?",parent=sub_root):
            #messagebox.showinfo("Yes", "刪除成功", parent=sub_root)
            if(add):
                for img in add:
                    t = datetime.datetime.now().strftime('%Y_%m_%d_%H-%M-%S-%f')
                    face = Image.open("faces\\suspects\\" + img)
                    face.save(dst + "/" + t + ".bmp")  #儲存至指定之資料夾
                    os.remove(path + "/%s" % img)  #移除
                add.clear()
                face_managing(path, add, sub_root, frm, cnv)
            else:
                messagebox.showinfo("Add", "未選擇新增之圖片", parent=sub_root)
        else:
            messagebox.showinfo("No", "新增取消", parent=sub_root)
    
    def os_remove():
        if messagebox.askyesno("Delete", "確定刪除麼?",parent=sub_root):
            #messagebox.showinfo("Yes", "刪除成功", parent=sub_root)
            if(add):
                for img in add:
                    os.remove(path + "/%s" % img)
                add.clear()
                face_managing(path, add, sub_root, frm, cnv)
            else:
                messagebox.showinfo("Delete", "未選擇刪除之圖片", parent=sub_root)
        else:
            messagebox.showinfo("No", "刪除取消",parent=sub_root)
     
    ## Main window
    sub_root = tk.Toplevel()
    sub_root.title("%s" %title)
    #sub_root.configure(background='#DDDDDD')
    sub_root.geometry('%sx%s' % (sub_wd, sub_hi))
    
    icon = PhotoImage(file= images_path + 'AI_system.png')
    sub_root.tk.call('wm','iconphoto',sub_root._w, icon)
    
    ## Grid sizing behavior in window
    sub_root.grid_rowconfigure(0, weight=1)
    sub_root.grid_columnconfigure(0, weight=1)

    ## Canvas
    cnv = Canvas(sub_root)
    cnv.grid(row=0, column=0, sticky='nswe')
    vScroll = Scrollbar(sub_root, command=cnv.yview)
    vScroll.grid(row=0, column=1, sticky='ns')
    cnv.configure(yscrollcommand=vScroll.set)

    # color Canvas
    photo = Image.open(images_path + bg)
    photo = photo.resize((sub_wd, sub_hi), Image.ANTIALIAS)
    ph = ImageTk.PhotoImage(photo)
    img_label = tk.Label(cnv, image=ph)  # 图片
    img_label.pack()

    ## Frame in canvas
    frm = Frame(cnv)
    frm.config(bg='#DDDDDD')

    ## This puts the frame in the canvas's scrollable zone
    cnv.create_window(0, 0, window=frm, anchor='nw')

    p_oke = back_ground(sc_wd, sc_hi, bg, 0.80, 0.60, text_wd, text_hi, "add_oke.png")
    add_oke = ttk.Button(sub_root, text=" 加奧客", style='bd.TButton', image=p_oke, command=lambda:os_add("faces\\train\\okes"))
    add_oke.place(relx=0.80, rely=0.60)
    
    p_unoke = back_ground(sc_wd, sc_hi, bg, 0.80, 0.70, text_wd, text_hi, "add_unoke.png")
    add_unoke = ttk.Button(sub_root, text="加非奧客", style='bd.TButton', image=p_unoke, command=lambda:os_add("faces\\train\\unokes"))
    add_unoke.place(relx=0.80, rely=0.70)
    
    pd = back_ground(sc_wd, sc_hi, bg, 0.80, 0.80, text_wd, text_hi, "delete_picture.png")
    delete_picture = ttk.Button(sub_root, text="刪除圖片", style='bd.TButton', image=pd, command=os_remove)
    delete_picture.place(relx=0.80, rely=0.80)
    
    pe = back_ground(sc_wd, sc_hi, bg, 0.80, 0.90, text_wd, text_hi, "exit_window.png")
    exit_window = ttk.Button(sub_root, text="關閉視窗", style='bd.TButton', image=pe, command=close)
    exit_window.place(relx=0.80, rely=0.90)

    face_managing(path, add, sub_root, frm, cnv)


def add_delete_window(bg, path, title, dst):
    remove = []

    def close():
        remove.clear()
        root.destroy()
    
    def os_remove():
        if messagebox.askyesno("Delete", "確定刪除麼?",parent=root):
            #messagebox.showinfo("Yes", "刪除成功", parent=root)
            if(remove):
                for img in remove:
                    os.remove(path + "/%s" % img)
                remove.clear()
                face_managing(path, remove, root, frm, cnv)
            else:
                messagebox.showinfo("Delete", "未選擇刪除之圖片", parent=root)
        else:
            messagebox.showinfo("No", "刪除取消",parent=root)
    
    def os_move():
        if messagebox.askyesno("Move", "確定移動麼?", parent=root):
            # messagebox.showinfo("Yes", "移動成功", parent=root)
            if(remove):
                for img in remove:
                    shutil.move(path + "/%s" % img, dst)
                remove.clear()
                face_managing(path, remove, root, frm, cnv)
            else:
                messagebox.showinfo("Move", "未選擇移動之圖片", parent=root)
        else:
            messagebox.showinfo("No", "移動取消", parent=root)
    
    ## Main window
    root = tk.Toplevel()
    root.title("%s" %title)
    #root.configure(background='#DDDDDD')
    root.geometry('%sx%s' % (sub_wd, sub_hi))
    
    icon = PhotoImage(file= images_path + 'AI_system.png')
    root.tk.call('wm','iconphoto',root._w, icon)

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
    photo = Image.open(images_path + bg)
    photo = photo.resize((sub_wd, sub_hi), Image.ANTIALIAS)
    ph = ImageTk.PhotoImage(photo)
    img_label = tk.Label(cnv, image=ph)  # 图片
    img_label.pack()

    ## Frame in canvas
    frm = Frame(cnv)
    frm.config(bg='#DDDDDD')

    ## This puts the frame in the canvas's scrollable zone
    cnv.create_window(0, 0, window=frm, anchor='nw')
    
    pa = back_ground(sc_wd, sc_hi, bg, 0.80, 0.60, text_wd, text_hi, "add_picture.png")
    add_picture = ttk.Button(root, text="新增圖片", style='bd.TButton', image=pa, command=lambda:add_window(bg,"faces/suspects","頗有深度的奧客稽查員-人臉之管理",root))
    add_picture.place(relx=0.80, rely=0.60)
    
    pm = back_ground(sc_wd, sc_hi, bg, 0.80, 0.70, text_wd, text_hi, "move_back.png")
    move_back = ttk.Button(root, text="移回圖片", style='bd.TButton', image=pm,command=os_move)
    move_back.place(relx=0.80, rely=0.70)

    pd = back_ground(sc_wd, sc_hi, bg, 0.80, 0.80, text_wd, text_hi, "delete_picture.png")
    delete_picture = ttk.Button(root, text="刪除圖片", style='bd.TButton', image=pd, command=os_remove)
    delete_picture.place(relx=0.80, rely=0.80)

    pe = back_ground(sc_wd, sc_hi, bg, 0.80, 0.90, text_wd, text_hi, "exit_window.png")
    exit_window = ttk.Button(root, text="關閉視窗", style='bd.TButton', image=pe, command=close)
    exit_window.place(relx=0.80, rely=0.90)

    face_managing(path, remove, root, frm, cnv)

def face_managing(path, arry, root, frm, cnv):

    def clickname(event):
        if (event.widget['background'] == "black"):
            event.widget.configure(background="blue")
            arry.append(event.widget['text'])
        else:
            event.widget.configure(background="black")
            arry.remove(event.widget['text'])

    #清除框架的子物件
    for widget in frm.winfo_children():
        widget.destroy()

    # 读取path文件夹下所有文件的名字
    imagelist = os.listdir(path)
    images = []  # 先存储所有的图像的名称

    for imgname in imagelist:
        if (imgname.endswith(".jpeg") or imgname.endswith(".jpg") or imgname.endswith(".png") or imgname.endswith(".bmp")):
            images.append(imgname)
    images.sort(reverse=True)  # 對讀取的路徑進行反排序

    picture = []  # 存储所有的图像
    ## Frame contents
    j = 0
    k = 0
    for i in range(1,len(images)+1):
        img = Image.open(path + "/" + str(images[i - 1]))
        img = img.resize((face_wd, face_hi), Image.ANTIALIAS)
        p = ImageTk.PhotoImage(img)
        picture.append(p)
        k += 1

        b = tk.Button(frm, text=images[i - 1], image=p, width=face_wd, height=face_hi, highlightthickness=5, background="black")
        b.bind("<Button-1>", clickname)
        b.grid(row=j, column=k, padx=5, pady=5)
        if (i % 4 == 0):
            k = 0
            j += 1

    ## Update display to get correct dimensions
    frm.update_idletasks()
    ## Configure size of canvas's scrollable zone
    cnv.configure(scrollregion=(0, 0, frm.winfo_width(), frm.winfo_height()))
    ## Go!
    root.resizable(width=False, height=False)
    root.mainloop()
    

