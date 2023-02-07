#face_model.py
#1. 匯入模組與類別
import tkinter as tk
import os
import threading
from tkinter import ttk
#from tkinter import *
from tkinter import PhotoImage,Text,filedialog,END,DISABLED,messagebox
from PIL import Image, ImageTk

from face_function import images_path, sub_wd, sub_hi, img_hi, img_wd, text_wd, text_hi
from face_function import back_ground
from face_object import CreateToolTip
from face_training import model_training
from utils.datasets import get_labels
from utils.preprocessor import preprocess_input
from keras.models import load_model
from tkinter.filedialog import askopenfilename
# 引入字体模块
import tensorflow as tf
import tkinter.font as tkFont
from keras.models import load_model
import cv2
import numpy as np
# 引入字体模块

from statistics import mode

#2. 定義元件之事件處理函數

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

def run_face_training(root,textbox):
    #os.popen('python face_training.py')
    # 建立一個子執行緒
    if  messagebox.askquestion("頗有深度的奧客稽查員", "要訓練新的模型嗎?"):
        textbox.delete('0.0', END)
        t = threading.Thread(target = model_training,args=(root,textbox))
    
        # 執行該子執行緒
        t.start()
    else:
        messagebox.showinfo("頗有深度的奧客稽查員", "已取消訓練")
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
        try:
            ochepoint = int((temp[0, 0] * 100)/10)*10 + emotionpoint
            print(temp)
        except:
            print(temp)
            ochepoint="未偵測"
        if ochepoint >= 100 :
            ochepoint=100
        if ochepoint <= 0 :
            ochepoint=0
        oke = tk.Label(window, text=emotion_mode, font=('Arial', 30))
        oke.place(relx=0.1,rely=0.05)
        adv = tk.Label(window, text=str(ochepoint)+"%", font=('Arial', 30))
        adv.place(relx=0.7,rely=0.9)
        
        
        img_test_face = tk.Label(window,text='assdadsads', font=('Arial', 30))
        img_test_face.configure(image = pp)
        img_test_face.place(relx=0.2,rely=0.2)
        window.mainloop()
    if image_path:
        test_win()

def model_window(title):
    def SelectOke():
        global image_path,state
        #global imagePath
        image_path = askopenfilename(initialdir='./faces/rec/all/')
       # print(image_path)
        if image_path :
            return image_path
    def close():
        root.destroy()

    def model_delete(root):
        rt = tk.Tk()
        rt.withdraw()

        file_path = filedialog.askopenfilename(parent=root)
        if (file_path):
            print(file_path)

    ## Main window
    root = tk.Toplevel()
    root.title("%s" % title)
    
    icon = PhotoImage(file= images_path + 'AI_system.png')
    root.tk.call('wm','iconphoto',root._w, icon)
    # root.configure(background='#DDDDDD')
    root.geometry('%sx%s' % (sub_wd, sub_hi))

    # color table
    bg = "bg3.png"
    photo = Image.open(images_path + bg)
    photo = photo.resize((sub_wd, sub_hi), Image.ANTIALIAS)
    ph = ImageTk.PhotoImage(photo)

    img_label = tk.Label(root, image=ph)  # 图片
    img_label.pack()

    # 指定字体名称、大小、样式
    ft = tkFont.Font(size=18, weight=tkFont.BOLD)
    textbox = Text(root, font=ft, width=46, height=22, background='white')

    #顯示模型建立資訊

    #textbox.insert(END,"模型訓練已完成: 10 %\n模型訓練已完成: 20 %\n模型訓練已完成: 30 %\n模型訓練已完成: 40 %\n模型訓練已完成: 50 %\n模型訓練已完成: 60 % \n模型訓練已完成: 70 %\n模型訓練已完成: 80 %\n模型訓練已完成: 90 %\n模型訓練已完成: 100 %\n預測模型已訓練完成。\n")
    #for i in range(10):
        #textbox.insert(END, str(i) + "\n")

    # 禁止輸入
    

    textbox.place(relx=0.38,rely=0.10)

    pi = back_ground(sub_wd, sub_hi, bg, 0.4, 0.03, 540, 36, "information.png")
    information = ttk.Button(root, text='模型資訊', style='bd.TButton', image=pi)
    information.place(relx=0.4, rely=0.03)

    pa = back_ground(sub_wd, sub_hi, bg, 0.10, 0.10, img_wd, img_hi, "add_model.png")
    add_model = ttk.Button(root, style='bd.TButton', image=pa,command=lambda:run_face_training(root,textbox))
    CreateToolTip(add_model, text='模型建立')
    add_model.place(relx=0.10, rely=0.10)

    pd = back_ground(sub_wd, sub_hi, bg, 0.10, 0.45, img_wd, img_hi, "test_model.png")
    delete_model = ttk.Button(root, style='bd.TButton', image=pd, command=lambda:TestModel(root,SelectOke()))
    CreateToolTip(delete_model, text='模型測試')
    delete_model.place(relx=0.10, rely=0.45)

    pe = back_ground(sub_wd, sub_hi, bg, 0.10, 0.80, text_wd, text_hi, "exit_window.png")
    exit_window = ttk.Button(root, text="關閉視窗", style='bd.TButton', image=pe, command=close)
    exit_window.place(relx=0.10,rely=0.80)

    ## Go!
    root.resizable(width=False, height=False)
    root.mainloop()