# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 22:32:07 2019

@author: chun8
"""
import os
import shutil
import tkinter as tk
from tkinter import messagebox
#from face_recognize import face_OkeManage_window

from PIL import Image, ImageTk
from rec_train import TrainAndInput

import pandas as pd

#from tkinter import *

from tkinter.filedialog import askopenfilename
from csvfuntion import load_and_tmp,printdata,delete_new,change_new
from face_object import CreateToolTip



 
def DeleteOke(root,image_path,img_label_face,adv_text_rec,oke_text_rec):
    result = messagebox.askquestion("頗有深度的奧客稽查員", "確定要刪除此奧客?")
    if result == 'yes':
        if image_path:
            image_name = os.path.split(image_path) [1]
            image_name_id = float(image_name.lstrip('0').rstrip('.bmp'))
            load_and_tmp('costo')
            #printdata('costo')
            delete_new('costo',image_name_id)
            shutil.rmtree('./faces/rec/face_oke/'+str(image_name.rstrip('.bmp')))
            os.remove('./faces/rec/all/'+image_name)
            #printdata('costo')
            messagebox.showinfo("頗有深度的奧客稽查員","已成功刪除")
            adv_text_rec.place_forget()
            oke_text_rec.place_forget()
            img_label_face.place_forget()
        else:
            messagebox.showinfo("頗有深度的奧客稽查員","請選擇人臉")
    else:
        messagebox.showinfo("頗有深度的奧客稽查員","已取消刪除")
        print('已取消')
def TrainModel(root,image_path,OkeBehavior,OkeAdvice,img_label_face,adv_text_rec,oke_text_rec):
    result = messagebox.askquestion("頗有深度的奧客稽查員", "確定要訓練模型?")
    print(image_path)
    if result == 'yes':
        if image_path:
            rec = './faces/rec/face_oke/'
            oke_data = pd.read_csv('costo.csv',encoding='utf-8')
            folder = os.listdir(rec)
            person_num_list = []
            try:
                new_face = int(os.path.split(image_path)[1].lstrip('0').rstrip('.bmp'))
            except:
                new_face = 'new'
                print('新人臉')
            for person in oke_data['顧客ID']:
                person_num_list.append(person)
            #folder_all = os.listdir('./faces/rec/all/')
            if person_num_list == []:
                os.makedirs(rec+'001')
                shutil.move(image_path,rec+'001')
                image_name = os.listdir(rec+'001')
                os.rename(rec+'001/'+image_name[0],rec+'001/001.bmp')
                shutil.copy(rec+'001/001.bmp','./faces/rec/all/')
            elif new_face in person_num_list:
                load_and_tmp('costo')
                print(image_path)
                change_new('costo',new_face,oke_data[oke_data['顧客ID']==new_face].values[0][3],OkeBehavior,OkeAdvice)
            else:
                count = len(person_num_list)
                os.makedirs(rec+str(count+1).zfill(3))
                shutil.move(image_path,rec+str(count+1).zfill(3))
                image_name = os.listdir(rec+str(count+1).zfill(3))
                os.rename(rec+str(count+1).zfill(3)+'/'+image_name[0],rec+str(count+1).zfill(3)+'/'+str(count+1).zfill(3)+'.bmp')
                shutil.copy(rec+str(count+1).zfill(3)+'/'+str(count+1).zfill(3)+'.bmp','./faces/rec/all/')
            folder = os.listdir('./faces/rec/face_oke/')
            flag = TrainAndInput(root,folder,OkeBehavior,OkeAdvice)
            adv_text_rec.place_forget()
            oke_text_rec.place_forget()
            if flag != 1:
                messagebox.showinfo("頗有深度的奧客稽查員","訓練成功")
        else:
            messagebox.showinfo("頗有深度的奧客稽查員","請先選擇人臉和奧客紀錄以及過去紀錄")
        img_label_face.place_forget()
    else:
        messagebox.showinfo("頗有深度的奧客稽查員","已取消訓練")
def TestModel(root,image_path,adv_text_rec,oke_text_rec):
    def test_win():
         window = tk.Toplevel()
         window.title('頗有深度的奧客稽查員')
         ##窗口尺寸
         window.geometry('500x500')
         oke = tk.Label(window, text=csv_oke.values[0][1], font=('Arial', 30))
         oke.place(relx=0.7,rely=0.05)
         adv = tk.Label(window, text=csv_oke.values[0][2], font=('Arial', 30))
         adv.place(relx=0.1,rely=0.9)
         photo_face = Image.open(image_path)
         photo_face = photo_face.resize((300, 300), Image.ANTIALIAS)
         pp = ImageTk.PhotoImage(photo_face)
         
         img_test_face = tk.Label(window,text='assdadsads', font=('Arial', 30))
         img_test_face.configure(image = pp)
         img_test_face.place(relx=0.2,rely=0.2)
         window.mainloop()
    #face_image = './faces/rec/001/001.bmp' 
    if image_path:
        messagebox.showinfo("頗有深度的奧客稽查員",'測試以觀看效果')
        face_image_name = os.path.split(image_path) 
        csv_file = pd.read_csv('costo.csv',encoding='utf-8')
        csv_oke = csv_file[csv_file['顧客ID'] == float(face_image_name[1].lstrip('0').rstrip('.bmp'))]
        print(csv_oke.values[0][1])
        test_win()
    else:
       messagebox.showinfo("頗有深度的奧客稽查員",'請選擇一張人臉')

#TestModel()