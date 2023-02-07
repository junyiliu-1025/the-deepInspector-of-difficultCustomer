import tkinter as tk
import csv

from csvfuntion import array,nullplace,load_and_tmp,printdata
window = tk.Tk()
window.title('事件管理')
window.geometry('800x600')
window.configure(background='white')


load_and_tmp("oke")
printdata("oke")

#创建Listbox
columns=("a","b")
treeview=ttk.Treeview(window,height=5,show="headings",columns=columns )#表格 
vbar = ttk.Scrollbar(window,orient=VERTICAL,command=treeview.yview)#表格的滾軸


treeview.configure(yscrollcommand=vbar.set)

treeview.column('a', width=150, anchor='center') 
treeview.column('b', width=150, anchor='center') 
treeview.heading('a', text=array[0][0][0])
treeview.heading('b', text=array[0][0][1])

for i in range(len(array[0])):
    if i == 0:
        continue
    if len(array[0][i])==0:
        continue
    treeview.insert('',i,values=(array[0][i][0],array[0][i][1]))

treeview.grid(row=2, column=0, columnspan=1, sticky="NSEW")
vbar.grid(row=2, column=1, sticky="NS")
window.mainloop()