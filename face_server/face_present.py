#face_login.py
#1. 匯入模組與類別
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage,messagebox
from PIL import Image, ImageTk

#from face_socketClient import socket_Client_confirm
from face_function import images_path, sc_wd, sc_hi, img_hi, img_wd, text_wd, text_hi
from face_function import back_ground, close
from face_object import CreateToolTip
import socket
import os 

#2. 定義元件之事件處理函數
def file_client_run():
    messagebox.showinfo("頗有深度的奧客稽查員","登入成功")
    os.popen("python face_system.py")
    root.destroy()

def read_file(file):
    project_var = []
    with open(file,'r') as f:
        data = f.readlines()
        for i in data:
            data = i.strip('\n').split(':')
            project_var.append(data)
    return dict(project_var)

def change_variables(file,old,new): 
    file_data = ""
    with open(file,'r+') as f:
        for line in f.readlines():
            if(line.find(old+':')==0):
                line = old+':%s' % (new) + '\n'
            file_data += line
    with open(file,"w+") as f:
        f.write(file_data)

def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ss.connect(('8.8.8.8', 80))
        ip = ss.getsockname()[0]
    finally:
        ss.close()

    return ip

#file_client_run()
data = read_file('face_variable.txt')

#3. 建立最上層視窗, 設定標題與大小
root = tk.Tk()
root.title("頗有深度的奧客稽查員-Server登入")

icon = PhotoImage(file= images_path + 'AI_system.png')
root.tk.call('wm','iconphoto',root._w, icon)
#root.iconbitmap(images_path + 'ai.png')
#root.configure(background='#DDDDDD')

#window sc_wd, sc_hi from face_function_client
bg = "sign_in.png" #背景
login_wd = int(sc_wd // 5 * 4)
login_hi = int(sc_hi // 10 * 7)

#color table
photo = Image.open(images_path + bg)
photo = photo.resize((login_wd, login_hi), Image.ANTIALIAS)
ph = ImageTk.PhotoImage(photo)

img_label = tk.Label(root,image=ph)  #图片
img_label.pack()

#1264,915 my_notebook
root.geometry('%sx%s'%(login_wd, login_hi))

# You have to use styles to customize ttk widgets.
#s = ttk.Style()
#s.configure('my.TButton', font=('Helvetica', 24), width=10, borderwidth=0, relief="raised", background='white')
bd = ttk.Style()
bd.configure('bd.TButton', borderwidth=0, relief="raised", background='white')

#button_click

#4. 加入 tk/ttk 元件並指定事件處理函數
#back_ground(sc_wd, sc_hi, bg, rx, ry, rw, rh, fg)
#ip = tk.Text(root,height=3,width=10)
'''
ip_label = ttk.Label(root,font=('Verdana',28),text="Server IP:")
ip_label.place(relx=0.13,rely=0.5)
'''
ps = back_ground(login_wd, login_hi, bg, 0.16, 0.4, img_wd, img_hi, "server_ip.png")
server_ip = ttk.Button(root, style='bd.TButton', image=ps)
CreateToolTip(server_ip, text=' Server-IP ')
server_ip.place(relx=0.16,rely=0.4)

ip_address = tk.StringVar(value= get_host_ip())
ip = ttk.Entry(root,font=('Verdana',28),textvariable=ip_address, state='disabled')
ip.place(relx=0.4,rely=0.5)

pl = back_ground(login_wd, login_hi, bg, 0.16, 0.83, img_wd, img_hi //5 * 2, "login.png")
system_login = ttk.Button(root, style='bd.TButton', image=pl,command=file_client_run)
system_login.place(relx=0.16,rely=0.83)

pc = back_ground(login_wd, login_hi, bg, 0.66, 0.83, img_wd, img_hi //5 * 2, "close.png")
system_close = ttk.Button(root, style='bd.TButton', image=pc, command=lambda:close(root))
system_close.place(relx=0.66,rely=0.83)

#5. 啟始事件迴圈顯示視窗
root.resizable(width=False, height=False)
root.mainloop()
