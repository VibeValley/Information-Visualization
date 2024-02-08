import tkinter as tk
from tkinter import *
from tkinter import ttk
import math
# from pynput import mouse



class Point:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id

        def __str__(self):
            return f"{self.x}i{self.y:+}j"


# load csv
def load_csv(file):
    data = []
    with open(file, "r") as file:
        for line in file:
            values = line.strip().split(",")
            data.append(Point(float(values[0]), float(values[1]), values[2]))
    return data


data = load_csv("data2.csv")
data1 = FALSE
data2 = TRUE

root = Tk()
root.geometry("1000x1000")
root.title("Canvas")
canvas = Canvas(root, bg="white", width="1000", height="1000")
canvas.pack()


def calculateMax(data):
    max_x = 0
    max_y = 0
    for point in data:
        if point.x > max_x:
            max_x = point.x
        if point.y > max_y:
            max_y = point.y

    maxT = (max_x, max_y)
    return maxT


def drawGraph(maxT):

    if data1:
        canvas.create_text(
            (100, 700),
            fill="black",
            text="Dot = a",
            width="100",
            font="Helvetica 15 bold",
        )
        canvas.create_text(
            (100, 730),
            fill="green",
            text="Rect = b",
            width="100",
            font="Helvetica 15 bold",
        )
        canvas.create_text(
            (100, 760),
            fill="red",
            text="Cross = c",
            width="100",
            font="Helvetica 15 bold",
        )

    if data2:
        canvas.create_text(
            (100, 700),
            fill="black",
            text="Dot = foo",
            width="120",
            font="Helvetica 15 bold",
        )
        canvas.create_text(
            (100, 730),
            fill="green",
            text="Rect = baz",
            width="120",
            font="Helvetica 15 bold",
        )
        canvas.create_text(
            (100, 760),
            fill="red",
            text="Cross = bar",
            width="120",
            font="Helvetica 15 bold",
        )

    xStart = 50
    xMid = 450 + xStart
    xEnd = 950

    yStart = 50
    yMid = 450 + xStart
    yEnd = 950

    canvas.create_line((xStart, yMid, xEnd, yMid), fill="black")
    canvas.create_line((xMid, yStart, xMid, yEnd), fill="black")
    # canvas.create_oval((400,400,450,450))
    """canvas.create_line((5,460,5,440), fill='black')"""

    for i in range(
        13
    ):  # 9 is the window size step for 1, f.e. from 1->2 is 0->9 in window
        canvas.create_line(
            (xStart + i * 75, yMid + 10, xStart + i * 75, yMid - 10), fill="black"
        )
        tick = canvas.create_line(
            (xMid + 10, yStart + i * 75, xMid - 10, yStart + i * 75), fill="black"
        )

        if i != 6:
            canvas.create_text(
                (xStart + i * 75, yMid + 20),
                fill="black",
                text=round(-maxT[0] + i * ((abs(maxT[0]) * 2) / 12), 1),
                width="30",
            )
            canvas.create_text(
                (xMid - 20, yStart + i * 75),
                fill="black",
                text=round(maxT[1] - i * ((abs(maxT[1]) * 2) / 12), 1),
                width="30",
            )


def drawDot(x, y, maxT):
    size = 4

    oval = canvas.create_oval((x - size, y - size, x + size, y + size), fill="black")
    canvas.tag_bind(oval, "<Button-1>", on_left_button_clicked)
    canvas.tag_bind(oval, "<Button-3>", on_right_button_clicked)


def drawRect(x, y, maxT):
    size = 4
    rect = canvas.create_rectangle(
        (x - size, y - size, x + size, y + size), fill="green"
    )
    canvas.tag_bind(rect, "<Button-1>", on_left_button_clicked)
    canvas.tag_bind(rect, "<Button-3>", on_right_button_clicked)


def drawCross(x, y, maxT):
    size = 5

    line2 = canvas.create_line((x - size, y - size + 1, x + size, y + size), fill="red")
    line = canvas.create_line((x - size, y + size - 1, x + size, y - size), fill="red")
    canvas.tag_bind(line, "<Button-1>", on_left_button_clicked)
    canvas.tag_bind(line2, "<Button-1>", on_left_button_clicked)
    canvas.tag_bind(line, "<Button-3>", on_right_button_clicked)
    canvas.tag_bind(line2, "<Button-3>", on_right_button_clicked)


