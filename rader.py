import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from matplotlib import cm
import os
from getPokeInfo import getSpeciesStrength

def rader(enName, _min,labels):
    imgFile = 'image\img\Rader_'+enName+'.png'
    isImgExists = os.path.isfile(imgFile)
    if isImgExists != True:
        N = len( _min)
        proportions = np.append( _min, 1)
        theta = np.linspace(0, 2 * np.pi, N, endpoint=False)
        x = np.append(np.sin(theta), 0)
        y = np.append(np.cos(theta), 0)
        triangles = [[N, i, (i + 1) % N] for i in range(N)]
        triang_backgr = tri.Triangulation(x , y , triangles)
        triang_foregr = tri.Triangulation(x * proportions, y * proportions, triangles)
        cmap = plt.cm.rainbow_r
        colors = np.linspace(0, 1, N + 1)

        line_color='white'
    
        plt.tripcolor(triang_backgr, colors, cmap=cmap, shading='gouraud', alpha=0.4)
        plt.tripcolor(triang_foregr, colors, cmap=cmap, shading='gouraud', alpha=0.8)
        plt.triplot(triang_backgr, color=line_color, lw=2)
        for label, color, xi, yi in zip(labels, colors, x, y):
            plt.text(xi * 1.05, yi * 1.05, label,  # color=cmap(color),
                     ha='left' if xi > 0.1 else 'right' if xi < -0.1 else 'center',
                     va='bottom' if yi > 0.1 else 'top' if yi < -0.1 else 'center')
            plt.axis('off')
            plt.gca().set_aspect('equal')
        plt.savefig('image\img\Rader_'+enName+'.png',bbox_inches='tight', transparent=True)
    else: print('pader exists')
    plt.show()
    
def bar(enName, _bar,labels):
    imgFile = 'image\img\Bar_'+enName+'.png'
    isImgExists = os.path.isfile(imgFile)
    if isImgExists != True:
        cmap = cm.rainbow(np.linspace(0, 1, len(labels)))
        x = np.arange(len(labels))
        labels.reverse()
        plt.barh(x,  _bar, color=cmap)
        plt.yticks(x, labels)
        plt.xlim(0, 255)
        plt.savefig('image\img\Bar_'+enName+'.png',bbox_inches='tight', transparent=True)
    else: print('bar exists')
    plt.show()

def rader_main(enName,chName):
    strength=getSpeciesStrength(chName)
    _min = [strength[0][0]/255,strength[1][0]/255,strength[2][0]/255,strength[5][0]/255,strength[4][0]/255,strength[3][0]/255]
    _bar = [strength[5][0],strength[4][0],strength[3][0],strength[2][0],strength[1][0],strength[0][0]]
    labels = ['HP', 'Attack', 'Defense', 'Speed', 'Sp.Def', 'Sp.Atk']
    rader(enName, _min, labels)
    bar(enName, _bar,labels)
    return _bar
