#face_processing.py
#1. 匯入模組與類別
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage,Canvas,Scrollbar,Frame,Text
from tkinter import END,DISABLED
#from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from PIL import Image, ImageTk

import face_recognition
from face_function import images_path, sub_wd, sub_hi, text_wd, text_hi, bg, face_wd , face_hi , data_wd, data_hi
from face_function import back_ground, face_managing
from face_object import CreateToolTip

import os
import shutil
import datetime

# 引入字体模块
import tkinter.font as tkFont

#2. 定義元件之事件處理函數
def select_window(title):
    path = askdirectory()  # 選擇路徑
    arry = []

    def os_listdir():
        imagelist = os.listdir(path)
        images = []  # 先存储所有的图像的名称

        for imgname in imagelist:
            if (imgname.endswith(".jpeg") or imgname.endswith(".jpg") or imgname.endswith(".png") or imgname.endswith(".bmp")):
                images.append(imgname)
        images.sort()  # 對讀取的路徑進行排序

        return images

    def close():
        arry.clear()
        root.destroy()

    if (path):
        ## Main window
        root = tk.Toplevel()
        root.title("%s" % title)
        
        icon = PhotoImage(file= images_path + 'AI_system.png')
        root.tk.call('wm','iconphoto',root._w, icon)
        ## Grid sizing behavior in window
        # root.configure(background='#DDDDDD')
        root.geometry('%sx%s' % (sub_wd, sub_hi))
        
      
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

        #pai = back_ground(sub_wd, sub_hi, bg, 0.67, 0.07, 360, 360, "face_management.png")
        #face_ai = ttk.Button(root, style='bd.TButton', image=pai, command=lambda: select_window("將處理之圖片"))
        #CreateToolTip(face_ai, text='人臉AI')
        #face_ai.place(relx=0.67, rely=0.07)

        pt = back_ground(sub_wd, sub_hi, bg, 0.75, 0.70, text_wd, text_hi, "total_picture.png")
        total_picture = ttk.Button(root, text="全圖處理", style='bd.TButton', image=pt, command=lambda:deal_window(path,os_listdir(),root,frm,cnv))
        total_picture.place(relx=0.75, rely=0.70)

        pd = back_ground(sub_wd, sub_hi, bg, 0.75, 0.80, text_wd, text_hi, "deal_picture.png")
        deal_picture = ttk.Button(root, text="處理圖片", style='bd.TButton', image=pd, command=lambda:deal_window(path,arry,root,frm,cnv))
        deal_picture.place(relx=0.75, rely=0.80)

        pe = back_ground(sub_wd, sub_hi, bg, 0.75, 0.90, text_wd, text_hi, "exit_window.png")
        exit_window = ttk.Button(root, text="關閉視窗", style='bd.TButton', image=pe, command=close)
        exit_window.place(relx=0.75,rely=0.90)
        
        #face_function
        face_managing(path, arry, root, frm, cnv)

def deal_window(path, images, root, frm, cnv):
    
    if messagebox.askyesno("Deal", "確定處理麼?", parent=root):
        # messagebox.showinfo("Yes", "處理成功", parent=root)
        images.sort()  # 排序
        faces = []
        unfaces = []
        
        if(images):
            ##messagebox.showinfo("Deal", "處理中(請稍後", parent=root)
            # 指定字体名称、大小、样式
            ft = tkFont.Font(size=18, weight=tkFont.BOLD)
            textbox = Text(root, font=ft, width=25, height=15, background='white')
            textbox.place(relx=0.70, rely=0.03) 
            ## Frame in textbox
            frmbox = Frame(textbox)
            ## Update display to get correct dimensions
            frmbox.update_idletasks()
            for file in images:
                print(file)
                image = face_recognition.load_image_file("%s/" % path + "%s" % file)
                face_locations = face_recognition.face_locations(image)
                 
                # 顯示圖片資訊
                textbox.insert(END," {} face(s) in {}\n".format(len(face_locations), file))
                print(" I found {} face(s) in this photograph.".format(len(face_locations)))
                frmbox.update_idletasks()
                 
                if (len(face_locations) == 0):
                    unfaces.append(file)

                for face_location in face_locations:
                    #t = datetime.datetime.now()
                    # Print the location of each face in this image
                    top, right, bottom, left = face_location
                    # print(
                    #    "A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom,
                    #                                                                                         right))
                    # You can access the actual face itself like this:
                    face_image = image[top:bottom, left:right]
                    pil_image = Image.fromarray(face_image)
                    ##pil_image.save("faces/suspects/" + str(t) + ".bmp")
                    faces.append(pil_image)
                    # pil_image.show()
            # 禁止輸入
            textbox.config(state=DISABLED)
            select_picture(faces, root, frm, cnv, path, unfaces)
        else:
            messagebox.showinfo("Deal", "未選擇處理之圖片", parent=root)
    else:
        messagebox.showinfo("No", "處理取消", parent=root)