def changeToRelativeCoordinate(pointX, pointY):
        timesValueX = (450) / maxT[0]
        timesValueY = (450) / maxT[1]
        window_x = pointX * timesValueX + 500
        window_y = -pointY * timesValueY + 500
        return (window_x, window_y)


maxT = calculateMax(data)
def setZero():
    return (0,0)

clickedPoint = (0,0)



def scatterplot(data):
    for point in data:
        (window_x, window_y) = changeToRelativeCoordinate(point.x,point.y)
        if point.id == "a" or point.id == "foo":     
            drawDot(window_x, window_y, maxT)
        elif point.id == "b" or point.id == "baz":
            drawRect(window_x, window_y, maxT)
        else:
            drawCross(window_x, window_y, maxT)


def scatterplot2(data, newCenterX, newCenterY, closestItemPoint):
    timesValueX = (450) / maxT[0]
    timesValueY = (450) / maxT[1]

    #print(closestItemPoint)
    (window_x1, window_y1) = changeToRelativeCoordinate(closestItemPoint[0],closestItemPoint[1])
    #print(window_x1, "   ",window_y1)
    print("Center point: ", newCenterX, newCenterY)
    itemIndex = 0
    for point in data:
            (window_x, window_y) = changeToRelativeCoordinate(point.x,point.y)
            (newCenterX, newCenterY) = changeToRelativeCoordinate(closestItemPoint[0],closestItemPoint[1])
            theDiff_x = 500 - newCenterX
            theDiff_y = 500 - newCenterY

            newWindow_x = window_x + theDiff_x
            newWindow_y = window_y + theDiff_y
            

            if(closestItemPoint[0] == point.x and closestItemPoint[1] == point.y):
                oval = canvas.create_oval((newWindow_x - 5,newWindow_y - 5, newWindow_x + 5, newWindow_y + 5), fill="black")
                oval2 = canvas.create_oval((newWindow_x - 7, newWindow_y - 7, newWindow_x + 7, newWindow_y + 7))
                canvas.tag_bind(oval, "<Button-1>", on_left_button_clicked)
                canvas.tag_bind(oval2, "<Button-3>", on_right_button_clicked)
            elif(window_y < newCenterY and window_x < newCenterX):
                line2 = canvas.create_line((newWindow_x - 5, newWindow_y - 5 + 1, newWindow_x + 5, newWindow_y + 5), fill="red")
                line = canvas.create_line((newWindow_x - 5, newWindow_y + 5 - 1, newWindow_x + 5, newWindow_y - 5), fill="red")
                canvas.tag_bind(line, "<Button-1>", on_left_button_clicked)
                canvas.tag_bind(line2, "<Button-1>", on_left_button_clicked)
                canvas.tag_bind(line2, "<Button-3>", on_right_button_clicked)
                canvas.tag_bind(line, "<Button-3>", on_right_button_clicked)
            elif (window_y < newCenterY and window_x > newCenterX):
                line2 = canvas.create_line((newWindow_x - 5, newWindow_y - 5 + 1, newWindow_x + 5, newWindow_y + 5), fill="blue")
                line = canvas.create_line((newWindow_x - 5, newWindow_y + 5 - 1, newWindow_x + 5, newWindow_y - 5), fill="blue")
                canvas.tag_bind(line, "<Button-1>", on_left_button_clicked)
                canvas.tag_bind(line2, "<Button-1>", on_left_button_clicked)
                canvas.tag_bind(line, "<Button-3>", on_right_button_clicked)
                canvas.tag_bind(line2, "<Button-3>", on_right_button_clicked)
            elif(window_y > newCenterY and window_x > newCenterX):
                oval = canvas.create_oval((newWindow_x - 5, newWindow_y - 5, newWindow_x + 5, newWindow_y + 5), fill="black")
                canvas.tag_bind(oval, "<Button-1>", on_left_button_clicked)
                canvas.tag_bind(oval, "<Button-3>", on_right_button_clicked)
            elif(window_y > newCenterY and window_x < newCenterX):
                rect = canvas.create_rectangle((newWindow_x - 4, newWindow_y - 4, newWindow_x + 4,newWindow_y + 4), fill="green")
                canvas.tag_bind(rect, "<Button-1>", on_left_button_clicked)
                canvas.tag_bind(rect, "<Button-3>", on_right_button_clicked)
            else:
                oval = canvas.create_oval((newWindow_x - 5,newWindow_y - 5, newWindow_x + 5, newWindow_y + 5), fill="black")
                oval2 = canvas.create_oval((newWindow_x - 7, newWindow_y - 7, newWindow_x + 7, newWindow_y + 7))
                canvas.tag_bind(oval, "<Button-1>", on_left_button_clicked)
                canvas.tag_bind(oval2, "<Button-1>", on_left_button_clicked)
                canvas.tag_bind(oval, "<Button-3>", on_right_button_clicked)
                canvas.tag_bind(oval2, "<Button-3>", on_right_button_clicked)
            
            #print("new ",newWindow_x)
            #print("old ",window_x)
            point.x = (newWindow_x - 500) / timesValueX
            point.y = -((newWindow_y - 500) / timesValueY)
            itemIndex = itemIndex + 1


