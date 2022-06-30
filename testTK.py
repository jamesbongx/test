import time
#from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog as fd
from PIL import ImageTk, Image
top = tk.Tk()
top.title('Python Guides')
top.config(bg='#345')
window_width = 600
window_height= 800
screen_width = top.winfo_screenwidth()
screen_height = top.winfo_screenheight()
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)
#top.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
#top.resizable(False, False)
#top.attributes('-alpha', 0.5)
#top.attributes('-topmost', 1)
top.geometry("600x800")
style = ttk.Style(top)
style.configure('.', font=('Helvetica', 12))

'''
answer1 = simpledialog.askstring("Input", "What is your first name?", parent = top)
if answer1 is not None:
	print("Your first name is ", answer1)
else:
	print("You don't have a first name?")
answer1 = simpledialog.askinteger("Input", "What is your age?", parent=top, minvalue=0, maxvalue=100)
if answer1 is not None:
	print("Your age is ", answer1)
else:
	print("You don't have an age?")
answer1 = simpledialog.askfloat("Input", "What is your salary?", parent=top, minvalue=0.0, maxvalue=100000.0)
if answer1 is not None:
	print("Your salary is ", answer1)
else:
	print("You don't have a salary?")
'''
########################################	
def editSec():  
    print("Edit section")
def helpSec():  
    print("Help section")
menubar = Menu(top)  
file = Menu(menubar, tearoff=1)  
file.add_command(label="New")  
file.add_command(label="Edit")  
file.add_command(label="Save")  
file.add_command(label="Save as", command= top.destroy)     
file.add_separator()  
file.add_command(label="Exit", command= top.quit)  
menubar.add_cascade(label="File", menu=file)  
menubar.add_command(label="Edit", command=editSec) 
menubar.add_command(label="Help", command=helpSec)   
top.config(menu = menubar)
########################################	
pop_up = Menu(top, tearoff=0)
pop_up.add_command(label="pop_up")
pop_up.add_command(label="Edit1")
pop_up.add_separator()
pop_up.add_command(label="Save1", command= top.destroy) 
def menupopup(event): 
	try:
		pop_up.tk_popup(event.x_root, event.y_root, 0)
	finally:
		pop_up.grab_release()
top.bind("<Button-3>", menupopup)
########################################
def display_selected(choice):
	print(choice, valueOption.get())
options_list = ["Option 1", "Option 2", "Option 3", "Option 4"]	
valueOption = tk.StringVar()
valueOption.set("Option 1")
optMenu2 = tk.OptionMenu(top,valueOption, *options_list, command=display_selected)
optMenu2.place(x = 170, y = 5) 
########################################	
def updatePB(value):
	top.update_idletasks()
	pb['value'] = value
	time.sleep(1)
	LabelProgressBar['text']=pb['value'],'%'
LabelProgressBar = ttk.Label(top, text = '0%')
LabelProgressBar.place(x = 5, y = 5)  
pb = ttk.Progressbar(top, orient='horizontal', length=100, mode='determinate')	
pb.place(x = 50, y = 5)
########################################	
ValueEntry = tk.StringVar(top, value='updatePB')
def e3EnterK(name):
	print('e3EnterK', name, ValueEntry.get())
	updatePB(0)
	for i in range(5):
		updatePB(pb['value'] + 20)
txtE = ttk.Entry(top, textvariable = ValueEntry)
txtE.bind('<Return>', e3EnterK)
txtE.place(x = 5, y = 30) 
########################################	
listbox = tk.Listbox(top, width=10, height=5, selectmode='multiple')
for x in range(100):
	listbox.insert('end', str(x))
def items_selected(event):
	for i in listbox.curselection():
		print(listbox.get(i), end='')
	print()
listbox.bind('<<ListboxSelect>>', items_selected)
listbox.place(x = 5, y = 60)
########################################	
text_widget = tk.Text(top,width=20, height=3)
text_widget.insert('end', "Text Widgetn20 characters widen3 lines high")
text_widget.place(x = 80, y = 60)
print(text_widget.get('1.0','end')) 
########################################	
valueCombo = tk.StringVar()
def combo_changed(event):
	print(combo.get(),valueCombo.get())
