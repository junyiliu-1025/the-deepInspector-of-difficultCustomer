# -*- coding: utf-8 -*-
##face_recognize.py
#1. 匯入模組與類別
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage,messagebox
from PIL import Image, ImageTk
from face_recognize_function import DeleteOke,TrainModel,TestModel
from face_function_client import images_path, sc_wd, sc_hi, img_hi, img_wd, text_wd, text_hi
from face_function_client import back_ground, close
from face_object import CreateToolTip
from tkinter.filedialog import askdirectory,askopenfilename
import pandas as pd
# 引入字体模块
import tkinter.font as tkFont

import os 

#2. 定義元件之事件處理函數
#file_client_run()

#3. 建立最上層視窗, 設定標題與大小
'''
def SelectOke(root):
    global imagePath
    imagePath = askopenfilename()
    print(imagePath)
    #color table
    photo = Image.open(imagePath)
    photo = photo.resize((img_wd, img_hi), Image.ANTIALIAS)
    pp = ImageTk.PhotoImage(photo)
    print(pp)
    
    img_label_face = tk.Label(root,image=pp)  #图片
    img_label_face.place(relx=0.11,rely=0.23)
 '''
def face_recognition_window():
    global image_path,state
    image_path = None
    state = 'disabled'
    default_face = ('customer_identify.png')
    default_id = ''
    def SelectOke():
        global image_path,state
        #global imagePath
        image_path = askopenfilename(initialdir='./faces/rec/all/')
        print(image_path)
        Oke_data = pd.read_csv('costo.csv',encoding='utf-8')
        person_num_list = []
        for person in Oke_data['顧客ID']:
            person_num_list.append(person)
        #print(image_path)
        image_path_id = os.path.split(image_path)[1].rstrip('.bmp')
        print('image_path_id',image_path_id)
        #forlder = os.listdir('./faces/rec/all/')
        try:
            if int(image_path_id.lstrip('0')) in person_num_list:
                delete_oke['state'] = tk.NORMAL
                face_id_address.set(" 顧客ID："+ image_path_id)
            #Oke_data = pd.read_csv('costo.csv',encoding='utf-8')
            #Oke_data = Oke_data .dropna()
            #print(Oke_data)
            #oke_br_combo.set=(Oke_data[Oke_data['顧客ID']==float(image_path_id)]['奧客行為紀錄'][0])
            #select_r_combo.set(Oke_data[Oke_data['顧客ID']==float(image_path_id)]['建議方式紀錄'][0])
            photo_face = Image.open(image_path)
            photo_face = photo_face.resize((img_wd, img_hi), Image.ANTIALIAS)
            pp = ImageTk.PhotoImage(photo_face)
            img_label_face.configure(image= pp)
            img_label_face.image = pp # keep a reference!
            img_label_face.place(relx=0.11,rely=0.23)
            oke_text_rec.place(relx=0.4,rely=0.4)
            oke_text.set(' 當前行為:'+Oke_data[Oke_data['顧客ID'] == int(image_path_id.lstrip('0'))].values[0][1])
            adv_text_rec.place(relx=0.4,rely=0.8)
            adv_text.set(' 當前應對:'+Oke_data[Oke_data['顧客ID'] == int(image_path_id.lstrip('0'))].values[0][2])
            root.update_idletasks()
        except:
            if image_path:
                if len(person_num_list) >= 1:
                    person_id_num_max = len(person_num_list)
                    print('person_num_list:',person_num_list)
                    face_id_address.set(" 新顧客ID："+ str(person_id_num_max+1).zfill(3))
                    delete_oke['state'] = tk.DISABLED
                else:
                    face_id_address.set(" 新顧客ID：001")
                    delete_oke['state'] = tk.DISABLED
                photo_face = Image.open(image_path)
                photo_face = photo_face.resize((img_wd, img_hi), Image.ANTIALIAS)
                pp = ImageTk.PhotoImage(photo_face)
                img_label_face.configure(image= pp)
                img_label_face.image = pp # keep a reference!
                img_label_face.place(relx=0.11,rely=0.23)
                adv_text_rec.place_forget()
                oke_text_rec.place_forget()
                root.update_idletasks()
            else:
                face_id_address.set(" 顧客ID：")
                delete_oke['state'] = tk.DISABLED
                img_label_face.place_forget()
                adv_text_rec.place_forget()
                oke_text_rec.place_forget()
    
    #    aa = 'C:/code/Graduate_Project/face_client/faces/test_file/2019_10_19_17-15-53-935650.bmp'
    OkeBehavior = pd.read_csv('oke.csv',encoding='utf-8')
    OkeAdvice = pd.read_csv('adv.csv',encoding='utf-8')
    OkeBehavior = OkeBehavior.dropna()
    OkeAdvice = OkeAdvice.dropna()
    behavior = []
    advice = []
    for i in OkeBehavior['奧客行為']:
        behavior.append(i)
    for i in OkeAdvice['建議方式']:
        advice.append(i)   
    root = tk.Toplevel()
    root.title("頗有深度的奧客稽查員-奧客管理")
    #root.attributes("-topmost", True)
    icon = PhotoImage(file= images_path + 'AI_system.png')
    root.tk.call('wm','iconphoto',root._w, icon)
    
    bg = "bg0.png" #背景
    recognize_wd = int(sc_wd // 5 * 4)
    recognize_hi = int(sc_hi // 10 * 7)
    
    #color table
    photo = Image.open(images_path + bg)
    #print(images_path)
    #print(bg)
    #print(photo)
    photo = photo.resize((recognize_wd, recognize_hi), Image.ANTIALIAS)
    ph = ImageTk.PhotoImage(photo)
    
    img_label = tk.Label(root,image=ph)  #图片
    img_label.pack()
    
    #1264,915 my_notebook
    root.geometry('%sx%s'%(recognize_wd, recognize_hi))
    
    bd = ttk.Style()
    bd.configure('bd.TButton', borderwidth=0, relief="raised", background='white')
    
    # 指定字体名称、大小、样式
    ft = tkFont.Font(size=18)
    root.option_add("*Font", ft)  
    
    #4. 加入 tk/ttk 元件並指定事件處理函數
    p_cface = back_ground(recognize_wd, recognize_hi, bg, 0.15, 0.15, text_wd//5*3, text_hi//5*3, "customer_face.png")
    c_face = ttk.Button(root, style='bd.TButton', image=p_cface)
    c_face.place(relx=0.15,rely=0.15)
    
    p_obr = back_ground(recognize_wd, recognize_hi, bg, 0.4, 0.13, text_wd//2*3, text_hi//5*4, "oke_behavior_record.png")
    oke_br = ttk.Button(root, style='bd.TButton', image=p_obr)
    oke_br.place(relx=0.4,rely=0.13)
    
    oke_br_combo = ttk.Combobox(root,value=behavior,state='readonly',width=25,height=5)   
    oke_br_combo.place(relx=0.4,rely=0.25)
    
    p_rs = back_ground(recognize_wd, recognize_hi, bg, 0.4, 0.55, text_wd//2*3, text_hi//5*4, "response_select.png")
    select_r = ttk.Button(root, style='bd.TButton', image=p_rs)
    select_r.place(relx=0.4,rely=0.55)
    
    select_r_combo = ttk.Combobox(root,value=advice,state='readonly',width=25,height=5)   
    select_r_combo.place(relx=0.4,rely=0.67)
    
    #face_id_address = tk.StringVar(value=data['IP'])
    face_id_address = tk.StringVar(value=" 顧客ID：" + default_id)
    face_id = ttk.Entry(root,font=('Verdana',20),width=12,textvariable= face_id_address,state='disabled')
    face_id.place(relx=0.11,rely=0.58)
    
    oke_text = tk.StringVar(value=" 當前行為：" + default_id)
    oke_text_rec = ttk.Entry(root,font=('Verdana',20),width=16,textvariable= oke_text,state='disabled')
    oke_text_rec.place(relx=0.4,rely=0.4)
    oke_text_rec.place_forget()
    
    adv_text = tk.StringVar(value=" 當前方式：" + default_id)
    adv_text_rec = ttk.Entry(root,font=('Verdana',20),width=16,textvariable= adv_text,state='disabled')
    adv_text_rec.place(relx=0.4,rely=0.8)
    adv_text_rec.place_forget()
    
    p_face = back_ground(recognize_wd, recognize_hi, bg, 0.11, 0.23, img_wd, img_hi ,default_face)
    present_face = ttk.Button(root, style='bd.TButton', image=p_face, command=SelectOke)
    CreateToolTip(present_face, text='選擇人臉')
    present_face.place(relx=0.11,rely=0.23)
    
    p_sk = back_ground(recognize_wd, recognize_hi, bg, 0.11, 0.67, text_wd, text_hi, "select_oke.png")
    select_oke = ttk.Button(root,style='bd.TButton', image=p_sk, command=SelectOke)
    select_oke.place(relx=0.11,rely=0.67)
    
    p_dk = back_ground(recognize_wd, recognize_hi, bg, 0.11, 0.81, text_wd, text_hi, "delete_oke.png")
    delete_oke = ttk.Button(root,state=state,style='bd.TButton', image=p_dk,command=lambda:DeleteOke(root,image_path,img_label_face,adv_text_rec,oke_text_rec))
    delete_oke.place(relx=0.11,rely=0.81)
    
    p_train = back_ground(recognize_wd, recognize_hi, bg, 0.77, 0.1, img_wd//7*6, img_hi//7*6, "model_train.png")
    train_model = ttk.Button(root, style='bd.TButton', image=p_train, command=lambda:TrainModel(root,image_path,oke_br_combo.get(),select_r_combo.get(),img_label_face,adv_text_rec,oke_text_rec))
    CreateToolTip(train_model, text='模型訓練')
    train_model.place(relx=0.77,rely=0.1)
    
    
    p_test = back_ground(recognize_wd, recognize_hi, bg, 0.77, 0.4, img_wd//7*6, img_hi//7*6, "test_model.png")
    test_model = ttk.Button(root, style='bd.TButton', image=p_test,command=lambda:TestModel(root,image_path,adv_text_rec,oke_text_rec))
    CreateToolTip(test_model, text='模型測試')
    test_model.place(relx=0.77,rely=0.4)
    
    
    pc = back_ground(recognize_wd, recognize_hi, bg, 0.77, 0.7, img_wd//7*6, img_hi//7*6, "exit.png")
    system_close = ttk.Button(root, style='bd.TButton', image=pc, command=lambda:close(root))
    CreateToolTip(system_close, text='離開視窗')
    system_close.place(relx=0.77,rely=0.7)
    
    photo_face = Image.open('./images_client/'+default_face)
    photo_face = photo_face.resize((img_wd, img_hi), Image.ANTIALIAS)
    pp = ImageTk.PhotoImage(photo_face)
    img_label_face = tk.Button(root,image=pp,command=lambda:SelectOke())  #图片
    img_label_face.image = pp # keep a reference!
    img_label_face.place(relx=0.11,rely=0.23)
    img_label_face.place_forget()
    
    #5. 啟始事件迴圈顯示視窗
    root.resizable(width=False, height=False)
    root.mainloop()
