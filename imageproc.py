from tkinter import *
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy import ndimage
from PIL import ImageOps,Image


class Window(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master=master
        self.initial_image_proc()
             
    def initial_image_proc(self):
        self.master.title("Image Processing Library")
        self.pack(expand=1,fill=BOTH)
        self.create_widgets()
                
    def create_widgets(self):
        self.browse=Button(self)
        self.browse["text"]="Browse Image"
        self.browse["command"]=self.load_image
        self.browse.grid(row=0,column=0)
        
        self.rotateLeft=Button(self)
        self.rotateLeft["text"]="Rotate Left"
        self.rotateLeft["command"]=self.rotate_left
        self.rotateLeft.grid(row=1,column=1)
        
        self.rotateRight=Button(self)
        self.rotateRight["text"]="Rotate Right"
        self.rotateRight["command"]=self.rotate_right
        self.rotateRight.grid(row=1,column=2)
        
        self.rotateLeft10=Button(self)
        self.rotateLeft10["text"]="Rotate -10°"
        self.rotateLeft10["command"]=self.rotatemin_10
        self.rotateLeft10.grid(row=1,column=3)
        
        self.rotateRight10=Button(self)
        self.rotateRight10["text"]="Rotate +10°"
        self.rotateRight10["command"]=self.rotateplus_10
        self.rotateRight10.grid(row=1,column=4)


        self.uniFilter=Button(self)
        self.uniFilter["text"]="Uniform Filter"
        self.uniFilter["command"]=self.unifilter
        self.uniFilter.grid(row=1,column=5)
        
        self.uniFilter1d=Button(self)
        self.uniFilter1d["text"]="Uniform Filter1D"
        self.uniFilter1d["command"]=self.unifilter1d
        self.uniFilter1d.grid(row=1,column=2)

        
        self.gausFilter=Button(self)
        self.gausFilter["text"]="Gaussian Filter"
        self.gausFilter["command"]=self.gausfilter
        self.gausFilter.grid(row=0,column=2)
        
        self.gausFilter1d=Button(self)
        self.gausFilter1d["text"]="Gaussian Filter1D"
        self.gausFilter1d["command"]=self.gausfilter1d
        self.gausFilter1d.grid(row=0,column=3)
        
        self.gausFiltergrad=Button(self)
        self.gausFiltergrad["text"]="Gaussian Gradient Magnitude"
        self.gausFiltergrad["command"]=self.gausgrad
        self.gausFiltergrad.grid(row=0,column=4)


        self.min=Button(self)
        self.min["text"]="Minimum"
        self.min["command"]=self.min_val
        self.min.grid(row=0,column=7)  
        
        self.reset=Button(self)
        self.reset["text"]="Reset"
        self.reset["command"]=self.reset_imag
        self.reset.grid(row=0,column=1)  

        
        self.sigmaval=Entry(self)
        self.sigmaval.grid()
        self.sigmaval.grid(row=1,column=0)
        self.sigmaval.focus()
        
        self.interpol=Button(self)
        self.interpol["text"]="interpolation"
        self.interpol["command"]=""
        self.interpol.grid(row=2,column=0)
        
        self.affineTrans=Button(self)
        self.affineTrans["text"]="Affine Transform"
        self.affineTrans["command"]=self.affineTransform
        self.affineTrans.grid(row=2,column=1)        
        

    canvas=''
    
    def load_image(self):
        filename=filedialog.askopenfilename(filetype=( ("image files","*.png;*.jpg"),("All files","*.*")) ) 
        self.image=plt.imread(filename)
        self.imgreset=self.image
        fig=plt.figure(figsize=(5,5))
        if self.canvas=='':
            self.im=plt.imshow(self.image)
            self.canvas=FigureCanvasTkAgg(fig,master=root)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(side=TOP,fill=BOTH,expand=1)
        else:
            self.im.set_data(self.image)
            self.canvas.draw()
        
    theta=0
    
    #rotate
   
    def rotate_left(self):
        self.theta+=90
        rotated= ndimage.rotate(self.image,self.theta)
        self.im.set_data(rotated)
        self.canvas.draw()
    
    def rotate_right(self):
        self.theta-=90
        rotated=ndimage.rotate(self.image,self.theta)
        self.im.set_data(rotated)
        self.canvas.draw()  
    
    def rotateplus_10(self):
        self.theta+=10
        rotated=ndimage.rotate(self.image,self.theta)
        self.im.set_data(rotated)
        self.canvas.draw()  

        
    def rotatemin_10(self):
        self.theta-=10
        rotated=ndimage.rotate(self.image,self.theta)
        self.im.set_data(rotated)
        self.canvas.draw()  
        
    #filters
    
    def unifilter(self):
        self.image=ndimage.uniform_filter(self.image,size=int(self.sigmaval.get()))
        self.im.set_data(self.image)
        self.canvas.draw()
        
    def unifilter1d(self):
        self.image=ndimage.uniform_filter1d(self.image,size=int(self.sigmaval.get()))
        self.im.set_data(self.image)
        self.canvas.draw()
        
    def gausfilter(self):
        self.image=ndimage.gaussian_filter(self.image,sigma=int(self.sigmaval.get()))
        self.im.set_data(self.image)
        self.canvas.draw()
        
    def gausfilter1d(self):
        self.image=ndimage.gaussian_filter1d(self.image,sigma=int(self.sigmaval.get()))
        self.im.set_data(self.image)
        self.canvas.draw()
        
    def gausgrad(self):
        self.image=ndimage.gaussian_gradient_magnitude(self.image,sigma=int(self.sigmaval.get()))
        self.im.set_data(self.image)
        self.canvas.draw()
        

    def min_val(self):
        self.sigmaval.delete(0,END)
        self.sigmaval.insert(0,ndimage.minimum(self.image))

    #interpolation
        
    def affineTransform(self):
        a=15.0*pi/180.0
       # rot=array([[cos(a),sin(a)],[-sin(a),cos(a)]])
        self.image=ndimage.affine_transform(self.image)
        self.im.set_data(self.image)
        self.canvas.draw()


    def reset_imag(self):
        self.im.set_data(self.imgreset)
        self.canvas.draw()



root = Tk()

root.geometry("1024x600")

app = Window(root)     
         
root.mainloop()

