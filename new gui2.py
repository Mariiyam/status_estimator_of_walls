from tkinter import Tk, BOTH, W, E, N, S, messagebox
from tkinter.ttk import Frame, Button

from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT, RIGHT, BOTTOM
from tkinter.ttk import Frame, Label, Entry
from Boxcrop_Analyzer import  *
from Boxcrop import  *
from TheBrickModel import  *
from finalcomarison import  * #code with just function
#from last import * 
import os
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
import cv2



class Example(Frame):
    def __init__(self):
        super().__init__()

        self.initUI()


class GUI(Frame):
    def __init__(self):
        super().__init__()
        self._window_entries = []
        self.path = None
        self.wall1 = None
        self.wall2 = None
        self.initUI()
        

    def initUI(self):
        self.master.title("State Estimation of Wall")
        self.pack(fill=BOTH, expand=True)
        lbl1 = Label(self, text="Height", width=6).grid(row=0)

        self.height = Entry(self, width=10)
        self.height.grid(row=0, column=1)

        lbl2 = Label(self, text="Width", width=6).grid(row=0, column=6, sticky=E)


        self.width = Entry(self, width=10)
        self.width.grid(row=0, column=7)

        self.n_enry_lines = 0
        self.build = Button(self, text="Build model", command=self.build)
        self.build.grid(row=4 + self.n_enry_lines, column=6, sticky=E)

        self.selectimg = Button(self, text="insert img", command=self.select) 
        self.selectimg.grid(row=3 + self.n_enry_lines, column=3, sticky=E)

        self.imageanalyzer = Button(self, text="wall analyzer", command=self.img_analyzer) 
        self.imageanalyzer.grid(row=3 + self.n_enry_lines, column=6, sticky=E)

        self.img_model = Button(self, text="Build Image model", command=self.create_img_model) 
        self.img_model.grid(row=3 + self.n_enry_lines, column=7, sticky=E)

        self.comp = Button(self, text="Compare", command=self.compare) 
        self.comp.grid(row=4+ self.n_enry_lines, column=7, sticky=E)


    def img_analyzer(self):
        img_analyzor2(self.path)


    def compare(self):
       z= status_comparison(self.wall1, self.wall2)
       print(z)
        
    def create_img_model(self): # shows only the 3D of the image wall
        self.wall2 = img_analyzor(self.path)

        draw3Dwall(self.wall2)
        

    def add_entry_line(self):
        self.n_enry_lines += 1
        self.add_window.grid_forget()
        self.build.grid_forget()


        lbl1 = Label(self, text="X").grid(row=self.n_enry_lines, column=0)
        lbl2 = Label(self, text="Y").grid(row=self.n_enry_lines, column=2)
        lbl2 = Label(self, text="Height").grid(row=self.n_enry_lines, column=4)
        lbl2 = Label(self, text="Width").grid(row=self.n_enry_lines, column=6)

        x = Entry(self, width=10)
        x.grid(row=self.n_enry_lines, column=1)
        y = Entry(self, width=10)
        y.grid(row=self.n_enry_lines, column=3)
        height = Entry(self, width=10)
        height.grid(row=self.n_enry_lines, column=5)
        width = Entry(self, width=10)
        width.grid(row=self.n_enry_lines, column=7)

        self._window_entries.append(([x,y,height,width]))
        self.add_window.grid(row=2 + self.n_enry_lines, column=7)
        self.build.grid(row=3 + self.n_enry_lines, column=7, sticky=E)
        

    def select(self):
        #select_action()
        self.path =  filedialog.askopenfilename(title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        print (self.path)
        
    def analyzeraction(self): # shows the original image and the image with boxes
      #img = select_action()
      img_analyzor2(self.path)
        # Do something with results here.
      
       
    def build(self):    # shows the 3D of the numerical wall
        results = {}
        height = self.height.get()
        width = self.width.get()

        try:
            height = abs(float(height))
            width = abs(float(width))
        except:
            messagebox.showerror("Error", "All inputs must be integers and must not be empty")
            return
        results["height"] = height
        results["width"] = width

        results["windows"] = []
        for entry in self._window_entries:
            values = map(lambda x: x.get(), entry)
            try:
                values = tuple(map(int ,values))
            except:
                messagebox.showerror("Error", "All inputs must be integers and must not be empty")
                return
            results["windows"].append(values)

        # Do something with results here (note that this inside for loop).
       # wall = Wall (Bricks=bricks)
        self.wall1= Wall(hight=results["height"],width=results["width"])#from result(numerical data),result must presented here
        draw3Dwall(self.wall1)
       # z=status_comparison(a,t)
       # print ((z),'new')
       
        
 

if __name__ == '__main__':
    root = Tk()
    ex = GUI()
    root.mainloop()