vlist = ["combo1", "combo2", "combo3", "combo4"]
combo = ttk.Combobox(top, values = vlist, textvariable=valueCombo)
combo.set("Combobox")
combo.bind('<<ComboboxSelected>>', combo_changed)
combo.place(x = 80, y = 110)
########################################
frameImg=ttk.Frame(top)
frameImg.place(x = 5, y = 145)
canvas = tk.Canvas(frameImg,bg='white', width = 210,height = 210)
coordinates = 5, 5, 205, 205
arc = canvas.create_arc(coordinates, start=0, extent=250, fill="blue")
arc = canvas.create_arc(coordinates, start=250, extent=50, fill="red")
arc = canvas.create_arc(coordinates, start=300, extent=60, fill="yellow")
canvas.pack()
########################################
valueScale = tk.DoubleVar()
def slider_changed(event):
	print(slider.get(), valueScale.get(), '??')
frameScale = ttk.Frame(top)
frameScale.place(x = 220, y = 145)
slider = ttk.Scale(frameScale, from_=0, to=100, orient='vertical', command=slider_changed, variable=valueScale)
slider.pack(padx=5, pady=5)
sliderH = ttk.Scale(frameScale, from_=0, to=10, orient='horizontal')
sliderH.pack(padx=5, pady=5)
########################################
img = Image.open("test.bmp")
test = ImageTk.PhotoImage(img)
labelImg = ttk.Label(top, text="my label")
labelImg.grid(row=0, column=0, sticky="w")
labelImg.configure(image=test)
labelImg.place(x = 250, y = 90)
########################################
def value_changed():
	print(valueSpin.get())
valueSpin = tk.StringVar(value=0)
spin_box = ttk.Spinbox(top, from_=0, to=30, textvariable=valueSpin, command=value_changed)    	
spin_box.place(x = 360, y = 5)
########################################	
########################################	
def tstMsgBox():
	top.withdraw()		########
	messagebox.showinfo("Say Hello", "Hello World")
	messagebox.showinfo('information', 'Hi! You got a prompt.')
	messagebox.showerror('error', 'Something went wrong!')
	messagebox.showwarning('warning', 'accept T&C')
	print(messagebox.askquestion('Ask Question', 'Do you want to continue?'))
	print(messagebox.askokcancel('Ok Cancel', 'Are You sure?'))
	print(messagebox.askyesno('Yes|No', 'Do you want to proceed?'))
	print(messagebox.askretrycancel('retry', 'Failed! want to try again?'))
	print(fd.askopenfilename())
	exit(0)
butL = ttk.Button(top,text = "show messagebox",command = tstMsgBox)
butL.pack(side = 'left')
########################################	
valueCheckButton = tk.StringVar()
def closewin(tp):
	tp.destroy()		########
def checkBoxChg():
	print(valueCheckButton.get())
	tp= tk.Toplevel(top)	########
	tp.geometry("500x200")
	button1= ttk.Button(tp, text="ok", command=lambda:closewin(tp))
	button1.pack(pady=5, side= 'top')
cboxR = ttk.Checkbutton(top,text='Checkbutton',command=checkBoxChg,variable=valueCheckButton,onvalue='agree',offvalue='disagree')
cboxR.pack(side = 'right')
########################################	
valueRadioButton = tk.IntVar()
def radioChg():
	print(valueRadioButton.get())
frameRadioButton = ttk.LabelFrame(top, text='radioChg')
ttk.Radiobutton(frameRadioButton, text='Army', variable=valueRadioButton, value=1, command=radioChg).pack(anchor='w')
ttk.Radiobutton(frameRadioButton, text="Airforce", variable=valueRadioButton, value=2, command=radioChg).pack(anchor='w')
ttk.Radiobutton(frameRadioButton, text="Navy", variable=valueRadioButton, value=3, command=radioChg).pack(anchor='w')
frameRadioButton.pack(side = 'top')
########################################	
frameGrid = ttk.LabelFrame(top, text='bottom')
name = ttk.Label(frameGrid, text = "Name").grid(row = 0, column = 0, padx=10, pady=0) 
varE1 = tk.StringVar(frameGrid, value='not available')
e1 = ttk.Entry(frameGrid, textvariable=varE1, width= 5).grid(row = 0, column = 1)
password = ttk.Label(frameGrid, text = "Password").grid(row = 1, column = 0)  
e2 = ttk.Entry(frameGrid)
e2.insert('end', 'You email here')
e2.grid(row = 1, column = 1)
frameGrid.pack(side = 'bottom')

def testAfter():
	print('testAfter')
top.after(2000, testAfter)

top.mainloop()