def scatterplot3(data, fiveClosestPoints, CenterPoint):
    for point in data:
        #Kollar ifall 
        found = FALSE
        (window_x, window_y) = changeToRelativeCoordinate(point.x,point.y)
        for close in fiveClosestPoints:
            if(close[0] == point.x and close[1] == point.y):
                found = TRUE
                if(window_x < 500 and window_y < 500):
                    line2 = canvas.create_line((window_x - 5, window_y - 5 + 1, window_x + 5, window_y + 5), fill="red")
                    line = canvas.create_line((window_x - 5, window_y + 5 - 1, window_x + 5, window_y - 5), fill="red")
                    canvas.tag_bind(line, "<Button-3>", on_right_button_clicked)
                    canvas.tag_bind(line2, "<Button-3>", on_right_button_clicked)
                    canvas.tag_bind(line, "<Button-1>", on_left_button_clicked)
                    canvas.tag_bind(line2, "<Button-1>", on_left_button_clicked)
                elif(window_x > 500 and window_y < 500):
                    line2 = canvas.create_line((window_x - 5, window_y - 5 + 1, window_x + 5, window_y + 5), fill="blue")
                    line = canvas.create_line((window_x - 5, window_y + 5 - 1, window_x + 5, window_y - 5), fill="blue")
                    canvas.tag_bind(line, "<Button-1>", on_left_button_clicked)
                    canvas.tag_bind(line2, "<Button-1>", on_left_button_clicked)
                    canvas.tag_bind(line, "<Button-3>", on_right_button_clicked)
                    canvas.tag_bind(line2, "<Button-3>", on_right_button_clicked)
                elif(window_x > 500 and window_y > 500):
                    oval = canvas.create_oval((window_x - 5, window_y - 5, window_x + 5, window_y + 5), fill="black")
                    canvas.tag_bind(oval, "<Button-1>", on_left_button_clicked)
                    canvas.tag_bind(oval, "<Button-3>", on_right_button_clicked)
                elif(window_x < 500 and window_y > 500):
                    rect = canvas.create_rectangle((window_x - 4, window_y - 4, window_x + 4,window_y + 4), fill="green")
                    canvas.tag_bind(rect, "<Button-1>", on_left_button_clicked)
                    canvas.tag_bind(rect, "<Button-3>", on_right_button_clicked)
                break
        if point.x == CenterPoint[0] and point.y == CenterPoint[1]:     
            oval = canvas.create_oval((window_x - 5,window_y - 5, window_x + 5, window_y + 5), fill="black")
            oval2 = canvas.create_oval((window_x - 7, window_y - 7, window_x + 7, window_y + 7))
            canvas.tag_bind(oval, "<Button-3>", on_right_button_clicked)
            canvas.tag_bind(oval2, "<Button-3>", on_right_button_clicked)
        elif(found == FALSE):
            if(window_x < 500 and window_y < 500):
                line2 = canvas.create_line((window_x - 5, window_y - 5 + 1, window_x + 5, window_y + 5), fill="#e3c5c9")
                line = canvas.create_line((window_x - 5, window_y + 5 - 1, window_x + 5, window_y - 5), fill="#e3c5c9")
                canvas.tag_bind(line, "<Button-3>", on_right_button_clicked)
                canvas.tag_bind(line2, "<Button-3>", on_right_button_clicked)
                canvas.tag_bind(line, "<Button-1>", on_left_button_clicked)
                canvas.tag_bind(line2, "<Button-1>", on_left_button_clicked)
            elif(window_x > 500 and window_y < 500):
                line2 = canvas.create_line((window_x - 5, window_y - 5 + 1, window_x + 5, window_y + 5), fill="#b8bfe0")
                line = canvas.create_line((window_x - 5, window_y + 5 - 1, window_x + 5, window_y - 5), fill="#b8bfe0")
                canvas.tag_bind(line, "<Button-1>", on_left_button_clicked)
                canvas.tag_bind(line2, "<Button-1>", on_left_button_clicked)
                canvas.tag_bind(line, "<Button-3>", on_right_button_clicked)
                canvas.tag_bind(line2, "<Button-3>", on_right_button_clicked)
            elif(window_x > 500 and window_y > 500):
                oval = canvas.create_oval((window_x - 5, window_y - 5, window_x + 5, window_y + 5), fill="#b6b8b6")
                canvas.tag_bind(oval, "<Button-1>", on_left_button_clicked)
                canvas.tag_bind(oval, "<Button-3>", on_right_button_clicked)
            elif(window_x < 500 and window_y > 500):
                rect = canvas.create_rectangle((window_x - 4, window_y - 4, window_x + 4,window_y + 4), fill="#cbf2cb")
                canvas.tag_bind(rect, "<Button-1>", on_left_button_clicked)
                canvas.tag_bind(rect, "<Button-3>", on_right_button_clicked)
            

