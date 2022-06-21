import requests
from bs4 import BeautifulSoup

'''
    取得基本資料 getBasicInfo(中文寶可夢名)
    回傳([屬性],分類,[特性],[隱藏特性],100級時經驗值,身高,體重,[雄性比例,雌性比例,無性別(0或1)])
    
    取得種族值 getSpeciesStrength(中文寶可夢名)
    回傳 list in tuple 最高及最低值 依序為 (HP 攻擊 防禦 特攻 特防 速度)
    
    取得屬性相性  Effectiveness(中文寶可夢名)
    回傳 list 依序為 一般 火 水 電 草 冰 格鬥 毒 地面 飛行 超能力 蟲 幽靈 龍 惡 鋼 仙子
    
    取得進化鏈 getEvolution(寶可夢編號)
    回傳 [[第一階],[第二階],[第三階]] 如無第三階，則其為 '', 如無進化則都為 ''
    
    Version 2
'''

soup = None

def getHTML(url):
    response = requests.get(url)
    soup=BeautifulSoup(response.text,"html.parser")
    return soup

def getBasicInfoTable(soup):
    raw=soup.find_all('table',attrs={'class':'roundy bgwhite fulltable'})
    return raw

def getType(raw):
    raw=raw[1]
    a=raw.find_all('a')
    type=[]
    for i in a:
        type.append(i.get_text())
    return type

def getCategory(raw):
    for i in raw[2]:
        category = i.get_text()
    category=category.strip("\n")
    return category

def getAbilities(raw):
    for i in raw[3]:
        if i !='\n':
            i=i.get_text()
            i=i.split()
            allAbilities=i
    abilities=[]
    hiddenAbilities=[]
    for i in allAbilities:
        if i != '或' and '隱藏特性' not in i:
            abilities.append(i)
        if '隱藏特性' in i:
            i=i.strip('隱藏特性')
            hiddenAbilities.append(i)
        
    return abilities, hiddenAbilities

def getMaxExpRequire(raw):
    exp=raw[4].get_text()
    exp=exp.strip("\n")
    return exp

def getHeightAndWeight(raw):
    height=raw[6].get_text()
    height=height.strip('\n')
    weight=raw[7].get_text()
    weight=weight.strip('\n')
    
    return height, weight

def getGenders(soup):
    raw = soup.find_all('table')
    male=raw[4].find_all('span',attrs={'style':'color:#00F;'})
    female=raw[4].find_all('span',attrs={'style':'color:#FF6060;'})
    genders=['','','']
    for i in male:
        i=i.get_text()
        if '雄性' in i:
            i=i.strip('雄性')
            i=i.strip('%')
            i=i.strip(' ')
            genders[0]=float(i)
            if i=='100':
                genders[1]=0
    for i in female:
        i=i.get_text()
        if '雌性' in i:
            i=i.strip('雌性')
            i=i.strip('%')
            i=i.strip(' ')
            genders[1]=float(i)
            if i=='100':
                genders[0]=0
    if genders[0] == '' and genders[1]=='':
        genders[0]=genders[1]=0
        genders[2]= 1
    else:
        genders[2]= 0
    return genders

def _getss(strength,soup):
    zhs=['HP','攻击','防御','特攻','特防','速度']
    zht=['ＨＰ：','攻擊：','防禦：','特攻：','特防：','速度：']
    s=soup.find_all('tr',attrs={'class':'bgl-'+zhs[strength]})
    s=s[0].get_text().split()
    s[0]=s[0].strip(zht[strength])
    s[1]=s[6]
    del s[2:]
    s=[int(x) for x in s]
    return s

