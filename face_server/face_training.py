import  tensorflow as tf
import  face_train_data as train_data
import  cv2
import  random
import  matplotlib.pyplot as plt
import  numpy as np
from sklearn.metrics import confusion_matrix, classification_report
import os
from tkinter import Text
from tkinter import END,DISABLED
import tkinter.font as tkFont
import shutil
train_epochs=5000
batch_size = 30
drop_prob = 0.5
learning_rate=0.0001
def model_training(root,textbox):
    percent = 5
    textbox.insert(END,"模型正在建立...\n")
        # 指定字体名称、大小、样式

    #顯示模型建立資訊

    #textbox.insert(END,"模型訓練已完成: 10 %\n模型訓練已完成: 20 %\n模型訓練已完成: 30 %\n模型訓練已完成: 40 %\n模型訓練已完成: 50 %\n模型訓練已完成: 60 % \n模型訓練已完成: 70 %\n模型訓練已完成: 80 %\n模型訓練已完成: 90 %\n模型訓練已完成: 100 %\n預測模型已訓練完成。\n")
    #for i in range(10):
        #textbox.insert(END, str(i) + "\n")

    # 禁止輸入

       
 
    
    def weight_init(shape):
        weight = tf.truncated_normal(shape,stddev=0.1,dtype=tf.float32)
        return tf.Variable(weight)
    
    
    def bias_init(shape):
        bias = tf.random_normal(shape,dtype=tf.float32)
        return tf.Variable(bias)
    images_input = tf.placeholder(tf.float32,[None,112*92],name='input_images')
    labels_input = tf.placeholder(tf.float32,[None,2],name='input_labels')
    
    def fch_init(layer1,layer2,const=1):
        min = -const * (6.0 / (layer1 + layer2));
        max = -min;
        weight = tf.random_uniform([layer1, layer2], minval=min, maxval=max, dtype=tf.float32)
        return tf.Variable(weight)
    
    def conv2d(images,weight):
        return tf.nn.conv2d(images,weight,strides=[1,1,1,1],padding='SAME')
        
    def max_pool2x2(images,tname):
        return tf.nn.max_pool(images,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME',name=tname)
    
        #here has been changed
    x_input = tf.reshape(images_input,[-1,112,92,1])
    
    
    #here has been changed
    # 第一層卷積
    w1 = weight_init([3,3,1,16])
    b1 = bias_init([16])
    # 结果 NHWC  N H W C
    conv_1 = conv2d(x_input,w1)+b1
    relu_1 = tf.nn.relu(conv_1,name='relu_1')
    max_pool_1 = max_pool2x2(relu_1,'max_pool_1')
    
    
    # 第二層卷積
    w2 = weight_init([3,3,16,32])
    b2 = bias_init([32])
    conv_2 = conv2d(max_pool_1,w2) + b2
    relu_2 = tf.nn.relu(conv_2,name='relu_2')
    max_pool_2 = max_pool2x2(relu_2,'max_pool_2')
    
    # 第三層卷積
    w3 = weight_init([3,3,32,64])
    b3 = bias_init([64])
    conv_3 = conv2d(max_pool_2,w3)+b3
    relu_3 = tf.nn.relu(conv_3,name='relu_3')
    max_pool_3 = max_pool2x2(relu_3,'max_pool_3')
    
    
    
    
    
    f_input = tf.reshape(max_pool_3,[-1,14*12*64])
    
        #全連階層第一層
    f_w1= fch_init(14*12*64,512)
    f_b1 = bias_init([512])
    f_r1 = tf.matmul(f_input,f_w1) + f_b1
    f_relu_r1 = tf.nn.relu(f_r1)
    f_dropout_r1 = tf.nn.dropout(f_relu_r1,drop_prob)
    
    #全連階層第二層
    f_w2 = fch_init(512,128)
    f_b2 = bias_init([128])
    f_r2 = tf.matmul(f_dropout_r1,f_w2) + f_b2
    f_relu_r2 = tf.nn.relu(f_r2)
    f_dropout_r2 = tf.nn.dropout(f_relu_r2,drop_prob)
    
    
    #輸出層
    f_w3 = fch_init(128,2)
    f_b3 = bias_init([2])
    f_r3 = tf.matmul(f_dropout_r2,f_w3) + f_b3
    
    f_softmax = tf.nn.softmax(f_r3,name='f_softmax')
    
    
    #定義交叉熵
    cross_entry =  tf.reduce_mean(tf.reduce_sum(-labels_input*tf.log(f_softmax)))
    optimizer  = tf.train.AdamOptimizer(learning_rate).minimize(cross_entry)
    
    #計算準確率
    arg1 = tf.argmax(labels_input,1)
    arg2 = tf.argmax(f_softmax,1)
    cos = tf.equal(arg1,arg2)
    acc = tf.reduce_mean(tf.cast(cos,dtype=tf.float32))
    
    
    init = tf.global_variables_initializer()
    
    sess = tf.Session()
    
    sess.run(init)
    
    
    
    Cost = []
    Accuracy=[]
    for i in range(train_epochs):
        idx=random.randint(0,len(train_data.images)-20)
        batch= random.randint(6,18)
        train_input = train_data.images[idx:(idx+batch)]
        train_labels = train_data.labels[idx:(idx+batch)]
        result,acc1,cross_entry_r,cos1,f_softmax1,relu_1_r= sess.run([optimizer,acc,cross_entry,cos,f_softmax,relu_1],feed_dict={images_input:train_input,labels_input:train_labels})
        #print (acc1)
        part = (i/train_epochs*100)
        if part >= percent:
            textbox.insert(END,"模型訓練已完成:"+str(percent)+"%...\n")
            percent += 5
        print("模型訓練已完成:","%0.2f"% (i/train_epochs*100),"%")
        if i == 4999:
            #textbox.delete(0.0,END)
            textbox.insert(END,"模型訓練已完成:100%\n模型已訓練完成。")
            textbox.config(state=DISABLED)
            print("模型訓練已完成: 100%","\n預測模型已訓練完成。")          
        Cost.append(cross_entry_r)
        Accuracy.append(acc1)
    # loss function
    fig1,ax1 = plt.subplots(figsize=(10,7))
    plt.plot(Cost)
    ax1.set_xlabel('Epochs')
    ax1.set_ylabel('Cost')
    plt.title('Cross Loss')
    plt.grid()
    plt.show()
    
    # Accuracy
    fig7,ax7 = plt.subplots(figsize=(10,7))
    plt.plot(Accuracy)
    ax7.set_xlabel('Epochs')
    ax7.set_ylabel('Accuracy Rate')
    plt.title('Train Accuracy Rate')
    plt.grid()
    plt.show()
    
    
    #测试
    arg2_r = sess.run(arg2,feed_dict={images_input:train_data.test_images,labels_input:train_data.test_labels})
    arg1_r = sess.run(arg1,feed_dict={images_input:train_data.test_images,labels_input:train_data.test_labels})
    
    textbox.insert(END,classification_report(arg1_r, arg2_r))
    print(confusion_matrix(arg1_r,arg2_r))
    #保存模型
    shutil.rmtree('./models/model_oka')
    os.makedirs('./models/model_oka')
    saver = tf.train.Saver()
    saver.save(sess, './models/model_oka/my-gender-v1.0')
    