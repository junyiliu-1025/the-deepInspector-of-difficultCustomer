#face_prediction.py
#1. 匯入模組與類別
from statistics import mode
import cv2
from keras.models import load_model
import numpy as np
import face_recognition
import tensorflow as tf
import os
import datetime
import time
import threading

from csvfuntion import load_and_tmp
from utils.datasets import get_labels
from utils.preprocessor import preprocess_input
from utils.inference import draw_text
#from face_socketClient import socket_Client
from PIL import Image, ImageDraw, ImageFont
from keras import backend as K
import numpy
import dlib
import pandas as pd

def initialize(): 
    global Prtsc_sysrq,click_prt
    Prtsc_sysrq = 0 
    click_prt=0

initialize()

def face_flagup():
    global Prtsc_sysrq
    Prtsc_sysrq = 1
    print(Prtsc_sysrq)
def face_flagdown():
    global Prtsc_sysrq
    Prtsc_sysrq = 0
    print(Prtsc_sysrq)
def click_prtsc():
    global click_prt
    click_prt = 1
    print(click_prt)
def check_globalvalue():
    global Prtsc_sysrq
    if Prtsc_sysrq==1:
        return True
    else:
        return False
#變數宣告&給初始值
scr_cd=0
if_face=0
catch_used=1
oke_used=1
i=0
find_oka=0
oka_t=""
start_dect=0
start_scr=0
now=0

#人臉的上下左右
top = 0
right = 0
bottom = 0
left = 0
#繪製框所需變數
pta=(0,0)
ptb=(0,0)
color=(255,255,255)
    
# hyper-parameters for bounding boxes shape
frame_window = 5
    


matrix=[]

   
#funtion
def read_file(file):
    project_var = []
    with open(file,'r',encoding='utf-8') as f:
        data = f.readlines()
        for i in data:
            data = i.strip('\n').split(':')
            project_var.append(data)
    return dict(project_var)
data=read_file('face_variable.txt')
print(data)


def pass_time(now,timevalue):
    return now-timevalue

def cv2ImgAddText(img, text, left, top, textColor, textSize=20):
    if (isinstance(img, numpy.ndarray)):  #判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    fontText = ImageFont.truetype( 
            "font/mingliu.ttc", textSize, encoding="utf-8")
    textColor=(textColor[2],textColor[1],textColor[0])
    draw.text( (left, top) , text , textColor , font=fontText)
    return cv2.cvtColor(numpy.asarray(img), cv2.COLOR_RGB2BGR)


def return_euclidean_distance(feature_1, feature_2):
    #print(type(feature_2))
    #print(feature_2)
    feature_1 = np.array(feature_1)
    feature_2 = np.array(feature_2)
    dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
    return dist


if os.path.exists("costo.csv"):
    path_features_known_csv = "costo.csv"
    csv_rd = pd.read_csv(path_features_known_csv,encoding='utf-8')
    print(csv_rd)

    features_known_arr = []

    for i in range(len(csv_rd)):
        try:
            features = csv_rd['特徵'][i].replace('\n','').replace('[','').replace(',','').replace(']','').split()
            features = list(map(eval,features))
            features_known_arr.append(features)
        except:
            print()
   # print(len(features_known_arr[7]))
    print("Faces in Database：", len(features_known_arr))

    # Dlib 检测器和预测器
    # The detector and predictor will be used
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('./recognition_model/shape_predictor_68_face_landmarks.dat')

