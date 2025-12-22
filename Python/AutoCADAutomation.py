from tkinter import *
from tkinter import messagebox
from tkinter import PhotoImage
from SeperateLayout import SeperateLayouts
from ReplaceTextByMLeader import ReplaceTextByMLeader
import requiredicon, base64, os
class AutoCADAutomation:
    @staticmethod
    def getCache():
        byteData = base64.b64decode(requiredicon.iconvar)
        iconImage = open(".icon.ico", "wb")
        iconImage.write(byteData)
        iconImage.close()
    @staticmethod
    def cleanCache():
        try:
            os.remove(".icon.ico")
        except:
            pass
    responseOfReplaceTextByMLeader=False
    responseOfSeperateLayout=False
    window=Tk()
    window.title("AutoCAD Automation")
    window.geometry("600x500")
    @classmethod
    def run(cls):
        AutoCADAutomation.cleanCache()
        w=cls.window
        #<<<--------------Handling the icon image ------------>>>
        if w.tk.call('tk', 'windowingsystem') == 'win32':
            AutoCADAutomation.getCache()
            w.iconbitmap(default="icon.ico")
            AutoCADAutomation.cleanCache()
        #<<<--------------wigets section--------------------->>>
        #<<<----welcome message---->>>
        introLabel = Label(w,text="<<<----Welcome to Autocad Automation Framework---->>>", font=("Helvetica", 15, "bold"))
        introLabel.pack()
        # bg = PhotoImage(file="imgbg.png")
        # bgLabel = Label(w, image=bg)
        # bgLabel.place(relwidth=1, relheight=1)
        seperateLayoutBtn = Button(w,text="Seperate Layouts", font=("Helvetica", 10, "bold"))
        seperateLayoutBtn.pack(anchor="nw")
        w.mainloop()
    @classmethod
    def runReplaceTextByMLeader(cls, layerName, ifText, ifMtext):
        replaceTextByMleader = ReplaceTextByMLeader()
        cls.responseOfReplaceTextByMLeader = replaceTextByMleader.doReplace(layerName, ifText, ifMtext)
        return cls.responseOfReplaceTextByMLeader
    @classmethod
    def runSeperateLayout(cls, path_to_source_dwg, path_to_result_dir):
        seperateLayout = SeperateLayouts()
        cls.responseOfSeperateLayout = seperateLayout.doSeparate(path_to_source_dwg, path_to_result_dir)
        return cls.responseOfSeperateLayout
ins = AutoCADAutomation()
ins.run()