# -*- coding: utf-8 -*-
"""
@version: 1.1
@author: Kenneth
"""

import Tkinter as tk
import tkFont
import tkFileDialog as tfd
from PIL import Image, ImageFilter
from tkMessageBox import showerror, showwarning, showinfo

color_gray = "#BBB"
color_black = "#000"

def toolHelp():
    showinfo(title="Help", message="1) Browse and select your image.\n"
                                    +"2) Choose a blur strength and press 'Blur'\n"
                                    +"3) Done! ^_^\n"
                                    +"Note: Image will be saved with '_blurred' attached to the name; e.g image_blurred.jpg")
def clearEntry():
    if(path_entry_var.get() == "browse to select a file..."):
        path_entry.config(fg=color_black)
        path_entry_var.set("")
def restoreEntry():
    if(path_entry_var.get() == ""):
        path_entry.config(fg=color_gray)
        path_entry_var.set("browse to select a file...")
def entryUpdate(a,b,c):
    path_entry.config(fg=color_black)

def getPath():
    #Get path
    path_label_var.set("waiting")
    report_label_var.set("")
    save_label_var.set("")
    path_entry.config(fg=color_gray)
    path_entry_var.set("browse to select a file...")
    file_options = {'initialdir':'/',
                                  'title':'Choose file(s) to load',
                                  'filetypes':[('JPEG','*.jpg *.jpeg'),
                                               ('Bitmap Image','*.bmp'),
                                               ('PNG Image','*.png')]}
    file_path = tfd.askopenfilename(parent=root, **file_options)
    if(len(file_path) > 0):
        path_entry.config(fg=color_black)
        path_entry_var.set(file_path)
        path_label_var.set("Selected: ["+getFileName(file_path)+"]")

def getFileName(path):
    filestring_split = path.split('/')
    len_split = len(filestring_split)
    
    filename = filestring_split[len_split-1]
    return filename

def getFileExt(file_name):
    name_split = file_name.split(".")
    len_split = len(name_split)
    
    file_ext = name_split[len_split-1]
    return file_ext
    
def getFileNameNoExt(file_name, ext):
    return file_name[0: len(file_name) - len(ext)-1]

def _getFileNameNoExt(path):
    """Give file name witout extension, having only file path"""
    file_name = getFileName(path)
    ext = getFileExt(file_name)
    return file_name[0: len(file_name) - len(ext)-1]
    
def confirmRadius(a,b,c):
    if (len(radius_entry_var.get()) <=0):
        radius_entry_var.set("1")
    try:
        rad= float(radius_entry_var.get())
    except Exception:
        showwarning(title="Invalid input", message="Only integers allowed; 1 to 15")
        radius_entry_var.set("15")
        return
    if(rad < 2):
        radius_entry_var.set("1")
    if(rad > 15):
        radius_entry_var.set("15")

def blur(path):
    start_blur_btn.config(state=tk.DISABLED)
    if(path == "browse to select a file..."):
        showerror(title="Error", message="No image selected")
        start_blur_btn.config(state=tk.NORMAL)
        return
    path_split = path.split("/")
    save_dir = path_split[0:len(path_split)-1]
    save = ""
    for l in save_dir:
        save = save+l+"/";
    print("Save dir: "+ save)
    print("Blur Path: "+ path)
    file_name = getFileName(path)
    file_ext = getFileExt(file_name)
    file_name_no_ext = getFileNameNoExt(file_name, file_ext)
    print("File name: "+file_name)
    print("File ext: "+file_ext)
    print("File name,no ext: "+file_name_no_ext)
    if (len(path) <= 0 ):
        showerror(title="Error", message="No image selected")
    else:#Begin blur
        #get radius
        path_label_var.set("Blurring ["+file_name+"] ...")
        try:
            path_entry_var.set(path)
            blur_strength = float(radius_entry_var.get())
            img = Image.open(path)
            img_blurred = img.filter(ImageFilter.GaussianBlur(radius=blur_strength))
            img_blurred.save(save+"/"+file_name_no_ext+"_blurred."+file_ext)
            report_label.config(fg="#19c90e")
            #report_label.config(fg="#00FF00")
            report_label_var.set("DONE!")
            save_label_var.set("Saved at "+save+"/"+file_name_no_ext+"_blurred."+file_ext)
        except Exception as e:
            print e
            report_label.config(fg="#FF0000")
            report_label_var.set("Oops! Something went wrong...")
            showerror(title="Error", message=e)
            
        start_blur_btn.config(state=tk.NORMAL)

