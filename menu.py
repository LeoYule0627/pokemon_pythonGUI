import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import *
from information import new

root = tk.Tk()
root.title("Menu")
root.geometry('700x500')
root.option_add("*tearOff", False) # This is always a good idea

conn = sqlite3.connect('pokedex.db')
conn.commit()

# search
def search():
    treeview.selection()
    fetchdata = treeview.get_children()
    for f in fetchdata:
        treeview.delete(f)
    try:
        conn = sqlite3.connect('pokedex.db')
        core = conn.cursor()
        if combobox.get()=="編號ID":
            db = 'select * from pokemon where id '
        elif combobox.get()=="英文名稱":
            db = 'select * from pokemon where en '
        else :
            db = 'select * from pokemon where ch '
        name = entry.get()
        data = core.execute(db + "like '%" + name + "%'")
        for d in data:
            treeview.insert('', END, values=d) 
    except Exception as e:
        showerror("issue", e)
    print("Search_Name:"+name)
    entry.delete(0,'end')

def show():
    entry.delete(0,'end')
    treeview.selection()
    cursor = conn.cursor()
    fetchdata = treeview.get_children()       
    for elements in fetchdata:
        treeview.delete(elements)
    rows=cursor.execute("select * from pokemon order by 'id' Asc")
    for row in rows:
        treeview.insert('', 'end', values=row)
    print("home")

# Make the app responsive
root.columnconfigure(index=0, weight=1)
root.columnconfigure(index=1, weight=1)
root.columnconfigure(index=2, weight=1)
root.columnconfigure(index=3, weight=1)
root.columnconfigure(index=4, weight=1)
root.rowconfigure(index=0, weight=1)
root.rowconfigure(index=1, weight=1)

# Create a style
style = ttk.Style(root)

root.tk.call("source", "dark.tcl")
root.tk.call("source", "light.tcl")
style.theme_use("dark")
root.configure(background='#313131')
style.configure("mystyle.Treeview", font=('Times', 20),rowheight=40)
style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold'))   

theme=True
def change_mode():
    global theme
    if theme:
        theme=False
        style.theme_use("light")
        root.configure(background='white')
        style.configure("mystyle.Treeview", font=('Times', 20),rowheight=40)
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold'))   
    else:
        theme=True
        style.theme_use("dark")
        root.configure(background='#313131')
        
# Create lists for the Combobox
combo_list = ["編號ID", "英文名稱", "中文名稱"]

# Create a Frame 
widgets_frame = ttk.Frame(root)
widgets_frame.pack(side="top",padx=5, pady=5)
widgets_frame.columnconfigure(index=0, weight=1)

home = ttk.Button(widgets_frame, text='Home', command=show)
home.grid(row=0, column=0, padx=5, pady=5)

#combobox
combobox = ttk.Combobox(widgets_frame, width=8, state="readonly", values=combo_list)
combobox.current(0)
combobox.grid(row=0, column=1, padx=5, pady=5)

# Entry
entry = ttk.Entry(widgets_frame)
entry.grid(row=0, column=2, padx=5, pady=5)

# Button
search= ttk.Button(widgets_frame, text='Search', command=search)
search.grid(row=0, column=3, padx=5, pady=5)

# Switch
switch = ttk.Checkbutton(widgets_frame, text="Mode", style="Switch", command=change_mode)
switch.grid(row=0, column=4, padx=5, pady=5)

# Panedwindow
paned = ttk.PanedWindow(root)
paned.pack(side="top",expand=True, fill="both", padx=5)

# Pane #1
pane_1 = ttk.Frame(root)
paned.add(pane_1, weight=1)

# Create a Frame for the Treeview
treeFrame = ttk.Frame(pane_1)
treeFrame.pack(side="top",expand=True, fill="both", padx=5)

# Scrollbar
treeScroll = ttk.Scrollbar(treeFrame)
treeScroll.pack(side="right", fill="y")

# Treeview
treeview = ttk.Treeview(treeFrame, selectmode="extended", yscrollcommand=treeScroll.set, column=("c1", "c2", "c3"),show='headings',height=10,style="mystyle.Treeview")
treeview.pack(side="top",expand=True, fill="both")
treeScroll.config(command=treeview.yview)

# Treeview columns
# Treeview headings
treeview.column("# 1", anchor=CENTER,width=80)
treeview.heading("# 1", text="ID")
treeview.column("# 2", anchor=CENTER)
treeview.heading("# 2", text="英文名稱")
treeview.column("# 3", anchor=CENTER)
treeview.heading("# 3", text="中文名稱")

# selected
def select(event):
    for item in treeview.selection():
        item_text = treeview.item(item,"values")
        new(item_text).pokemon()
treeview.bind("<ButtonRelease-1>", select)

# Center the window, and set minsize
root.update()
root.minsize(root.winfo_width(), root.winfo_height())
x_cordinate = int((root.winfo_screenwidth()/2) - (root.winfo_width()/2))
y_cordinate = int((root.winfo_screenheight()/2) - (root.winfo_height()/2))
root.geometry("+{}+{}".format(x_cordinate-500, y_cordinate-200))

# Start the main loop
show()
root.mainloop()
conn.close()