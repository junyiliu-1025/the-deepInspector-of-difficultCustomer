# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 14:10:14 2019

@author: chun8
"""
import pandas as pd
import os
import numpy as np
from csvfuntion import add_new,load_and_tmp,printdata,add_new
np.set_printoptions(suppress=True)
#load_and_tmp('costo')

#printdata('costo')
from tkinter import messagebox
import shutil
import cv2
import os
import dlib
from skimage import io
import csv
import numpy as np

# 要读取人脸图像文件的路径
path_images_from_camera = './faces/rec/face_oke/'

# Dlib 正向人脸检测器
detector = dlib.get_frontal_face_detector()

# Dlib 人脸预测器
predictor = dlib.shape_predictor("./recognition_model/shape_predictor_5_face_landmarks.dat")

# Dlib 人脸识别模型
# Face recognition model, the object maps human faces into 128D vectors
face_rec = dlib.face_recognition_model_v1("./recognition_model/dlib_face_recognition_resnet_model_v1.dat")

# 返回单张图像的 128D 特征
def return_128d_features(path_img):
    img_rd = io.imread(path_img)
    img_gray = cv2.cvtColor(img_rd, cv2.COLOR_BGR2RGB)
    img_gray=cv2.resize(img_gray,(0, 0), fx=0.5, fy=0.5)
    faces = detector(img_gray, 1)
    print(faces)
    print("%-40s %-20s" % ("检测到人脸的图像 / image with faces detected:", path_img), '\n')

    # 因为有可能截下来的人脸再去检测，检测不出来人脸了
    # 所以要确保是 检测到人脸的人脸图像 拿去算特征
    if len(faces) != 0:
        shape = predictor(img_gray, faces[0])
        face_descriptor = face_rec.compute_face_descriptor(img_gray, shape)
    else:
        face_descriptor = 0
        print("no face")

    return face_descriptor


# 将文件夹中照片特征提取出来, 写入 CSV
def return_features_mean_personX(path_faces_personX):
    features_list_personX = []
    photos_list = os.listdir(path_faces_personX)
    if photos_list:
        for i in range(len(photos_list)):
            # 调用return_128d_features()得到128d特征
            print("%-40s %-20s" % ("正在读的人脸图像 / image to read:", path_faces_personX + "/" + photos_list[i]))
            features_128d = return_128d_features(path_faces_personX + "/" + photos_list[i])
            #  print(features_128d)
            # 遇到没有检测出人脸的图片跳过
            if features_128d == 0:
                i += 1
            else:
                features_list_personX.append(features_128d)
    else:
        print("文件夹内图像文件为空 / Warning: No images in " + path_faces_personX + '/', '\n')

    # 计算 128D 特征的均值
    # personX 的 N 张图像 x 128D -> 1 x 128D
    if features_list_personX:
        features_mean_personX = np.array(features_list_personX).mean(axis=0)
    else:
        features_mean_personX = np.array(['0'])

    return features_mean_personX


# 获取已录入的最后一个人脸序号 / get the num of latest person
def TrainAndInput(root,face_folder,oke_behavior_record,response_select):
    csv_file = pd.read_csv('costo.csv')
  #  person_list = os.listdir('./faces/rec/face_oke/')
    person_num_list = []
    for face in face_folder:
        face_folder[face_folder.index(face)] = int(face.lstrip('0')) 
    for person in csv_file['顧客ID']:
        person_num_list.append(person)
    #person_cnt = max(person_num_list)
    #csv_file = csv_file.dropna()
    #print('TrainAndInput',csv_file['顧客ID'])
    #print("person_num_list:",person_num_list)
   
    for person in face_folder:
        # Get the mean/average features of face/personX, it will be a list with a length of 128D
        #print(path_images_from_camera + "person_"+str(person+1))
        if person not in person_num_list:
            features_mean_personX = return_features_mean_personX(path_images_from_camera + str(int(person)).zfill(3))
            if features_mean_personX == np.array(['0']):
                messagebox.showinfo('頗有深度的奧客稽查員','找不到此圖的人臉，請另選一張。',parent=root)
                shutil.move('./faces/rec/all/'+str(face_folder[-1]).zfill(3)+'.bmp','./faces/unfaces/')
                shutil.rmtree('./faces/rec/face_oke/'+str(face_folder[-1]).zfill(3).rstrip('.bmp'))
                return 1
            else:
                load_and_tmp('costo')
                add_new('costo',list(features_mean_personX),oke_behavior_record,response_select)
                return 0
            #printdata('costo')
            #print("特征均值 / The mean of features:", list(features_mean_personX))
            #print('\n')
            print("奧客已儲存")
        else:
            print('已存在')
   

    
    