root = tk.Tk()
root.iconbitmap('favicon.ico')
root.focus_set()
root.bind("<Control-H>", lambda e:toolHelp())
root.bind("<Control-h>", lambda e:toolHelp())
#root.bind("<Control-o>", openAndBlur)
root.title("Blur Tool")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_percent, y_percent = 300.0/screen_width, 160.0/screen_height
root_w, root_h = x_percent * screen_width, y_percent * screen_height

posx = (screen_width/2)- (root_w/2)
posy = (screen_height/2)- (root_h/2)

print "root_w:",root_w," root_h:",root_h

root.geometry('%dx%d+%d+%d' %(root_w, root_h, posx, posy))
root.minsize(width=int(root_w), height=int(root_h))
#root.resizable(width=False, height=False)


browse_btn = tk.Button(master=root, text="Browse",
                       font=tkFont.Font(size=11), relief=tk.FLAT,
                       bg="#12adb9",fg="#ffffff",
                       activebackground ="#19c90e",activeforeground="#FFFFFF",
                       overrelief=tk.GROOVE,
                       cursor="hand2",
                       command=getPath)
browse_btn.grid(row=0, column=0, ipadx=10, padx=10,pady=5, sticky=tk.W)

path_entry_var = tk.StringVar()
path_entry_var.set("")
path_entry = tk.Entry(master=root, bd=2, textvariable=path_entry_var,
                      font=tkFont.Font(size=10), fg=color_black)
path_entry.grid(row=0, column=0, pady=5, ipadx=20,
                sticky=tk.W, padx=100, ipady=4)
path_entry.config(fg=color_gray)
path_entry_var.set("browse to select a file...")
path_entry.bind("<FocusIn>", lambda a:clearEntry())
path_entry.bind("<FocusOut>", lambda a:restoreEntry())

radius_label = tk.Label(master=root, text="Strength:", font=tkFont.Font(size=9))
radius_label.grid(row=1, column=0,sticky=tk.W, padx=10)

radius_entry_var = tk.StringVar()
radius_entry_var.set("2")
radius_entry = tk.Spinbox(master=root, bd=2, textvariable=radius_entry_var, from_=1, to=15)
radius_entry.grid(row=1, column=0, sticky=tk.W, padx=100, ipady=4)
radius_entry.update_idletasks()
radius_entry_var.trace('w', confirmRadius)

start_blur_btn = tk.Button(master=root, text="Blur",
                           bg="#12adb9",fg="#ffffff",
                           activebackground ="#19c90e",activeforeground="#FFFFFF",
                           overrelief=tk.GROOVE,
                           cursor="hand2",
                           font=tkFont.Font(size=11), relief=tk.FLAT,
                            command= lambda:blur(path_entry_var.get()))
start_blur_btn.grid(row=2, column=0, padx=10, ipadx=10, sticky=tk.W)

path_label_var = tk.StringVar()
path_label_var.set("waiting...")
path_label = tk.Label(master=root, textvariable=path_label_var,
                      font=tkFont.Font(size=9), fg="#0087d1")
path_label.grid(row=3, column=0, sticky=tk.W, padx=10)



report_label_var = tk.StringVar()
report_label_var.set("")
report_label = tk.Label(master=root, textvariable=report_label_var,
                        font=tkFont.Font(size=9, weight="bold"))
report_label.grid(row=4, column=0, sticky=tk.W, padx=10)

save_label_var = tk.StringVar()
save_label_var.set("")
save_label = tk.Label(master=root, textvariable=save_label_var,
                      anchor=tk.W, justify=tk.LEFT,fg="#19c90e",
                        font=tkFont.Font(size=9, weight="bold"))
save_label.grid(row=5, column=0, sticky=tk.W, padx=10)

menubar = tk.Menu(master=root)
file_menu = tk.Menu(menubar, tearoff=0)

menubar.add_cascade(label="File", menu=file_menu)

file_menu.add_command(label="Help  Ctrl+H", command=lambda :toolHelp())

root.config(menu=menubar)


root.mainloop()