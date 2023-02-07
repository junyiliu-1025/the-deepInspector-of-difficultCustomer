# -*- coding: utf-8 -*-
##face_recognize.py
#1. 匯入模組與類別
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk

from face_function import images_path, sc_wd, sc_hi, img_hi, img_wd, text_wd, text_hi
from face_function import back_ground, close
from face_object import CreateToolTip

from tkinter.filedialog import askopenfilename
import pandas as pd
from utils.datasets import get_labels
from utils.preprocessor import preprocess_input

import cv2
import numpy as np
# 引入字体模块
import tensorflow as tf
import tkinter.font as tkFont
from keras.models import load_model
import os 
from statistics import mode

# parameters for loading data and images
emotion_model_path = './emotional_model/fer2013_mini_XCEPTION.102-0.66.hdf5'
    
emotion_labels = get_labels('fer2013')
 # loading models
emotion_classifier = load_model(emotion_model_path, compile=False)
    
# getting input model shapes for inference
emotion_target_size = emotion_classifier.input_shape[1:3]
    
# starting lists for calculating modes
emotion_window = []
emotion_mode =""
    
#oche_model_preprocess
dim = (92, 112)
sess = tf.compat.v1.Session()
graph_path = os.path.abspath('./models/model_oka/my-gender-v1.0.meta')
model = os.path.abspath('./models/model_oka/')
    
graph = tf.compat.v1.get_default_graph()
    
server = tf.compat.v1.train.import_meta_graph(graph_path)
server.restore(sess, tf.compat.v1.train.latest_checkpoint(model))

# 填充feed_dict
x = graph.get_tensor_by_name('input_images:0')
y = graph.get_tensor_by_name('input_labels:0')
# 全连接最后一层输出
f_softmax = graph.get_tensor_by_name('f_softmax:0')

emotion_window=[]
def TestModel(root,image_path):
    def test_win():
        window = tk.Toplevel()
        window.title('頗有深度的奧客稽查員')
        ##窗口尺寸
        window.geometry('500x500')
           
        
        
        photo_face_t = cv2.imread(image_path)
        photo_face_t = cv2.cvtColor(photo_face_t, cv2.COLOR_BGR2GRAY)
        gray_face = cv2.resize(photo_face_t, (emotion_target_size))

        gray_face = preprocess_input(gray_face, True)
        gray_face = np.expand_dims(gray_face, 0)
        gray_face = np.expand_dims(gray_face, -1)
        
        emotion_prediction = emotion_classifier.predict(gray_face)
        emotion_probability = np.max(emotion_prediction)

        emotion_label_arg = np.argmax(emotion_prediction)
        emotion_text = emotion_labels[emotion_label_arg]
        emotion_window.append(emotion_text)
        try:
            emotion_mode = mode(emotion_window)
        except:
            emotion_mode =""
        if emotion_text == 'Angry':
            color = emotion_probability * np.asarray((255, 0, 0))
            emotionpoint = 20
            emotion_mode="憤怒"
        elif emotion_text == 'Sad':
            color = emotion_probability * np.asarray((0, 0, 255))
            emotionpoint = 10
            emotion_mode="沮喪"
        elif emotion_text == 'Happy':
            color = emotion_probability * np.asarray((255, 255, 0))
            emotionpoint = -10
            emotion_mode="高興"
        else:
            color = emotion_probability * np.asarray((0, 255, 0))
            emotionpoint = 0
            if emotion_text == 'Neutral':
                emotion_mode="自然"
            elif emotion_text == 'Fear':
                emotion_mode="恐懼"
            elif emotion_text == 'Disgust':
                emotion_mode="噁心"
            elif emotion_text == "Surprise":
                emotion_mode="驚喜"
            else:
                emotion_text= ""
        color = color.astype(int)
        color = color.tolist()
        color=(color[0],color[1],color[2])

        
        photo_face = Image.open(image_path)
        photo_face = photo_face.resize((300, 300), Image.ANTIALIAS)
        
        pp = ImageTk.PhotoImage(photo_face)
        
        photo_for_test_gray = cv2.resize(photo_face_t,(92,112), fx=0, fy=0, interpolation=cv2.INTER_AREA)
        input_images = photo_for_test_gray.reshape(1, 10304)
        labels = np.zeros((1, 2), dtype=np.int)
        feed_dict = {x: input_images, y: labels}
        temp = sess.run(f_softmax, feed_dict)

        ochepoint = int((temp[0, 0] * 100)/10)*10 + emotionpoint
        
        oke = tk.Label(window, text=emotion_mode, font=('Arial', 30))
        oke.place(relx=0.1,rely=0.05)
        adv = tk.Label(window, text=str(ochepoint)+"%", font=('Arial', 30))
        adv.place(relx=0.7,rely=0.9)
        
        
        img_test_face = tk.Label(window,text='assdadsads', font=('Arial', 30))
        img_test_face.configure(image = pp)
        img_test_face.place(relx=0.2,rely=0.2)
        window.mainloop()

    test_win()

       
def face_OkeManage_window():
    global image_path,state
    image_path = None
    state = 'disabled'
    
    def SelectOke():
        global image_path,state
        #global imagePath
        image_path = askopenfilename(initialdir='./faces/rec/all/')
        print(image_path)        
        return image_path
    

    root = tk.Tk()
    root.title("頗有深度的奧客稽查員-奧客管理")
    
    icon = PhotoImage(file= images_path + 'AI_system.png')
    root.tk.call('wm','iconphoto',root._w, icon)
    
    bg = "bg0.png" #背景
    recognize_wd = int(sc_wd // 5 * 4)
    recognize_hi = int(sc_hi // 10 * 7)
    
    #color table
    photo = Image.open(images_path + bg)
    print(images_path)
    print(bg)
    print(photo)
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

    p_sk = back_ground(recognize_wd, recognize_hi, bg, 0.11, 0.67, text_wd, text_hi, "select_oke.png")
    select_oke = ttk.Button(root,style='bd.TButton', image=p_sk, command=SelectOke)
    select_oke.place(relx=0.11,rely=0.67)
    
    p_dk = back_ground(recognize_wd, recognize_hi, bg, 0.11, 0.81, text_wd, text_hi, "delete_oke.png")
    delete_oke = ttk.Button(root,state=state,style='bd.TButton', image=p_dk)
    delete_oke.place(relx=0.11,rely=0.81)

    
    p_test = back_ground(recognize_wd, recognize_hi, bg, 0.77, 0.4, img_wd//7*6, img_hi//7*6, "test_model.png")
    test_model = ttk.Button(root, style='bd.TButton', image=p_test,command=lambda:TestModel(root,SelectOke()))
    CreateToolTip(test_model, text='模型測試')
    test_model.place(relx=0.77,rely=0.4)
    
    
    pc = back_ground(recognize_wd, recognize_hi, bg, 0.77, 0.7, img_wd//7*6, img_hi//7*6, "exit.png")
    system_close = ttk.Button(root, style='bd.TButton', image=pc, command=lambda:close(root))
    CreateToolTip(system_close, text='離開視窗')
    system_close.place(relx=0.77,rely=0.7)
    

    
    #5. 啟始事件迴圈顯示視窗
    root.resizable(width=False, height=False)
    root.mainloop()
face_OkeManage_window()