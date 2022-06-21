import tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
from getPokeInfo import getBasicInfo,getBiology
from pokeImage import getImgIdEnCh
from rader import rader_main

def ui(item):
    window = tk.Toplevel()
    window.title("Pokemon")       
    window.geometry('1450x800')
    
    paned = ttk.PanedWindow(window)
    paned.pack(side='top', fill="both")
    
    pane_1 = ttk.Frame(paned)
    paned.add(pane_1, weight=0)
    
     # Create a Frame for the ID and NANE
    id_frame = ttk.LabelFrame(pane_1,text="pokemon")
    id_frame.pack(side="top", fill="x",padx=5)

    id_text = ttk.Label(id_frame,text="#"+item[0],font=('Times', 20),justify='center')
    id_text.pack(side="left",expand=True, fill="both",padx=40)
    
    en_text = ttk.Label(id_frame,text=item[1],font=('Times', 20),justify='center')
    en_text.pack(side="left",expand=True, fill="both")

    ch_text = ttk.Label(id_frame,text=item[2],font=('Times', 20),justify='center')
    ch_text.pack(side="left",expand=True, fill="both")

    paned = ttk.PanedWindow(window)
    paned.pack(side='top',expand=True, fill="both")
    
    pane_2 = ttk.Frame(paned)
    pane_2.pack(expand=True,fill='x')
    paned.add(pane_2, weight=0)

    image_frame = ttk.LabelFrame(pane_2,text="pokemon")
    image_frame.pack(side="left")
    
    pokemon_photo = ImageTk.PhotoImage(Image.open('image\poke_image\Pokemon_'+item[1]+'.png').resize((300,300), Image.ANTIALIAS))
    image1 = ttk.Label(image_frame, image=pokemon_photo)
    image1.pack(fill="both",padx=10,pady=10)
    
    Cloud_photo = ImageTk.PhotoImage(Image.open('image\img\Cloud_'+item[1]+'.png').resize((300,300), Image.ANTIALIAS))
    image2 = ttk.Label(image_frame, image=Cloud_photo)
    image2.pack(fill="both")
    
    # Notebook
    notebook = ttk.Notebook(pane_2)
    
    # Tab #1
    tab_1 = ttk.Frame(notebook)
    notebook.add(tab_1, text="文字敘述")
    
    text99_frame = ttk.Frame(tab_1)
    text99_frame.pack(side="left")
    text99=getBiology(item[2])
    text = ttk.Label(text99_frame,text=text99,font=('Times', 15),wraplength=1100,justify = 'left')
    text.pack(side="top")

    tab_3 = ttk.Frame(notebook)
    notebook.add(tab_3, text="內容")
    
    info=getBasicInfo(item[2])
    
    info_frame= ttk.Frame(tab_3)
    info_frame.pack(side="top",fill="x",pady=20)
    
    type_frame = ttk.LabelFrame(info_frame,text="屬性")
    type_frame.pack(side="left",padx=20)
    type_text = ttk.Label(type_frame,text=info[0],font=('Times', 20),justify='center')
    type_text.pack(side="left",expand=True,padx=20)
    
    category_frame = ttk.LabelFrame(info_frame,text="分類")
    category_frame.pack(side="left",padx=20)
    category_text = ttk.Label(category_frame,text=info[1],font=('Times', 20),justify='center')
    category_text.pack(side="left",expand=True,padx=20)
    
    abilities_frame = ttk.LabelFrame(info_frame,text="特性")
    abilities_frame.pack(side="left",padx=20)
    abilities_text = ttk.Label(abilities_frame,text=info[2],font=('Times', 20),justify='center')
    abilities_text.pack(side="left",expand=True, fill="both",padx=20)
    
    if info[3]!=[]:
        hiddenAbilities_frame = ttk.LabelFrame(info_frame,text="隱藏特性")
        hiddenAbilities_frame.pack(side="left",padx=20)
        hiddenAbilities_text = ttk.Label(hiddenAbilities_frame,text=info[3],font=('Times', 20),justify='center')
        hiddenAbilities_text.pack(side="left",expand=True, fill="both",padx=20)
    
    height_frame = ttk.LabelFrame(info_frame,text="身高")
    height_frame.pack(side="left",padx=20)
    height_text = ttk.Label(height_frame,text=info[5],font=('Times', 20),justify='center')
    height_text.pack(side="left",expand=True, fill="both",padx=20)
    
    weight_frame = ttk.LabelFrame(info_frame,text="體重")
    weight_frame.pack(side="left",padx=20)
    weight_text = ttk.Label(weight_frame,text=info[6],font=('Times', 20),justify='center')
    weight_text.pack(side="left",expand=True, fill="both",padx=20)
    
    
    info2_frame= ttk.Frame(tab_3)
    info2_frame.pack(side="top",fill="x",pady=20)
    rader_text=rader_main(item[1],item[2])
    
    hp_frame = ttk.LabelFrame(info2_frame,text="HP")
    hp_frame.pack(side="left",padx=20)
    hp_text = ttk.Label(hp_frame,text=rader_text[0],font=('Times', 20),justify='center')
    hp_text.pack(side="left",expand=True, fill="both",padx=20)
    
    att_frame = ttk.LabelFrame(info2_frame,text="攻擊")
    att_frame.pack(side="left",padx=20)
    att_text = ttk.Label(att_frame,text=rader_text[1],font=('Times', 20),justify='center')
    att_text.pack(side="left",expand=True, fill="both",padx=20)
    
    def_frame = ttk.LabelFrame(info2_frame,text="防禦")
    def_frame.pack(side="left",padx=20)
    def_text = ttk.Label(def_frame,text=rader_text[2],font=('Times', 20),justify='center')
    def_text.pack(side="left",expand=True, fill="both",padx=20)
    
    speed_frame = ttk.LabelFrame(info2_frame,text="速度")
    speed_frame.pack(side="left",padx=20)
    speed_text = ttk.Label(speed_frame,text=rader_text[3],font=('Times', 20),justify='center')
    speed_text.pack(side="left",expand=True, fill="both",padx=20)
    
    sp_atk_frame = ttk.LabelFrame(info2_frame,text="特攻")
    sp_atk_frame.pack(side="left",padx=20)
    sp_atk_text = ttk.Label(sp_atk_frame,text=rader_text[5],font=('Times', 20),justify='center')
    sp_atk_text.pack(side="left",expand=True, fill="both",padx=20)
    
    sp_def_frame = ttk.LabelFrame(info2_frame,text="特防")
    sp_def_frame.pack(side="left",padx=20)
    sp_def_text = ttk.Label(sp_def_frame,text=rader_text[4],font=('Times', 20),justify='center')
    sp_def_text.pack(side="left",expand=True, fill="both",padx=20)
    
    info3_frame= ttk.Frame(tab_3)
    info3_frame.pack(side="top",fill="x",pady=20)
    
    Rader_photo = ImageTk.PhotoImage(Image.open('image\img\Rader_'+item[1]+'.png'))
    image3 = ttk.Label(info3_frame, image=Rader_photo)
    image3.pack(side="left")
    
    Bar_photo = ImageTk.PhotoImage(Image.open('image\img\Bar_'+item[1]+'.png'))
    image4 = ttk.Label(info3_frame, image=Bar_photo)
    image4.pack(side="left")
    
    tab_5 = ttk.Frame(notebook)
    notebook.add(tab_5, text="進化鍊")
    
    evo = getImgIdEnCh(item[0])
    
    evo1_frame = ttk.LabelFrame(tab_5,text="第一階段")
    evo1_frame.pack(side="top",padx=20)
    evo1_photo=[]
    for i in range(len(evo[0])):
        evo1_photo.append(ImageTk.PhotoImage(Image.open('image\poke_image\Pokemon_'+evo[0][i]+'.png').resize((200,200), Image.ANTIALIAS)))
        ttk.Label(evo1_frame, image=evo1_photo[i]).pack(side="left", fill="both",padx=10,pady=10)
    
    evo2_frame = ttk.LabelFrame(tab_5,text="第二階段")
    evo2_frame.pack(side="top",padx=20)
    evo2_photo=[]
    for i in range(len(evo[1])):
        evo2_photo.append(ImageTk.PhotoImage(Image.open('image\poke_image\Pokemon_'+evo[1][i]+'.png').resize((200,200), Image.ANTIALIAS)))
        ttk.Label(evo2_frame, image=evo2_photo[i]).pack(side="left", fill="both",padx=10,pady=10)
    
    evo3_frame = ttk.LabelFrame(tab_5,text="第三階段")
    evo3_frame.pack(side="top",padx=20)
    evo3_photo=[]
    for i in range(len(evo[2])):
        evo3_photo.append(ImageTk.PhotoImage(Image.open('image\poke_image\Pokemon_'+evo[2][i]+'.png').resize((200,200), Image.ANTIALIAS)))
        ttk.Label(evo3_frame, image=evo3_photo[i]).pack(side="left", fill="both",padx=10,pady=10)
    
    notebook.pack(side='left',fill="both",expand=True, padx=5, pady=5)
    
    # Center the window, and set minsize
    window.update()
    window.minsize(window.winfo_width(), window.winfo_height())
    x_cordinate = int((window.winfo_screenwidth()/2) - (window.winfo_width()/2))
    y_cordinate = int((window.winfo_screenheight()/2) - (window.winfo_height()/2))
    window.geometry("+{}+{}".format(x_cordinate, y_cordinate))
    
    mainloop()

#j=["image",'再不出來','我就去玩遊戲了']
#ui(j)