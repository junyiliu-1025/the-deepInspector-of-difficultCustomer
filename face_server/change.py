
import tkinter as tk
from tkinter import ttk,messagebox
from csvfuntion import change_new,load_and_tmp,printdata

def close(root):
    root.destroy()
    root.quit()


def change(name,target,target_content):
    
    window = tk.Tk()
    window.title('修改')
    
    ##窗口尺寸
    window.geometry('200x200')
    target_id = tk.Label(window,text="修改目標ID:"+str(target))
    target_id .pack()
    
    target_content_label = tk.Label(window,text="修改目標值:"+target_content)
    target_content_label.pack()
    
    content = tk.Entry(window)
    content.pack()
    
    def insert_point(root):
        if messagebox.askyesno('修改','是否確定修改該數值', parent=root) :
            load_and_tmp(name)
            printdata(name)
            var = content.get()
            change_new(name,int(target),var)
        else:
            messagebox.showinfo("No", "取消修改", parent=root)
        
        close(window)
        
    change_button = tk.Button(window,text="修改",width=15,height=2,command=lambda:insert_point(window))
    change_button.pack() 
    
    exit_button = tk.Button(window,text="離開",command=lambda:close(window))
    exit_button .pack()
    
    ##显示出来
    window.mainloop()