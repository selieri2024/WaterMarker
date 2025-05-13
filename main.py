import tkinter
from tkinter import *
from tkinter.filedialog import askopenfiles, askopenfile
import tkinter.messagebox
from PIL import Image, ImageTk
import os
from tkinter.ttk import Combobox
import cv2
import numpy as np

if not os.path.exists(os.path.join(os.getcwd(),'watermarks')):
    os.makedirs(os.path.join(os.getcwd(),'watermarks'))

root = Tk()
root.geometry('365x195')

watermark_names = None

def error_solver(self, *args):
    if str(args[1]) == "PRIMARY selection doesn't"+' exist or form "STRING" not defined':
        tkinter.messagebox.askokcancel('No mark choosed', 'Please select watermark')
    elif str(args[1]) == "'NoneType' object has no attribute 'convert'":
        tkinter.messagebox.askokcancel('Image is too small', 'The selected image is too small')
    else:
        print(self)
        print(args)
        tkinter.messagebox.askokcancel('Unknown error', 'Unknown tkinter error')

tkinter.Tk.report_callback_exception = error_solver

watermarks_frame = Frame(root)
watermarks_frame.grid(column=1,row=0,padx=10,pady=1,sticky='nw')

choose_watermark = Combobox(watermarks_frame,values=watermark_names)
choose_watermark.pack(pady=5)

def update(self=None):
    global watermark_names
    watermark_names = os.listdir(os.path.join(os.getcwd(),'watermarks'))
    watermark_names.remove('.DS_Store')
    choose_watermark.configure(values=watermark_names)
    try:
        default_canvas_image = Image.open(os.path.join(os.getcwd(),'watermarks',choose_watermark.selection_get()))
        default_canvas_image = default_canvas_image.resize((round(100),round(default_canvas_image.size[1]/default_canvas_image.size[0]*100)))
        default_canvas_2 = ImageTk.PhotoImage(default_canvas_image)
        watermark_canvas.configure(image=default_canvas_2)
        watermark_canvas.image = default_canvas_2
    except Exception as e:
        print(e)

def place_watermark(watermark,image):
    if image.size[0] >= watermark.size[0] and image.size[1] >= watermark.size[1]:
        watermark = watermark.resize((round(image.size[0]/3),round(watermark.size[1]/watermark.size[0]*image.size[0]/3)))
        image.paste(watermark, (image.size[0]-1-watermark.size[0],image.size[1]-1-watermark.size[1]), mask=watermark)
        return image

def choose_photo_func():
    watermark_name = choose_watermark.selection_get()
    files = askopenfiles()
    for image in files:
        img = Image.open(image.name)
        img.putalpha(255)
        watermark = Image.open(os.path.join(os.getcwd(),'watermarks',watermark_name)).convert(img.mode)
        watermarked = place_watermark(watermark,img).convert('RGB')
        watermarked.save(image.name)
    update()
    tkinter.messagebox.askokcancel('Success', 'Watermarks successfully placed')s

update()
try:
    default_canvas = Image.open(os.path.join(os.getcwd(),'watermarks',watermark_names[0]))
    choose_watermark.set(watermark_names[0])
    default_canvas = ImageTk.PhotoImage(default_canvas.resize((round(100),round(default_canvas.size[1]/default_canvas.size[0]*100))))

    watermark_canvas = Label(root, image=default_canvas)
    watermark_canvas.grid(column=0,row=0,padx=10,pady=10)
except IndexError:
    watermark_canvas = Label(root)
    watermark_canvas.grid(column=0,row=0,padx=10,pady=10)
    tkinter.messagebox.askokcancel('No watermark added', 'Please add at least one watermark')

choose_photo_btn = Button(root,text='Выбрать',command=choose_photo_func)
choose_photo_btn.grid(column=0,row=1,padx=10,pady=10,sticky='e')

def add_watermark():
    if not os.path.exists(os.path.join(os.getcwd(),'watermarks')):
        os.makedirs(os.path.join(os.getcwd(),'watermarks'))
    file = askopenfile()
    try:
        img = cv2.imread(file.name,cv2.IMREAD_GRAYSCALE)
        cv2.imwrite(os.path.join(os.getcwd(),'watermarks',file.name.split('/')[-1]),img)s
        update(file.name)
    except Exception as e:
        print(e)
        

add_watermark_btn = Button(watermarks_frame,text='Добавить водяной знак',command=add_watermark)
add_watermark_btn.pack(pady=5,anchor='n')


choose_watermark.bind('<<ComboboxSelected>>', update)

root.mainloop()