def euclidean_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

def findClosestItem(clickedX, clickedY):
    timesValueX = (450) / maxT[0]
    timesValueY = (450) / maxT[1]
    clickedX = (clickedX - 500) / timesValueX
    clickedY = -((clickedY - 500) / timesValueY)
    closestDist = 1000
    pointCoords = (0,0)
    for point in data:
        dist = euclidean_distance((clickedX,clickedY), (point.x, point.y))
        if(dist < closestDist):
            closestDist = dist
            pointCoords = (point.x, point.y)
    return(pointCoords)
def findClosestFive(clickedPoint):
    fiveClosest = [(996,996), (997,997), (998,998), (999,999), (1000,1000)]
    k = 0
    for point in data: 
        
        dist = euclidean_distance((clickedPoint[0],clickedPoint[1]), (point.x,point.y))
        
        currestIndex = 0
        lastIndex = 4
        for close in fiveClosest:
            k = k+1
            if(dist < euclidean_distance((clickedPoint[0],clickedPoint[1]), close) and clickedPoint[0] != point.x and clickedPoint[1] != point.y):
                print("point: ", point.x, point.y)
                for i in range(5-currestIndex):
                    if(fiveClosest[lastIndex-i] == fiveClosest[currestIndex]):
                        print("JAG BREAKAR LOOPEN")
                        break
                    print("lastindex i = ", lastIndex-i)
                    fiveClosest[lastIndex-i] = fiveClosest[lastIndex-i-1] # Kommer returna hela arrayen som ett värde
                    
                fiveClosest[currestIndex] = (point.x,point.y)
                break
            currestIndex = currestIndex+1
    print(k)
    return fiveClosest




def clearCanvas():
    canvas.delete("all")
    drawGraph(maxT)


def on_left_button_clicked(event):
    item = canvas.find_closest(event.x, event.y)
    closestItem  = findClosestItem(event.x, event.y)

    #print(event)
    if item:
        clearCanvas()
        print(event.x, " ", event.y)
        scatterplot2(data, closestItem[0], closestItem[1], closestItem)

def on_right_button_clicked(event):
    item = canvas.find_closest(event.x, event.y)
    closestItem  = findClosestItem(event.x, event.y)
    global clickedPoint
    if item:
        clearCanvas()
        if(clickedPoint[0] == closestItem[0] and clickedPoint[1] == closestItem[1]):
            scatterplot(data)
        else:
            five = findClosestFive(closestItem)
            scatterplot3(data, five, closestItem)
            clickedPoint = closestItem





# print(maxT[0])
# print(maxT[1])



drawGraph(maxT)
scatterplot(data)
# canvas.bind("<Button-1>", on_left_button_clicked)

root.mainloop()

# print(data[1].id)
