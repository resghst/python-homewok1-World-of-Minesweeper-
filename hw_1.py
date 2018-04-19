# coding=utf-8
from copy import deepcopy
import random
import time

victor = [
  # X , Y
  [ -1, -1 ], # LT
  [  0, -1 ], # L
  [  1, -1 ], # LD
  [  1,  0 ], # D
  [  1,  1 ], # RD
  [  0,  1 ], # R
  [ -1,  1 ], # RT
  [ -1,  0 ], # T
]

def countbomb( bombpos, infomap):
  global victor
  for conpoment in victor: addvictor(bombpos, infomap, conpoment)

def addvictor(bombpos, infomap, dir):
  x = bombpos[0]
  y = bombpos[1]
  dirx = dir[0]
  diry = dir[1]
  if(0<=x+dirx and x+dirx<=8 and 0<=y+diry and y+diry<=8):
    if( infomap[x+dirx][y+diry] == -1 ): return
    else: infomap[x+dirx][y+diry] += 1

def printGameview(mask, infomap, fd):
  gamestr = [
    '        踩  地  雷  遊  戲\n', ' Y|  0  1  2  3  4  5  6  7  8\n', ' X|---------------------------\n',
    ' 0|', ' 1|', ' 2|', ' 3|', ' 4|', ' 5|', ' 6|', ' 7|', ' 8|'
  ]
  block = '██'
  print "--------------------------------------------"
  print gamestr[0] + gamestr[1] + gamestr[2],
  fd.write( gamestr[0] + gamestr[1] + gamestr[2],)
  i=3
  for x in range(0,9):
    print gamestr[i],
    fd.write(gamestr[i],)
    i+=1
    for y in range(0,9):
      if(mask[x][y] == 1): 
        print block,
        fd.write( ' ' + str(block,) )  
      elif(infomap[x][y] == -1): 
        print str(infomap[x][y]),
        fd.write(' ' + str(infomap[x][y]),)        
      else: 
        print ' ' + str(infomap[x][y]),
        fd.write('  ' + str(infomap[x][y]),)   
    print ""
    fd.write('\n')
  fd.write('\n')

def gameround(mask, infomap, fd):
  printGameview(mask, infomap, fd)
  inputfinish = 0
  pickpos = []
  pickpos = raw_input('輸入要踩的位置[ 格式 X,Y ](例:X,Y : 0<=x<=8, 0<=y<=8)\n')
  while(inputfinish==0):
    try:
      pickpos = pickpos.split(',')
      pickpos = [int(i) for i in pickpos]
      inputfinish = 1
    except Exception: 
      pickpos = raw_input('輸入要踩的位置[ 格式 X,Y ](例:X,Y : 0<=x<=8, 0<=y<=8)\n')
      print('error input')
      inputfinish = 0
  x = pickpos[1]
  y = pickpos[0]
  mask[x][y]=0
  if(infomap[x][y] == -1): return  1
  elif(infomap[x][y] != 0): return  0
  elif(infomap[x][y] == 0):
    selectnull(x, y)
    return  0

def aipick(mask, infomap, x, y, pmap, fd):
  printGameview(mask, infomap, fd)
  print "pick "+str(x)+'  '+str(y)
  mask[x][y]=0
  if(infomap[x][y] == -1): 
    mask[x][y] = 1
    pmap[x][y] = 1
    print "bomb pos"+str(x)+','+str(y)
    return  -1
  elif(infomap[x][y] != 0): 
    pmap[x][y] = -1
    return  0
  elif(infomap[x][y] == 0):
    pmap[x][y] = -1
    selectnull(x, y)
    return  0

