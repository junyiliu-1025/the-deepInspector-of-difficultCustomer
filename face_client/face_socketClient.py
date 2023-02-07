# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 21:49:40 2019

@author: junyi
"""
from socket import socket
#from face_login import data
from tkinter import messagebox
import os
import shutil
import time
import tkinter.font as tkFont
import tkinter as tk
from tkinter import ttk
from tkinter import Canvas,Scrollbar,Frame,Text
from tkinter import END,DISABLED
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

def read_file(file):
    project_var = []
    with open(file,'r',encoding='utf-8') as f:
        data = f.readlines()
        for i in data:
            data = i.strip('\n').split(':')
            project_var.append(data)
    return dict(project_var)

def change_variables(file,old,new): 
    file_data = ""
    with open(file,'r+',encoding='utf-8') as f:
        for line in f.readlines():
            if(line.find(old+':')==0):
                line = old+':%s' % (new) + '\n'
            file_data += line
    with open(file,"w+",encoding='utf-8') as f:
        f.write(file_data)
        
def file_client_run():
    os.popen("python face_client.py")

def socket_Client(kind,name):
    CHUNKSIZE = 1_000_000
    data = read_file('face_variable.txt')
    print(data['IP'])
    filename = name
    flag = kind
    flag = flag.encode('utf-8')
    sock = socket()
    sock.connect((data['IP'],5000))
    sock.sendall(flag)
    with sock,open(filename,'rb') as f:
        sock.sendall(filename.encode() + b'\n')
        sock.sendall(f'{os.path.getsize(filename)}'.encode() + b'\n')

        # Send the file in chunks so large files can be handled.
        while True:
            data = f.read(CHUNKSIZE)
            if not data: break
            sock.sendall(data)
    time.sleep(0.01)

def socket_Client_model(root):
    if messagebox.askyesno("頗有深度的奧客稽查員", "確定下載最新模型?", parent=root):
        shutil.rmtree('./models/model_oka')
        os.mkdir('./models/model_oka')
        ft = tkFont.Font(size=16, weight=tkFont.BOLD)
        textbox = Text(root, font=ft, width=25, height=15, background='white')
        textbox.place(relx=0.715, rely=0.01) 
        ## Frame in textbox
        frmbox = Frame(textbox)
        ## Update display to get correct dimensions
        frmbox.update_idletasks()
    
        CHUNKSIZE = 1_000_000
        flag = '3'
        flag = flag.encode('utf-8')
        var_data = read_file('face_variable.txt')
        model_arr = ["checkpoint","my-gender-v1.0.meta","my-gender-v1.0.index","my-gender-v1.0.data-00000-of-00001"]
        for i in range(4):
            model_arr[i] = model_arr[i].encode('utf-8')
            sock = socket()
            sock.connect((var_data['IP'],5000))
            sock.sendall(flag)
            sock.sendall(model_arr[i])
            with sock, sock.makefile('rb') as sockfile:
                filename = sockfile.readline().strip().decode()
                length = int(sockfile.readline())
                print(f'Downloading {filename}:{length}...')
                path = os.path.join('./models/model_oka',filename)
            
                with open(path,'wb') as f:
                    while length:
                        chunk = min(length,CHUNKSIZE)
                        data = sockfile.read(chunk)
                        if not data: break
                        f.write(data)
                        length -= len(data)
            textbox.insert(END,"模型已下載 "+str(i+1)+"/4\n")
            frmbox.update_idletasks()
        textbox.insert(END,"模型已完整下載\n")
        frmbox.update_idletasks()
    else:
        messagebox.showinfo("頗有深度的奧客稽查員","已取消下載",parent=root)
def socket_Client_confirm(ip,root):
    flag = '4'
    flag = flag.encode('utf-8')
    try:
        print(ip)
        sock = socket()
        sock.settimeout(0.5 )
        sock.connect((ip,5000))
        sock.settimeout(None)
        sock.sendall(flag)
        conn = sock.recv(1024)
        print(conn)
        if conn:
            messagebox.showinfo("頗有深度的奧客稽查員","連線成功",parent=root)
            change_variables('./face_variable.txt','IP',ip)
            file_client_run()
            root.destroy()
    except:
        messagebox.showinfo("頗有深度的奧客稽查員","連線失敗",parent=root)
#socket_Client_all("./okes")
#print(os.listdir("./okes"))
