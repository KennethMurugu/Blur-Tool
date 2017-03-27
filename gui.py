# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 15:38:11 2017

@author: Kenneth
"""

import Tkinter as tk
import tkFont
import tkFileDialog as tfd
#import fileops as f_ops
from tkMessageBox import showerror, showwarning, showinfo
from blur import BlurImage


class MainWindow():
    """Class holding all GUI elements for the Blur Tool"""
    
    color_gray = "#BBB"
    color_black = "#000"
    path_entry_default = "browse to select a file..."
    
    VERSION =  "1.0.1.1"
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.iconbitmap('favicon.ico')
        self.root.focus_set()
        self.root.bind("<Control-H>", lambda e:self.toolHelp())
        self.root.bind("<Control-h>", lambda e:self.toolHelp())
        
        self.root.title("Blur Tool "+self.VERSION)
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.x_percent, self.y_percent = 300.0/self.screen_width, 160.0/self.screen_height
        self.root_w, self.root_h = self.x_percent * self.screen_width, self.y_percent * self.screen_height
        
        self.posx = (self.screen_width/2)- (self.root_w/2)
        self.posy = (self.screen_height/2)- (self.root_h/2)
        
        print "root_w:",self.root_w," root_h:",self.root_h
        
        self.root.geometry('%dx%d+%d+%d' %(self.root_w, self.root_h, self.posx, self.posy))
        self.root.minsize(width=int(self.root_w), height=int(self.root_h))
        self.root.resizable(width=False, height=False)
        
        #Opens up file dialog to choose file
        self.browse_btn = tk.Button(master=self.root, text="Browse",
                               font=tkFont.Font(size=11), relief=tk.FLAT,
                               bg="#12adb9",fg="#ffffff",
                               activebackground ="#19c90e",activeforeground="#FFFFFF",
                               overrelief=tk.RIDGE,
                               cursor="hand2",
                               command=self.getPath)
        self.browse_btn.grid(row=0, column=0, ipadx=10, padx=10,pady=5, sticky=tk.W)
        
        #Entry field for image path/Alternate to Browse
        self.path_entry_var = tk.StringVar()
        self.path_entry_var.set("")
        self.path_entry = tk.Entry(master=self.root, bd=2, textvariable=self.path_entry_var,
                              font=tkFont.Font(size=10), fg=self.color_black)
        self.path_entry.grid(row=0, column=0, pady=5, ipadx=20,
                        sticky=tk.W, padx=100, ipady=4)
        self.path_entry.config(fg=self.color_gray)
        self.path_entry_var.set(self.path_entry_default)
        #Updating entry field when text is entered
        self.path_entry.bind("<FocusIn>", lambda a:self.clearEntry())
        self.path_entry.bind("<FocusOut>", lambda a:self.restoreEntry())
        
        self.radius_label = tk.Label(master=self.root, text="Strength:", font=tkFont.Font(size=10))
        self.radius_label.grid(row=1, column=0,sticky=tk.W, padx=10)
        
        #Spinbox to xhoose blur strength
        self.radius_spinbox_var = tk.StringVar()
        self.radius_spinbox_var.set("2")
        self.radius_spinbox = tk.Spinbox(master=self.root, bd=2, textvariable=self.radius_spinbox_var, from_=1, to=15)
        self.radius_spinbox.grid(row=1, column=0, sticky=tk.W, padx=100, ipady=4)
        self.radius_spinbox.update_idletasks()
        self.radius_spinbox_var.trace('w', self.confirmRadius)
        
        self.start_blur_btn = tk.Button(master=self.root, text="Blur",
                                   bg="#12adb9",fg="#ffffff",
                                   activebackground ="#19c90e",activeforeground="#FFFFFF",
                                   overrelief=tk.RIDGE,
                                   cursor="hand2",
                                   font=tkFont.Font(size=11), relief=tk.FLAT,
                                   command = lambda:self.blur(self.path_entry_var.get()))
        self.start_blur_btn.grid(row=2, column=0, padx=10, ipadx=10, sticky=tk.W)
        
        #Shows image name of selected image
        self.path_label_var = tk.StringVar()
        self.path_label_var.set("waiting...")
        self.path_label = tk.Label(master=self.root, textvariable=self.path_label_var,
                              font=tkFont.Font(size=9), fg="#0087d1")
        self.path_label.grid(row=3, column=0, sticky=tk.W, padx=10)
        
        
        #Shows if blur is successful or not
        self.report_label_var = tk.StringVar()
        self.report_label_var.set("")
        self.report_label = tk.Label(master=self.root, textvariable=self.report_label_var,
                                font=tkFont.Font(size=10, weight="bold"))
        self.report_label.grid(row=4, column=0, sticky=tk.W, padx=10)
        
        #Shows path of saved image
        #TODO: REMOVE, transfer to dialog
        self.save_label_var = tk.StringVar()
        self.save_label_var.set("")
        self.save_label = tk.Label(master=self.root, textvariable=self.save_label_var,
                              anchor=tk.W, justify=tk.LEFT,fg="#19c90e",
                              font=tkFont.Font(size=9, weight="bold"))
        self.save_label.grid(row=5, column=0, sticky=tk.W, padx=10)
        
        #Menu optins for help
        self.menubar = tk.Menu(master=self.root)
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Help  Ctrl+H", command=lambda :self.toolHelp())
        self.root.config(menu=self.menubar)
        
        
        self.root.mainloop()
        
    def blur(self, path):
        self.start_blur_btn.config(state=tk.DISABLED)
        if(path == self.path_entry_default):
            showerror(title="Error", message="No image selected")
            self.start_blur_btn.config(state=tk.NORMAL)
            return
        path_split = path.split("/")
        save_dir = path_split[0:len(path_split) - 1]
        save = ""
        for l in save_dir:
            save = save+l+"/";
        print("Save dir: "+ save)
        print("Blur Path: "+ path)
        
        file_name = self.getFileName(path)
        file_ext = self.getFileExt(file_name)
        file_name_no_ext = self.getFileNameNoExt(file_name, file_ext)
        
        print("File name: "+file_name)
        print("File name,no ext: "+file_name_no_ext)
        print("File ext: "+file_ext)
        
        if (len(path) <= 0 ):
            showerror(title="Error", message="No image selected")
        else:#Begin blur
            #get radius
            self.path_label_var.set("Blurring ["+file_name+"] ...")
            try:
                self.path_entry_var.set(path)
                blur_strength = float(self.radius_spinbox_var.get())
                #img = Image.open(path)
                #img_blurred = img.filter(ImageFilter.GaussianBlur(radius=blur_strength))
                blur_instance = BlurImage(path, blur_strength)
                img_blurred = blur_instance.blur()
                img_blurred.save(save+"/"+file_name_no_ext+"_blurred."+file_ext)
                self.report_label.config(fg="#19c90e")
                #report_label.config(fg="#00FF00")
                self.report_label_var.set("DONE!")
                #save_label_var.set("Saved at "+save+"/"+file_name_no_ext+"_blurred."+file_ext)
                showinfo(title="DONE", message="Image saved at:\n "+save+"/"+file_name_no_ext+"_blurred."+file_ext)
            except Exception as e:
                print e
                self.report_label.config(fg="#FF0000")
                self.report_label_var.set("Oops! Something went wrong...")
                showerror(title="Error", message="Something went wrong during the blur. Here's the error:\n"+e)
                
            self.start_blur_btn.config(state=tk.NORMAL)    
    
    def toolHelp(self):
        showinfo(title="Help", message="1) Browse and select your image.\n"
                                    +"2) Choose a blur strength and press 'Blur'\n"
                                    +"3) Done! ^_^\n"
                                    +"Note: Image will be saved with '_blurred' attached to the name; e.g image_blurred.jpg")
                                    
    def clearEntry(self):
        if(self.path_entry_var.get() == self.path_entry_default):
            self.path_entry.config(fg=self.color_black)
            self.path_entry_var.set("")
    def restoreEntry(self):
        if(self.path_entry_var.get() == ""):
            self.path_entry.config(fg=self.color_gray)
            self.path_entry_var.set(self.path_entry_default)
    def entryUpdate(self,a,b,c):
        self.path_entry.config(fg=self.color_black)
        
    def getPath(self):
        #Get path of selected image
        self.path_label_var.set("waiting")
        self.report_label_var.set("")
        self.save_label_var.set("")
        self.path_entry.config(fg=self.color_gray)
        self.path_entry_var.set(self.path_entry_default)
        file_options = {'initialdir':'/',
                                      'title':'Choose file(s) to load',
                                      'filetypes':[('JPEG','*.jpg *.jpeg'),
                                                   ('Bitmap Image','*.bmp'),
                                                   ('PNG Image','*.png')]}
        file_path = tfd.askopenfilename(parent=self.root, **file_options)
        if(len(file_path) > 0):
            self.path_entry.config(fg=self.color_black)
            self.path_entry_var.set(file_path)
            self.path_label_var.set("Selected: ["+self.getFileName(file_path)+"]")
    
    def getFileName(self,path):
        filestring_split = path.split('/')
        len_split = len(filestring_split)
        
        filename = filestring_split[len_split-1]
        return filename
    
    def getFileExt(self,file_name):
        name_split = file_name.split(".")
        len_split = len(name_split)
        
        file_ext = name_split[len_split-1]
        return file_ext
        
    def getFileNameNoExt(self,file_name, ext):
        return file_name[0: len(file_name) - len(ext)-1]
    
    def _getFileNameNoExt(self,path):
        """Give file name witout extension, having only file path"""
        file_name = self.getFileName(path)
        ext = self.getFileExt(file_name)
        return file_name[0: len(file_name) - len(ext)-1]
    
    def confirmRadius(self,a,b,c):
        """ Makes sure radius is an integer, and in range [1,15]"""
        if (len(self.radius_spinbox_var.get()) <=0):
            self.radius_spinbox_var.set("1")
        try:
            rad= float(self.radius_spinbox_var.get())
        except Exception:
            showwarning(title="Invalid input", message="Only integers allowed; 1 to 15")
            self.radius_spinbox_var.set("15")
            return
        if(rad < 2):
            self.radius_spinbox_var.set("1")
        if(rad > 15):
            self.radius_spinbox_var.set("15")    
