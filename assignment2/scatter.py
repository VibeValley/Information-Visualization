import tkinter as tk
from tkinter import *
from tkinter import ttk

print('hej')



class Point:
  def __init__(self,x,y,id):
    self.x = x
    self.y = y
    self.id = id

    def __str__(self):
        return f'{self.x}i{self.y:+}j'
    

# load csv
def load_csv(file):
    data = []
    with open(file, "r") as file:
        for line in file:
            values = line.strip().split(",")
            data.append(Point(
                float(values[0]),
                float(values[1]),
                values[2]
            ))
    return data


data = load_csv('data2.csv')
data1 = False
data2 = True

root = Tk()
root.geometry('1000x1000')
root.title('Canvas')
canvas = Canvas(root, bg='white', width='1000', height='1000')
canvas.pack()

def calculateMax(data):
   max_x = 0
   max_y = 0
   for point in data:
      if(point.x > max_x):
         max_x = point.x
      if(point.y > max_y):
         max_y = point.y

   maxT = (max_x,max_y)
   return maxT

def drawGraph(maxT):

   if(data1):
      canvas.create_text((100,700), fill='black', text='Dot = a', width='100', font='Helvetica 15 bold')
      canvas.create_text((100,730), fill='green', text='Rect = b', width='100', font='Helvetica 15 bold')
      canvas.create_text((100,760), fill='red', text='Cross = c', width='100', font='Helvetica 15 bold')

   if(data2):
      canvas.create_text((100,700), fill='black', text='Dot = foo', width='120', font='Helvetica 15 bold')
      canvas.create_text((100,730), fill='green', text='Rect = baz', width='120', font='Helvetica 15 bold')
      canvas.create_text((100,760), fill='red', text='Cross = bar', width='120', font='Helvetica 15 bold')

   xStart = 50
   xMid = 450+xStart
   xEnd = 950

   yStart = 50
   yMid = 450+xStart
   yEnd = 950

   canvas.create_line((xStart,yMid,xEnd,yMid), fill='black')
   canvas.create_line((xMid,yStart,xMid,yEnd), fill='black')
   #canvas.create_oval((400,400,450,450))
   """canvas.create_line((5,460,5,440), fill='black')"""

   for i in range(13): # 9 is the window size step for 1, f.e. from 1->2 is 0->9 in window
      canvas.create_line((xStart+i*75,yMid+10,xStart+i*75,yMid-10), fill='black')
      canvas.create_line((xMid+10,yStart+i*75,xMid-10,yStart+i*75), fill='black')

      if(i!=6):
        canvas.create_text((xStart+i*75,yMid+20), fill='black', text=round(-maxT[0]+i*((abs(maxT[0])*2)/12), 1), width='30')
        canvas.create_text((xMid-20,yStart+i*75), fill='black', text=round(maxT[1]-i*((abs(maxT[1])*2)/12), 1), width='30')


def drawDot(x,y,maxT):
   timesValueX = (450)/maxT[0]
   timesValueY = (450)/maxT[1]
   window_x = x*timesValueX+500
   window_y = -y*timesValueY+500

   size = 4

   canvas.create_oval((window_x-size,window_y-size,window_x+size,window_y+size), fill='black')
   
def drawRect(x,y,maxT):
   timesValueX = (450)/maxT[0]
   timesValueY = (450)/maxT[1]
   window_x = x*timesValueX+500
   window_y = -y*timesValueY+500

   size = 4

   canvas.create_rectangle((window_x-size,window_y-size,window_x+size,window_y+size), fill='green')

def drawCross(x,y,maxT):
   timesValueX = (450)/maxT[0]
   timesValueY = (450)/maxT[1]
   window_x = x*timesValueX+500
   window_y = -y*timesValueY+500

   size = 5

   canvas.create_line((window_x-size,window_y-size+1,window_x+size,window_y+size), fill='red')
   canvas.create_line((window_x-size,window_y+size-1,window_x+size,window_y-size), fill='red')

maxT = calculateMax(data)

def scatterplot(data):
   for point in data:
      if(point.id == 'a' or point.id == 'foo'):
        drawDot(point.x,point.y,maxT)
      elif(point.id == 'b' or point.id == 'baz'):
        drawRect(point.x,point.y,maxT)
      else:
        drawCross(point.x,point.y, maxT)


""" print(maxT[0])
print(maxT[1]) """


drawGraph(maxT)
scatterplot(data)

root.mainloop()

#print(data[1].id)

""" root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
root.mainloop() """