def _typeEffectivenessChart(type_):
    normal=     [ 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1]
    fire=       [ 1,.5, 2, 1,.5,.5, 1, 1, 2, 1, 1,.5, 2, 1, 1, 1,.5,.5]
    water=      [ 1,.5,.5, 2, 2,.5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,.5, 1]
    electric=   [ 1, 1, 1,.5, 1, 1, 1, 1, 2,.5, 1, 1, 1, 1, 1, 1,.5, 1]
    grass=      [ 1, 2,.5,.5,.5, 2, 1, 2,.5, 2, 1, 2, 1, 1, 1, 1, 1, 1]
    ice=        [ 1, 2, 1, 1, 1,.5, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1]
    fighting=   [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2,.5,.5, 1, 1,.5, 1, 2]
    poison=     [ 1, 1, 1, 1,.5, 1,.5,.5, 2, 1, 2,.5, 1, 1, 1, 1, 1,.5]
    ground=     [ 1, 1, 2, 0, 2, 2, 1,.5, 1, 1, 1, 1,.5, 1, 1, 1, 1, 1]
    flying=     [ 1, 1, 1, 2,.5, 2,.5, 1, 0, 1, 1,.5, 2, 1, 1, 1, 1, 1]
    psychic=    [ 1, 1, 1, 1, 1, 1,.5, 1, 1, 1,.5, 2, 1, 2, 1, 2, 1, 1]
    bug=        [ 1, 2, 1, 1,.5, 1,.5, 1,.5, 2, 1, 1, 2, 1, 1, 1, 1, 1]
    rock=       [.5,.5, 2, 1, 2, 1, 2,.5, 2,.5, 1, 1, 1, 1, 1, 1, 2, 1]
    ghost=      [ 0, 1, 1, 1, 1, 1, 0,.5, 1, 1, 1,.5, 1, 2, 1, 2, 1, 1]
    dragon=     [ 1,.5,.5,.5,.5, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2]
    dark=       [ 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 0, 2, 1,.5, 1,.5, 1, 2]
    steel=      [.5, 2, 1, 1,.5,.5, 2, 0, 2,.5,.5,.5,.5, 1,.5, 1,.5,.5]
    fairy=      [ 1, 1, 1, 1, 1, 1,.5, 2, 1, 1, 1,.5, 1, 1, 0,.5, 2, 1]
    
    if type_ == '一般':
        return normal
    if type_ == '火':
        return fire
    if type_ == '水':
        return water
    if type_ == '電':
        return electric
    if type_ == '草':
        return grass
    if type_ == '冰':
        return ice
    if type_ == '格鬥':
        return fighting
    if type_ == '毒':
        return poison
    if type_ == '地面':
        return ground
    if type_ == '飛行':
        return flying
    if type_ == '超能力':
        return psychic
    if type_ == '蟲':
        return bug
    if type_ == '岩石':
        return rock
    if type_ == '幽靈':
        return ghost
    if type_ == '龍':
        return dragon
    if type_ == '惡':
        return dark
    if type_ == '鋼':
        return steel
    if type_ == '仙子':
        return fairy

def _typeEffectiveness(type_):
    effectiveness=[]
    if len(type_)==1:
        effectiveness=_typeEffectivenessChart(type_[0])
    else:
        for t1, t2 in zip(_typeEffectivenessChart(type_[0]),_typeEffectivenessChart(type_[1])):
            effectiveness.append(t1*t2)
    return effectiveness

def Effectiveness(zhName):
    return _typeEffectiveness(getType(getBasicInfoTable(getHTML('https://wiki.52poke.com/zh-hant/'+zhName))))

def getSpeciesStrength(zhName):
    url='https://wiki.52poke.com/zh-hant/'+zhName
    soup=getHTML(url)
    hp=_getss(0,soup)
    attack=_getss(1,soup)
    defence=_getss(2,soup)
    spAtk=_getss(3,soup)
    spDef=_getss(4,soup)
    speed=_getss(5,soup)
    
    return hp, attack, defence, spAtk, spDef, speed
    
def getBasicInfo(zhName):
    url='https://wiki.52poke.com/zh-hant/'+zhName
    soup=getHTML(url)
    raw=getBasicInfoTable(soup)
    type_=getType(raw)
    category=getCategory(raw)
    abilities,hiddenAbilities=getAbilities(raw)
    exp=getMaxExpRequire(raw)  
    height,weight=getHeightAndWeight(raw)
    genders=getGenders(soup)
    
    return type_, category, abilities, hiddenAbilities, exp, height, weight, genders

def getEvolution(id_):
    if int(id_)<10:
        id_ = str(id_)
        id_ = '00'+id_
    elif int(id_)<100:
        id_ = str(id_)
        id_ = '0'+id_ 
    url = 'https://tw.portal-pokemon.com/play/pokedex/' + str(id_)
    response = requests.get(url)
    soup=BeautifulSoup(response.text,"html.parser")
    soup = soup.find_all('div',attrs={'class':'pokemon-evolutionlevel'})
    evoChian=['','','']
    lv=0
    for i in soup:
        name = i.find_all('p',attrs={'class':'pokemon-evolution-item__info-name'})
        nextLv = i.find('div',attrs={'class':'pokemon-evolution__arrow-wrapper'})
        sameLv=[]
        for j in name:
            sameLv.append(j.get_text())
        if nextLv != None:
            evoChian[lv]=sameLv
            lv=lv+1
        evoChian[lv]=sameLv
    return evoChian

def getBiology(zhName):
    url = 'https://wiki.52poke.com/zh-hant/'+zhName
    soup=getHTML(url)
    
    check=False
    bio = ''
    
    for i in soup:
        text = i.get_text()
        if '概述' in text or '基本介紹' in text:
            split = text.split('\n')
        
            for j in split:
                if j=='概述' or j=='基本介紹' or j=='概述=':
                    check=True
                
                if j=='動畫中':
                    check=False
                
                if check==True and '主頁面' not in j and j!='概述' and j!='基本介紹' and j!='概述=':
                    bio=bio+j+'\n'
    return bio

def _test(n,id_):
    print("內容："+str(getBasicInfo(n)))
    print("種族值："+str(getSpeciesStrength(n)))
    print("進化鍊："+str(getEvolution(id_)))
    print("文字敘述："+str(getBiology(n)))
