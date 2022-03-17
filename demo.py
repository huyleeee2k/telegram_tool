from tkinter import *
import tkinter
from tkinter import messagebox as mess
from tkinter import filedialog
import os,psutil

window = Tk()

def initUI():
    window.title("App telegram")
    window.geometry("600x600")

def isOpen():
    for process in (process for process in psutil.process_iter() if process.name()=="Telegram.exe"):
        return True
    return False

def openTeleGram():
    #mess.showinfo("Hello", "Lo cc")
    #filepath = filedialog.askopenfilename()
    #print('"%s"' % filepath)
    if not isOpen():
        dir = "C:/Users/MOBOT/AppData/Roaming/Telegram Desktop/Telegram.exe"
        os.startfile(dir)
        
    
def closeTeleGram():
    for process in (process for process in psutil.process_iter() if process.name()=="Telegram.exe"):
        process.kill()
        break

#Khởi tạo file giao diện
initUI()

btnOpen = tkinter.Button(window,text="Mở telegram", command= openTeleGram)
btnOpen.pack(pady=20)

btnCloes = tkinter.Button(window,text="Đóng telegram", command= closeTeleGram)
btnCloes.pack(pady=20)
#btnCloes.place(x = 260, y = 60)

window.mainloop()