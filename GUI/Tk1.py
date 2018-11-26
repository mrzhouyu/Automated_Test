from tkinter import Frame
import tkinter as tk
from tkinter import messagebox
from Requests.AutoOta import Filter,Api

root=tk.Tk()

root.title('Auto Ota')

#左边框
# #定义左边框
leftFrame = Frame(root, width=600, height=400)
leftFrame.propagate(False)
leftFrame.pack(side='left')

deviceList=[('GWSL',1),('CDSC',2),('GWFL',3)]
v=tk.IntVar()
for lang,num in deviceList:
    choiceFrame=Frame(leftFrame,width=100,height=50,bg='red')
    choiceFrame.propagate(False)
    choiceFrame.pack(side='left',anchor='e',padx=5,pady=5)
    Radio=tk.Radiobutton(choiceFrame,text=lang,variable=v,value=num)
    Radio.grid_propagate(0)
    Radio.grid(row=1,column=1)

root.mainloop()