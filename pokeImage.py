import jieba
import numpy as np
from PIL import Image
from wordcloud import WordCloud
import random
import os.path
from palettable.colorbrewer.sequential import YlGnBu_9
import requests,os
from bs4 import BeautifulSoup
from getPokeInfo import getEvolution
import sqlite3
'''
    使用 getImgAndGenerateTextCloud(寶可夢全國編號,英文名稱,中文名稱)
    即可下載寶可夢的圖片與取得詞雲圖
    寶可夢圖片名稱: pokemonImage+英文名稱(首字母大寫)+.png
    詞雲圖片名稱: pokemonWordcloud+英文名稱(首字母大寫)+.png
    !!! 寶可夢全國編號 為 int 不要在編號前加上'0'或'#'
    如成功會回傳 OK，否則回傳ERROR
    Version 3.0
'''
#圖片資料夾路徑
imgDir = 'image/'

#取得寶可夢圖片連結
def getPokeImgLink(_id,enName):
    if int(_id)<10:
        _id = str(_id)
        _id = '00'+_id
    elif int(_id)<100:
        _id = str(_id)
        _id = '0'+_id  
    url= 'https://wiki.52poke.com/wiki/File:'+str(_id)+enName+'.png'
    #print(url)
    response = requests.get(url)
    if response.status_code != requests.codes.ok:
        return 'ERROR'
    else:
        soup=BeautifulSoup(response.text,"html.parser")
        i = soup.find('div', attrs={'class':'fullImageLink'})
        ia = i.a
        lin = ia.attrs
        imageUrl=lin['href']
        imageUrl = 'https:'+imageUrl
        return imageUrl
    
#下載照片
def downloadImg(imgUrl,enName):
    imgFile = 'image\poke_image\Pokemon_'+enName+'.png'
    isImgExists = os.path.isfile(imgFile)
    if imgUrl=='ERROR':
        return 'ERROR'
    elif isImgExists==True:
        print('image exists')
    else:
        img = requests.get(imgUrl).content
        imgFile = 'image\poke_image\Pokemon_'+enName+'.png'
        with open(imgFile, 'wb') as handler:
            handler.write(img)
   
#取得寶可夢介紹文字等
def getPokeIntro(url):
    response = requests.get(url)
    if response.status_code != requests.codes.ok:
        return 'ERROR'
    else:
        soup=BeautifulSoup(response.text,"html.parser")
        para=[]
        for header in soup.find_all('p'):
            para.append(header)
            fullText=''
        for i in para:
            if i != None:
                fullText=fullText+i.get_text()
        return fullText

def color_func(word,font_size,position,orientation,
               random_state=None,**kwargs):
    return tuple(YlGnBu_9.colors[random.randint(0, 8)])

def getImgAndGenerateTextCloud(id,enName,zhName):
    enName = enName.lower()
    enName = enName.capitalize() 
    isImgDlSuccessful=getImg(id, enName)
    url = 'https://wiki.52poke.com/zh-hant/'+zhName
    text = getPokeIntro(url) 
    text=' '.join(jieba.cut(text))
    text=text.replace('的', '')
    
    if isImgDlSuccessful =='ERROR' or text=='ERROR':
        return 'ERROR'

    imgPath = 'image\poke_image\Pokemon_'+enName+'.png'
    imgFile = 'image\img\Cloud_'+enName+'.png'
    isImgExists = os.path.isfile(imgFile)
    if isImgExists != True:
        img=Image.open(imgPath)
        mask = Image.new("RGB",img.size,(255,255,255))
        mask.paste(img,img)
        mask = np.array(mask)

        font='C:\windows\fonts\msjh.ttc'

        wc=WordCloud(mode = "RGBA",font_path=font,background_color=None,
                 max_words=2000,mask=mask,max_font_size=300,
                 random_state=1)

        wc.generate_from_text(text)
        wc.recolor(color_func=color_func,random_state=2)

        output_path='image\img\Cloud_'+enName+'.png'
        wc.to_file(output_path)
    else: print('cloud exists')

    return 'OK'

def getImg(_id,enName):
    enName = enName.lower()
    enName = enName.capitalize() 
    if not os.path.exists(imgDir):
        os.mkdir(imgDir)
    isImgDlSuccessful = downloadImg(getPokeImgLink(_id, enName),enName)
    if isImgDlSuccessful =='ERROR':
        return 'ERROR'
    return 'OK'

def getImgIdEnCh(_id):
    conn = sqlite3.connect('pokedex.db')
    conn.commit()
    cursor = conn.cursor()
    db="select * from pokemon where ch ="
    evo=getEvolution(_id)
    evoChian=['','','']
    lv=0
    for i in evo:
        samelv=[]
        for j in i:
            data = cursor.execute(db+"'"+j+"'").fetchall()
            getImg(data[0][0],data[0][1])
            samelv.append(data[0][1])
        evoChian[lv]=samelv
        lv+=1
    conn.close()
    return evoChian



