import turtle
import random
import math
import time
import numpy as np

# Встановлення seed для відтворюваності випадкових значень
random.seed(3214)

# Зберігання позицій вузлів для подальшого використання
NodePositions = []

# Створення матриці розміром 11x11 з випадковими значеннями
matrix = [[random.uniform(0, 2) for j in range(11)] for i in range(11)]

# Обчислення значення коефіцієнта k
k = 1.0 - 1 * 0.02 - 4 * 0.005 - 0.25

# Множення матриці на коефіцієнт k
matrixMultipliedBy_k = np.multiply(matrix, k)

# Округлення значень матриці до цілих чисел
matrixForDirected = np.floor(matrixMultipliedBy_k)

# Визначення матриці для неорієнтованого графа
matrixForUndirected = np.maximum(matrixForDirected, np.transpose(matrixForDirected))

print("Матриця суміжності напрямленого графа:\n", matrixForDirected)
print()
print("Матриця суміжності ненапрямленого графа:\n", matrixForUndirected)

# Функція для нанесення номерів вузлів на полотно
def numbers():
    global NodePositions
    turtle.speed(0)  # Найшвидший режим анімації
    turtle.penup()
    turtle.goto(-300, 300)  # Початкова позиція для виведення номерів
    intCounting = 1
    vertSpacing = -120 * 1.2
    horizSpacing = 180 * 1.2

    # Для верхнього ряду вузлів
    for i in range(4):
        NodePositions.append(turtle.position())
        turtle.color("white")  # Колір тексту
        turtle.write(intCounting, align="center")  # Виведення номера вузла
        turtle.color("black")  # Повернення до чорного кольору
        intCounting += 1
        turtle.goto(turtle.xcor(), turtle.ycor() + vertSpacing)

    # Для правого стовпця вузлів
    for i in range(3):
        NodePositions.append(turtle.position())
        turtle.color("white")
        turtle.write(intCounting, align="center")
        turtle.color("black")
        intCounting += 1
        turtle.goto(turtle.xcor() + horizSpacing, turtle.ycor())

    # Для нижнього ряду вузлів
    for i in range(4):
        NodePositions.append(turtle.position())
        turtle.color("white")
        turtle.write(intCounting, align="center")
        turtle.color("black")
        intCounting += 1
        turtle.goto(turtle.xcor() - horizSpacing / 1.5, turtle.ycor() - vertSpacing)

    turtle.hideturtle()  # Приховання візка

radius = 16  # Радіус кола для візка

# Функція для малювання кола у вузлах
def circles():
    turtle.color('blue')
    turtle.speed(0)
    def circle(x, y):
        turtle.begin_fill()
        turtle.penup()
        turtle.goto(x, y - radius)
        turtle.pendown()
        turtle.circle(radius)
        turtle.end_fill()
    for pos in NodePositions: circle(pos[0], pos[1])

# Функція для визначення початкової позиції для малювання стрілки
def startPos(firstPosition, topPos):
    vector = (topPos - firstPosition)
    vector = vector / calcDistSize(firstPosition, topPos)
    return firstPosition + vector * radius

# Функція для обчислення відстані між двома точками
def calcDistSize(start, end):
    distSize = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
    return distSize

# Функція для отримання ортогонального вектора до вектора, заданого двома точками
def getOrto(x, y):
    orthVect = (-y, x)
    value = math.sqrt(orthVect[0] ** 2 + orthVect[1] ** 2)
    vectUnit = (orthVect[0] / value, orthVect[1] / value)
    return np.array(vectUnit)

# Функція для малювання стрілки між двома вузлами
def drawArrow(firstPosition, secondPosition, directed, k):
    firstPosition = np.array(firstPosition)
    secondPosition = np.array(secondPosition)
    vectorArrow = secondPosition - firstPosition
    mid = (secondPosition + firstPosition) / 2
    firstOrt = getOrto(*vectorArrow)
    koefOfDistance = k / calcDistSize(firstPosition, secondPosition) * 110
    side = 1 if koefOfDistance > 40 else -1
    firstOrt *= side
    topPos = mid + firstOrt * koefOfDistance + firstOrt * 40
    turtle.penup()
    startPosition = startPos(firstPosition, topPos)
    turtle.goto(startPosition[0], startPosition[1])
    turtle.pendown()
    turtle.goto(topPos[0], topPos[1])
    finalPosition = startPos(secondPosition, topPos)
    turtle.goto(finalPosition[0], finalPosition[1])
    turtle.penup()
    if directed: dirArrow(finalPosition, topPos, secondPosition)

# Функція для малювання напрямленої частини стрілки
def dirArrow(endPosition, topPosition, secondPosition):
    length = 14
    width = 14 / 2
    secondOrt = getOrto(*(topPosition - secondPosition))
    backVector = (topPosition - endPosition) / calcDistSize(topPosition, endPosition)
    a = endPosition + backVector * length
    turtle.goto(a + secondOrt * width)
    turtle.pendown()
    turtle.begin_fill()
    turtle.goto(endPosition)
    turtle.penup()
    turtle.goto(a - secondOrt * width)
    turtle.pendown()
    turtle.goto(endPosition)
    turtle.penup()
    turtle.goto(a - secondOrt * width)
    turtle.pendown()
    turtle.goto(a + secondOrt * width)
    turtle.end_fill()
    turtle.penup()

# Функція для малювання петлі навколо вузла
def samoloop(position, sizeOfTheLoop, directed):
    turtle.penup()
    turtle.goto(position[0], position[1] + radius)
    turtle.pendown()
    turtle.circle(sizeOfTheLoop)
    if directed:
        arrStartAng = 120  # Початковий кут для малювання стрілки петлі
        arrLen = 15  # Довжина стрілки
        arrWidth = 10  # Ширина стрілки
        arrPos_x = position[0] + sizeOfTheLoop * math.cos(math.radians(arrStartAng))
        arrPos_y = position[1] + 0.25 * radius + sizeOfTheLoop * math.sin(math.radians(arrStartAng))
        arrDirected_x = arrLen * math.cos(math.radians(arrStartAng + 190))
        arrDirected_y = arrLen * math.sin(math.radians(arrStartAng + 190))
        turtle.penup()
        turtle.goto(arrPos_x, arrPos_y)
        turtle.pendown()
        turtle.begin_fill()
        turtle.goto(arrPos_x + arrDirected_x, arrPos_y + arrDirected_y)
        turtle.goto(arrPos_x - arrWidth, arrPos_y - arrWidth)
        turtle.goto(arrPos_x, arrPos_y)
        turtle.end_fill()

# Виклик функцій для малювання номерів вузлів і кол на полотні
numbers()
circles()
numbers()

# Перебір усіх пар вузлів і малювання стрілок або петель

def Graph(isDir):
    for i in range(11):
        for j in range(i + 1):
            if matrixForUndirected[i][j]:
                if i == j:  # Якщо індекси однакові, це петля
                    samoloop(NodePositions[i], 30, isDir)
                else:
                    if i == 7: k = 350
                    elif i == 8 and 200 <= calcDistSize(NodePositions[i], NodePositions[j]) <= 280: k = 50
                    elif i > 8: k = 30
                    else: k = 120
                    drawArrow(NodePositions[i], NodePositions[j], directed=isDir, k=k)
Graph(True) #directed стає тру і граф напрямлений
time.sleep(4)
turtle.clear()
numbers()
circles()
numbers()

Graph(False) # навпаки
turtle.hideturtle()  # Приховання візка
turtle.done()  # Завершення роботи з turtle
