
import tkinter as tk
from tkinter import ttk,PhotoImage,messagebox
from csvfuntion import add_new,load_and_tmp,printdata,change_new
import tkinter.font as tkFont
from face_function import images_path, text_wd, text_hi
from PIL import Image, ImageTk
from face_function import back_ground

bg = "bg0.png" #背景

def close(root):
    root.destroy()
    root.quit()


def addnewdata(name,root):
    
    window = tk.Toplevel()
    window.title('事件管理-新增')
    icon = PhotoImage(file= images_path + 'AI_system.png')
    window.tk.call('wm','iconphoto',window._w, icon)
    
    #color table
    photo = Image.open(images_path + bg)
    photo = photo.resize((300, 200), Image.ANTIALIAS)
    ph = ImageTk.PhotoImage(photo)
    
    img_label = tk.Label(window,image=ph)  #图片
    img_label.pack()
    
    ##窗口尺寸
    window.geometry('300x200')
    ft = tkFont.Font(size=12, weight=tkFont.BOLD)
    window.option_add("*Font", ft)
    target_content_label = tk.Label(window,text="輸入想新增的內容:",font=ft,background='white')
    target_content_label.place(relx=0.13,rely=0.2) 
    
    content = tk.Entry(window,font=('Verdana',14))
    content.place(relx=0.1,rely=0.35) 
    def insert_point(root):
       if messagebox.askyesno('新增','是否確定新增該數值', parent=root) :
            var = content.get()
            if var.replace(' ','') != '':
                load_and_tmp(name)
                printdata(name)
                #print("add_new")
                add_new(name,var)
                messagebox.showinfo('頗有深度的奧客稽查員','新增成功')
                close(window)
            else:
                messagebox.showinfo('頗有深度的奧客稽查員','請不要留空白')
                
       else:
            messagebox.showinfo("No", "取消新增", parent=root)
            close(window)
    p_change = back_ground(300, 200, bg, 0.2, 0.6, text_wd//3, text_hi//2, "new.png")
    change_button = tk.Button(window,text="新增",image=p_change,command=lambda:insert_point(root))
    change_button.place(relx=0.2,rely=0.6) 
    
    p_exit = back_ground(300, 200, bg, 0.55, 0.6, text_wd//3, text_hi//2, "leave.png")
    exit_button = tk.Button(window,text="離開",image=p_exit,command=lambda:close(window))
    exit_button.place(relx=0.55,rely=0.6)
    

    
    ##显示出来
    window.resizable(width=False, height=False)
    window.mainloop()

def change(name,target,target_content):
    
    window = tk.Toplevel()
    window.title('事件管理-修改')
    icon = PhotoImage(file= images_path + 'AI_system.png')
    window.tk.call('wm','iconphoto',window._w, icon)
    
    #color table
    photo = Image.open(images_path + bg)
    photo = photo.resize((300, 200), Image.ANTIALIAS)
    ph = ImageTk.PhotoImage(photo)
    
    img_label = tk.Label(window,image=ph)  #图片
    img_label.pack()
    
    #window.configure(background='#FFFFFF')
    ##窗口尺寸
    window.geometry('300x200')
    ft = tkFont.Font(size=12, weight=tkFont.BOLD)
    window.option_add("*Font", ft)
    target_id = tk.Label(window,text="修改目標ID:"+str(target),font=ft,background='white')
    target_id.place(relx=0.13,rely=0.1) 
    
    target_content_label = tk.Label(window,text="修改目標值:"+target_content,font=ft,background='white')
    target_content_label.place(relx=0.13,rely=0.23) 
    
    content = tk.Entry(window,font=('Verdana',14))
    content.place(relx=0.1,rely=0.35) 
    
    def insert_point(root):
         if messagebox.askyesno('修改','是否確定修改該數值', parent=root) :
            var = content.get()
            if var.replace(' ','') != '':
                load_and_tmp(name)
                printdata(name)
                #print("add_new")
                change_new(name,int(target),var)
                messagebox.showinfo('頗有深度的奧客稽查員','修改成功')
                close(window)
            else:
                messagebox.showinfo('頗有深度的奧客稽查員','請不要留空白')
         else:
            messagebox.showinfo("No", "取消修改", parent=root)
            close(window)
        
    p_change = back_ground(300, 200, bg, 0.2, 0.6, text_wd//3, text_hi//2, "modify.png")
    change_button = tk.Button(window,text="修改",image=p_change,command=lambda:insert_point(window))
    change_button.place(relx=0.2,rely=0.6) 
    
    p_exit = back_ground(300, 200, bg, 0.55, 0.6, text_wd//3, text_hi//2, "leave.png")
    exit_button = tk.Button(window,text="離開",image=p_exit,command=lambda:close(window))
    exit_button.place(relx=0.55,rely=0.6)
    
    ##显示出来
    window.resizable(width=False, height=False)
    window.mainloop()