def prediction_client():
    
    
    winname= "The Deep Inspector Of Difficult Customer"
    # starting video streaming
    cv2.namedWindow(winname,0)
    K.clear_session()
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
    
    facerec = dlib.face_recognition_model_v1("./recognition_model/dlib_face_recognition_resnet_model_v1.dat")

    name_namelist = []
    e_distance_list = []
    features_cap_arr = []

    
    #變數宣告&給初始值
    tmp_for_distance=[]
    target_for_distance=0
    scr_cd=0
    if_face=0
    catch_used=1
    oke_used=1
    i=0
    find_oka=0
    oka_t=""
    start_dect=0
    start_scr=0
    start_oka=0
    start_push=0
    start_oka_save=0
    now=0
    push_p=0
    flag_war=0
    k=0
    flag_test=0
    load_and_tmp('costo')
    okewarning=int(data['oke_warning'])
    aut_capture_min=int(data['aut_capture_min'])
    aut_capture_max=int(data['aut_capture_max'])
    
    
    #人臉的上下左右
    top = 0
    right = 0
    bottom = 0
    left = 0
    #繪製框所需變數
    pta=(0,0)
    ptb=(0,0)
    color=(255,255,255)
    #main process
    capture = cv2.VideoCapture(0)
    while True:
            name_namelist = []
            if oke_used == 1 :
                start_dect = time.time()
                oke_used=0
            if catch_used == 1 :
                start_scr = time.time()
                catch_used=0
            now=time.time()
            
            bgr_image = capture.read()[1]
            gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
            rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
            gray_image2 = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2RGB)
            gray_image2 = cv2.resize(gray_image2, (0, 0), fx=0.5, fy=0.5)
            frame = bgr_image
            
            if (oke_used < 1) & (pass_time(now,start_dect) >= 0.05) :
                
                gray_image3 = cv2.resize(gray_image2, (0, 0), fx=0.5, fy=0.5)
                face_locations = detector(gray_image2, 0)
                face_locations2 = detector(gray_image3, 0)
                features_cap_arr = []
                tmp_for_distance=[]
                for i in range(len(face_locations2)):
                    shape = predictor(gray_image3 , face_locations2[i])
                    features_cap_arr.append(facerec.compute_face_descriptor(gray_image3 , shape))
                
                
                if len(face_locations)==0:
                    if_face = 0
              
                matrix=[]
                for k in range(len(face_locations2)):
                    name_namelist.append("unknown")
                        # 对于某张人脸，遍历所有存储的人脸特征
                        # For every faces detected, compare the faces in the database
                    e_distance_list = []
                    for i in range(len(features_known_arr)):
                        
                        # 如果 person_X 数据不为空
                        if str(features_known_arr[i][0]) != '0.0':
                            print("with person", str(i + 1), "the e distance: ", end='')
                            e_distance_tmp = return_euclidean_distance(features_cap_arr[k], features_known_arr[i])
                            #print(e_distance_tmp)
                            e_distance_list.append(e_distance_tmp)
                            if min(e_distance_list) < 0.3:
                                break
                        else:
                            # 空数据 person_X
                            e_distance_list.append(999999999)
                    # Find the one with minimum e distance
                    similar_person_num = e_distance_list.index(min(e_distance_list))
                    print("Minimum e distance with person", int(similar_person_num)+1)
    
                    if min(e_distance_list) < 0.3:
                        print('the distance:',e_distance_list)
                        name_namelist[k] = "Person "+str(int(similar_person_num)+1)
                        print("May be person "+str(int(similar_person_num)+1))
                        
                        tmp_for_distance.append([k,csv_rd['奧客行為紀錄'][int(similar_person_num)],
                                                 csv_rd['建議方式紀錄'][int(similar_person_num)],face_locations2[k]])
                        print(tmp_for_distance)
                    else:
                        print("Unknown person")
                for k in range(len(face_locations)):

                    top = face_locations[k].top()
                    right = face_locations[k].right()
                    bottom = face_locations[k].bottom()
                    left = face_locations[k].left()
                    
                    top *= 2
                   
                    right *= 2
        
                    bottom *= 2
        
                    left *= 2
                    
                    pta = (left - 10, top - 10)
                    ptb = (right + 10, bottom + 10)
                    print("pta=",pta,",ptb=",ptb)
                 
                    gray_face_o = gray_image[top:bottom, left:right]
                    gray_face = gray_image[top:bottom, left:right]
                    try:
                        gray_face = cv2.resize(gray_face, (emotion_target_size))
                    except:
                        continue      
                    gray_face = preprocess_input(gray_face, True)
                    gray_face = np.expand_dims(gray_face, 0)
                    gray_face = np.expand_dims(gray_face, -1)
                    
                    emotion_prediction = emotion_classifier.predict(gray_face)
                    emotion_probability = np.max(emotion_prediction)
        
                    emotion_label_arg = np.argmax(emotion_prediction)
                    emotion_text = emotion_labels[emotion_label_arg]
                    emotion_window.append(emotion_text)
                    if len(emotion_window) > frame_window:
                        emotion_window.pop(0)
                        try:
                            emotion_mode = mode(emotion_window)
                        except:
                            emotion_mode =""
                            continue
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
                    
                    #oche_detect
                    gray_face_o=cv2.resize(gray_face_o, dim, fx=0, fy=0, interpolation=cv2.INTER_AREA)
                    input_images = gray_face_o.reshape(1, 10304)
                    labels = np.zeros((1, 2), dtype=np.int)
                    feed_dict = {x: input_images, y: labels}
                    temp = sess.run(f_softmax, feed_dict)
                    print(temp)
                    text="   "
                    ochepoint = int((temp[0, 0] * 100)/10)*10 + emotionpoint
                    if ochepoint >= 100 :
                        ochepoint=100
                    if ochepoint <= 0 :
                        ochepoint=0
                    matrix.append([top,right,bottom,left,emotion_mode,color,ochepoint])
                    oke_used = 1
                    if_face = 1
                    #end
                    
            if if_face == 1:
                face_count = k+1
                #print('face_count=',face_count)
                for j in range(face_count):
                    if len(matrix) == face_count:
                        top, right, bottom, left = matrix[j][0],matrix[j][1],matrix[j][2],matrix[j][3]
            
                        pta = (left - 10, top - 10)
                        ptb = (right + 10, bottom + 10)
                        
                        emotion_mode=matrix[j][4]
                        color= matrix[j][5]
                        ochepoint = matrix[j][6]
                        oketext = text+ str(ochepoint) +  "%   "
                        cv2.rectangle(rgb_image,ptb,(right+40,bottom-10), (0,0,0),-1)
                        cv2.rectangle(rgb_image,ptb,(right+40,int(bottom+10+(top-20-bottom)*ochepoint/100)), color, -1)
                        cv2.rectangle(rgb_image, ptb,pta, color, 2)
                        #draw_text(pta,(right-34,bottom+34),oketext, rgb_image, emotion_mode , color, 0, -45, 1, 1)
                        rgb_image = cv2ImgAddText(rgb_image, oketext , right-25 , bottom +12, color , 22)
                        rgb_image = cv2ImgAddText(rgb_image, emotion_mode , left-10 , top-37, color , 22)
                        for k in range(len(tmp_for_distance)):
                            if j == tmp_for_distance[k][0]:
                                rgb_image = cv2ImgAddText(rgb_image, tmp_for_distance[k][1] , tmp_for_distance[k][3].right()*4-40
                                                          , tmp_for_distance[k][3].top()*4-35, color , 22)
                                rgb_image = cv2ImgAddText(rgb_image, tmp_for_distance[k][2] , tmp_for_distance[k][3].left()*4
                                                          , tmp_for_distance[k][3].bottom()*4 , color , 22)
                                     
                if (catch_used == 0) & (pass_time(now,start_scr) > 10) :
                    for j in range(face_count):
                        if len(matrix) == face_count:
                            ochepoint = matrix[j][6]
                            top, right, bottom, left = matrix[j][0],matrix[j][1],matrix[j][2],matrix[j][3]
                            gbr_img=frame[top:bottom, left:right]
                            
                            if ochepoint >= aut_capture_max :
                                t = datetime.datetime.now().strftime('%Y_%m_%d_%H-%M-%S-%f')
                                face = cv2.resize(gbr_img, dim, fx=0, fy=0, interpolation=cv2.INTER_AREA)
                                imageL = "./faces/suspects/" + t + ".bmp"
                                cv2.imwrite(imageL,face)
                                #socket_Client('1',imageL)
                                start_oka_save=time.time()
                                print("已截圖成功")
                                flag_test=1
                                scr_cd=1
                            elif ochepoint <= aut_capture_min :
                                t = datetime.datetime.now().strftime('%Y_%m_%d_%H-%M-%S-%f')
                                face = cv2.resize(gbr_img, dim, fx=0, fy=0, interpolation=cv2.INTER_AREA)
                                imageL = "./faces/suspects/" + t + ".bmp"
                                cv2.imwrite(imageL,face)
                                #socket_Client('1',imageL)
                                print("已截圖成功")
                                scr_cd=1
                                
                            if ochepoint >= okewarning:
                                find_oka=1
                                print('find_oka=',find_oka)
                                oka_t=datetime.datetime.now().strftime('%H : %M : %S')
                                
                    if scr_cd==1:
                        scr_cd=0
                        catch_used = 1
                if (check_globalvalue()) :
                    for j in range(face_count):
                        if len(matrix) == face_count:
                            ochepoint = matrix[j][6]
                            top, right, bottom, left = matrix[j][0],matrix[j][1],matrix[j][2],matrix[j][3]
                            print(top,right,bottom,left)
                            gbr_img=frame[top:bottom, left:right]
                            t = datetime.datetime.now().strftime('%Y_%m_%d_%H-%M-%S-%f')
                            face = cv2.resize(gbr_img, dim, fx=0, fy=0, interpolation=cv2.INTER_AREA)
                            cv2.imwrite("./faces/suspects/" + t + ".bmp",face)
                            #socket_Client('1',imageL)
                            print("已手動截圖成功")
                            start_push=time.time()
                            push_p=1
                    face_flagdown()
                kk=cv2.waitKey(1)
                if kk == (ord('p') or ord('P')):
                        for j in range(face_count):
                            if len(matrix) == face_count:
                                ochepoint = matrix[j][6]
                                top, right, bottom, left = matrix[j][0],matrix[j][1],matrix[j][2],matrix[j][3]
                                print(top,right,bottom,left)
                                gbr_img=frame[top:bottom, left:right]
                                t = datetime.datetime.now().strftime('%Y_%m_%d_%H-%M-%S-%f')
                                face = cv2.resize(gbr_img, dim, fx=0, fy=0, interpolation=cv2.INTER_AREA)
                                cv2.imwrite("./faces/suspects/" + t + ".bmp",face)
                                #socket_Client('1',imageL)
                                push_p=1
                                start_push=time.time()
                                print("已手動截圖成功")
                elif  kk == (ord('q') or ord('Q')):
                        break
                
                if cv2.getWindowProperty(winname, 0) < 0:
                    break

            if find_oka == 1:
                start_oka = time.time()
                flag_war = 1
                print('flag_war=',flag_war)
                find_oka = 0
                
            if push_p == 1 :
                rgb_image = cv2ImgAddText(rgb_image , "已保存" ,  550, 400, (0, 255 , 0), 20)
                if  pass_time(now,start_push) > 5 :
                    push_p = 0
                    
            if flag_war == 1 and pass_time(now,start_oka) < 10:
                oka_time_text="在 "+oka_t+" 時發現奧客!!"
                rgb_image = cv2ImgAddText(rgb_image, oka_time_text, 0, 0, (255, 0 , 0), 30)
            elif flag_war ==1 :
                flag_war = 0
                
            if flag_test == 1 and pass_time(now,start_oka_save) < 5:
                rgb_image = cv2ImgAddText(rgb_image , "資料待處理" ,  550, 425, (255, 0 , 0), 20)
            elif flag_test == 1:
                flag_test = 0
                
            rgb_image = cv2ImgAddText(rgb_image, "p鍵擷臉", 550, 450, (0, 255, 0), 20)
            bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
            cv2.imshow(winname, bgr_image)
            
            if cv2.waitKey(1) & 0xFF == (ord('q') or ord('Q')):
                    break
                
            if cv2.getWindowProperty(winname, 0) < 0:
                    break
    capture.release()
    cv2.destroyAllWindows()
#prediction_client()