def select_picture(faces, root, frm, cnv, path, unfaces):
    save_faces = []

    def clickname(event):
        if (event.widget['background'] == "black"):
            event.widget.configure(background="blue")
            save_faces.append(faces[event.widget['text']])
        else:
            event.widget.configure(background="black")
            save_faces.remove(faces[event.widget['text']])

    def save_face(order):
        if messagebox.askyesno("Save", "確定儲存麼?", parent=root):
            # messagebox.showinfo("Yes", "儲存成功", parent=root)
            if(order): #1 total
                for face in faces:
                    t = datetime.datetime.now().strftime('%Y_%m_%d_%H-%M-%S-%f')
                    face = face.resize((data_wd, data_hi), Image.ANTIALIAS)
                    face.save("faces/suspects/" + t + ".bmp")
                faces.clear() #faces.remove
                save_faces.clear()
                messagebox.showinfo("Save", "儲存成功", parent=root)
                select_picture(faces, root, frm, cnv, path, unfaces)
                #root.destroy()
            else: #0
                if(save_faces):
                    for face in save_faces:
                        t = datetime.datetime.now().strftime('%Y_%m_%d_%H-%M-%S-%f')
                        faces.remove(face)
                        face = face.resize((data_wd, data_hi), Image.ANTIALIAS)
                        face.save("faces/suspects/" + t + ".bmp")
                        
                    save_faces.clear()
                    messagebox.showinfo("Save", "儲存成功", parent=root)
                    select_picture(faces, root, frm, cnv,  path, unfaces)
                else:
                    messagebox.showinfo("Save", "未選擇儲存之圖片", parent=root)
        else:
            messagebox.showinfo("No", "儲存取消", parent=root)

    def unfaces_picture(faces, root, frm, cnv, path, unfaces):
        move = []
        def clickname(event):
            if (event.widget['background'] == "black"):
                event.widget.configure(background="blue")
                move.append(event.widget['text'])
            else:
                event.widget.configure(background="black")
                move.remove(event.widget['text'])

        def move_face():
            if messagebox.askyesno("Move", "確定匯集麼?", parent=root):
                # messagebox.showinfo("Yes", "匯集成功", parent=root)
                if (unfaces):
                    #same exists
                    same_flag = 0

                    for face in unfaces:
                        folder = os.path.exists("faces/unfaces/%s" % face)

                        if folder:  # 判断是否存在文件夹 如果存在则刪除後 匯集
                            same_flag = 1 #存在同檔名
                            break

                    if(same_flag): #如果存在同檔名
                        if messagebox.askyesno("Move", "含有同名檔案將覆蓋，確定匯集麼?", parent=root):
                            for face in unfaces:
                                    os.remove("faces/unfaces/%s" % face)
                                    shutil.move(path + "/%s" % face, "faces/unfaces")
                            messagebox.showinfo("Move", "匯集成功", parent=root)
                        else:
                            messagebox.showinfo("No", "匯集取消", parent=root)
                    else:#如果不存在同檔名
                        for face in unfaces:
                                shutil.move(path + "/%s" % face, "faces/unfaces")
                        messagebox.showinfo("Move", "匯集成功", parent=root)

                    move.clear()
                    unfaces.clear()
                    unfaces_picture(faces, root, frm, cnv, path, unfaces)
            else:
                messagebox.showinfo("No", "匯集取消", parent=root)

        def remove_face():
            if messagebox.askyesno("Delete", "確定刪除麼?", parent=root):
                # messagebox.showinfo("Yes", "刪除成功", parent=root)
                if (move):
                    for face in move:
                        os.remove(path + "/%s" % face)
                        unfaces.remove(face)
                    move.clear()
                    unfaces_picture(faces, root, frm, cnv, path, unfaces)
                else:
                    messagebox.showinfo("Delete", "未選擇刪除之圖片", parent=root)
            else:
                messagebox.showinfo("No", "刪除取消", parent=root)

        # 清除框架的子物件
        for widget in frm.winfo_children():
            widget.destroy()

        unfaces.sort()  # 對讀取的檔案進行排序

        picture = []  # 存储所有的图像
        ## Frame contents
        j = 0
        k = 0
        for i in range(1, len( unfaces) + 1):
            img = Image.open(path + "/" + str(unfaces[i - 1]))
            img = img.resize((face_wd, face_hi), Image.ANTIALIAS)
            p = ImageTk.PhotoImage(img)
            picture.append(p)
            k += 1

            b = tk.Button(frm, text=unfaces[i - 1], image=p, width=face_wd, height=face_hi, highlightthickness=5, background="black")
            b.bind("<Button-1>", clickname)
            b.grid(row=j, column=k, padx=5, pady=5)
            if (i % 4 == 0):
                k = 0
                j += 1

        pp = back_ground(sub_wd, sub_hi, bg, 0.75, 0.60, text_wd, text_hi, "processed.png")
        processed = ttk.Button(root, text="完成處理", style='bd.TButton', image=pp, command=lambda:select_picture(faces,root,frm,cnv,path,unfaces))
        processed.place(relx=0.75,rely=0.60)

        pc = back_ground(sub_wd, sub_hi, bg, 0.75, 0.70, text_wd, text_hi, "collection.png")
        collection = ttk.Button(root, text="全部匯集", style='bd.TButton', image=pc, command=move_face)
        collection.place(relx=0.75, rely=0.70)

        pd = back_ground(sub_wd, sub_hi, bg, 0.75, 0.80, text_wd, text_hi, "delete_picture.png")
        delete_picture = ttk.Button(root, text="刪除圖片", style='bd.TButton', image=pd, command=remove_face)
        delete_picture.place(relx=0.75,rely=0.80)

        ## Update display to get correct dimensions
        frm.update_idletasks()
        ## Configure size of canvas's scrollable zone
        cnv.configure(scrollregion=(0, 0, frm.winfo_width(), frm.winfo_height()))
        ## Go!
        #.resizable(width=False, height=False)
        root.mainloop()

        # 清除框架的子物件
    for widget in frm.winfo_children():
        widget.destroy()

    picture = []  # 存储所有的图像
    ## Frame contents
    j = 0
    k = 0
    for i in range(1, len(faces) + 1):
        # print(images[i - 1])
        img = faces[i - 1]
        img = img.resize((face_wd, face_hi), Image.ANTIALIAS)
        p = ImageTk.PhotoImage(img)
        picture.append(p)

        k += 1
        b = tk.Button(frm, text=i - 1, image=p, width=face_wd, height=face_hi, highlightthickness=5, background="black")
        b.bind("<Button-1>", clickname)
        b.grid(row=j, column=k, padx=5, pady=5)

        if (i % 4 == 0):
            k = 0
            j += 1

    if(unfaces):
        pu = back_ground(sub_wd, sub_hi, bg, 0.75, 0.60, text_wd, text_hi, "unprocessed.png")
        unprocessed = ttk.Button(root, text="未能處理", style='bd.TButton', image=pu, command=lambda:unfaces_picture(faces,root,frm,cnv,path,unfaces))
        unprocessed.place(relx=0.75, rely=0.60)

    pst = back_ground(sub_wd, sub_hi, bg, 0.75, 0.70, text_wd, text_hi, "save_total.png")
    save_total = ttk.Button(root, text="全部儲存", style='bd.TButton', image=pst, command=lambda:save_face(1))
    save_total.place(relx=0.75, rely=0.70)

    psp = back_ground(sub_wd, sub_hi, bg, 0.75, 0.80, text_wd, text_hi, "save_picture.png")
    save_picture = ttk.Button(root, text="儲存圖片", style='bd.TButton', image=psp, command=lambda:save_face(0))
    save_picture.place(relx=0.75, rely=0.80)

    #re = ttk.Button(root, text="返回上頁", style='my.TButton', command=delete_button).place(relx=0.80, rely=0.90)

    ## Update display to get correct dimensions
    frm.update_idletasks()
    ## Configure size of canvas's scrollable zone
    cnv.configure(scrollregion=(0, 0, frm.winfo_width(), frm.winfo_height()))
    ## Go!
    #root.resizable(width=False, height=False)
    root.mainloop()