def aicountP(mask, infomap, pmap):
  global victor
  min = 2
  for x in range(0,9):
    for y in range(0,9):
      if(mask[x][y]==0):
        edge = 0
        bomb = infomap[x][y]
        for conpoment in victor:
          dx = conpoment[0]
          dy = conpoment[1]
          if(0<=x+dx and x+dx<=8 and 0<=y+dy and y+dy<=8):
            if(mask[x+dx][y+dy]==1): edge+=1 
            if(pmap[x+dx][y+dy]==1): bomb-=1 
            if(mask[x+dx][y+dy]==0): pmap[x+dx][y+dy]=-1
        if(edge==0): continue
        p =  float(bomb)/float(edge)
        for conpoment in victor:
          dx = conpoment[0]
          dy = conpoment[1]
          if(0<=x+dx and x+dx<=8 and 0<=y+dy and y+dy<=8):
            if( mask[x+dx][y+dy]==1 and pmap[x+dx][y+dy]<p ):  pmap[x+dx][y+dy]=p 
  
  # --------------------------------------------------------------------------------------
  anslist = []
  i = 0
  for x in range(0,9):
    for y in range(0,9):
      if( min>pmap[x][y] and pmap[x][y]!=-1 ): min = pmap[x][y]
  for x in range(0,9):
    for y in range(0,9):
      if( min == pmap[x][y] and pmap[x][y]!=-1 ): 
        anslist.append([x,y])
        i+=1
  i = random.randint(0, i-1)
  print "p = "+ str(min) + ', i = '+ str(i)
  print 'predict '+ str(anslist[i])
  # for k in pmap:
  #   for j in k:
  #     print str("%.3f"%j)+ "\t",
  #   print '\n'
  return anslist[i][0], anslist[i][1]

def selectnull(x, y):
  global victor
  for conpoment in victor:
    dirx = conpoment[1]
    diry = conpoment[0]
    if(0<=x+dirx and x+dirx<=8 and 0<=y+diry and y+diry<=8):
      if(infomap[x+dirx][y+diry]==0 and mask[x+dirx][y+diry]!=0):
        mask[x+dirx][y+diry]=0
        selectnull(x+dirx, y+diry)
      else: 
        mask[x+dirx][y+diry]=0

def openbombpos(mask, infomap):
  count=0
  for x in range(0,9):
    for y in range(0,9):
      if(infomap[x][y]==-1 and mask[x][y]!=0 ): 
        mask[x][y]=0
        count+=1
  return count

if __name__=="__main__":
  gamemap = [[0] for i in range(0,9)]
  fd = open("data01.txt",'r')
  i=0
  bombcount = 0
  for line in fd:
    inputrow = line.strip('\n').split(',')
    inputrow = [int(j) for j in inputrow]
    gamemap[i] = inputrow
    i+=1
  fd.close()
  infomap = deepcopy(gamemap)
  for x in range(0,9):
    for y in range(0,9):
      if(infomap[x][y] == -1): 
        bombcount+=1
        countbomb([x,y],infomap)

  fd = open('standard.txt','w')
  for i in infomap: fd.write(str(i).strip('[]')+"\n")
  fd.close()
  # =================================================================

  fdplay = open('play.txt','w+')
  fdresult = open('result.txt','w+')
  mask = [[1]*9 for i in range(0,9)]
  pmap = [[float(0)]*9 for i in range(0,9)]
  maskcount = 9*9
  live = 3
  x = random.randint(0, 8)
  y = random.randint(0, 8)
  live += aipick(mask, infomap, x, y, pmap, fdplay)
  while(live>0):
    time.sleep(0.5)
    x, y = aicountP(mask, infomap, pmap)
    opencount = 0
    live += aipick(mask, infomap, x, y, pmap, fdplay)
    for x in range(0,9):
      for y in range(0,9):
        if(mask[x][y] == 0): opencount+=1
    print opencount
    if( maskcount-bombcount == opencount ): 
      # print 'game win'
      break
  
  printGameview(mask, infomap, fdresult)
  if( maskcount-bombcount == opencount ):
      print 'game win'
  else:
      print 'game lose'
  

# =================================================================

  # fdplay = open('play.txt','w+')
  # fdresult = open('result.txt','w+')

  # mask = [[1]*9 for i in range(0,9)]
  # maskcount = 9*9
  # end = 0
  # print maskcount-bombcount 
  # while(end==0):
  #   opencount = 0
  #   end = gameround(mask, infomap, fdplay)
  #   for x in range(0,9):
  #     for y in range(0,9):
  #       if(mask[x][y] == 0): opencount+=1
  #   print opencount
  #   if( maskcount-bombcount == opencount ): 
  #     print 'game win'
  #     break

  # opencount+=openbombpos(mask, infomap)
  # printGameview(mask, infomap, fdresult)
  # print end
  # score = opencount/maskcount *30
  # fdplay.close()
  # fdresult.close()