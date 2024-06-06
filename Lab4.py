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
# turtle.done()  # Завершення роботи з turtle
def F_stepeniOfDirG(matrix):
    # Обчислення степенів напрямленого графа
    stepeni = [0] * len(matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] > 0: stepeni[i] += 1
    return stepeni

stepeniOfDirG = F_stepeniOfDirG(matrixForDirected)
print("Граф, степені напрямлених вершин:", stepeniOfDirG)

def F_stepeniOfUndirG(matrix):
    # Обчислення степенів ненапрямленого графа
    stepeni = [0] * len(matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] > 0: stepeni[i] += 1
    return stepeni
stepeniOfUndirG = F_stepeniOfUndirG(matrixForUndirected)
print("Граф, степені ненапрямлених вершин:", stepeniOfUndirG)


def F_outterStepeni(matrix):
    # Обчислення зовнішніх степенів
    outterStepeni = [0] * len(matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] > 0: outterStepeni[i] += 1
    return outterStepeni

def F_innerStepeni(matrix):
    # Обчислення внутрішніх степенів
    innerStepeni = [0] * len(matrix)
    for j in range(len(matrix)):
        for i in range(len(matrix)):
            if matrix[i][j] > 0: innerStepeni[j] += 1
    return innerStepeni
outterStepeni = F_outterStepeni(matrixForDirected)
innerStepeni = F_innerStepeni(matrixForDirected)

print("Граф, напівстепені виходу:", outterStepeni)
print("Граф, напівстепені заходу:", innerStepeni)

def odnorGraph(matrix):
    # Перевірка на однорідність графа
    stepeni = [sum(row) for row in matrix]
    if all(degree == stepeni[0] for degree in stepeni): return True, stepeni[0]
    else: return False, None

isOdnor, stepin = odnorGraph(matrixForDirected)
if isOdnor: print(f"Однорідний граф. Ступінь однорідності: {stepin}")
else: print("Неоднорідний.")


def pendAndIsolVert(matrix):
    # Визначення висячих та ізольованих вершин
    pendVert = []
    isolVert = []
    for i in range(len(matrix)):
        con = sum(1 for j in range(len(matrix[i])) if matrix[i][j] > 0)
        if con == 1: pendVert.append(i)
        elif con == 0: isolVert.append(i)
    return pendVert, isolVert

pendVert, isolVert = pendAndIsolVert(matrixForUndirected)
print("Ізольовані:", isolVert)
print("Висячі:", pendVert)

def shliah(matrix):
    # Знаходження шляхів
    sizeOfCont = len(matrix)
    shliahRoz2 = [[[] for _ in range(sizeOfCont)] for _ in range(sizeOfCont)]
    shliahRoz3 = [[[] for _ in range(sizeOfCont)] for _ in range(sizeOfCont)]

    for i in range(sizeOfCont):
        for j in range(sizeOfCont):
            for k in range(sizeOfCont):
                if matrix[i][k] > 0 and matrix[k][j] > 0: shliahRoz2[i][j].append([i, k, j])

    for i in range(sizeOfCont):
        for j in range(sizeOfCont):
            for path in shliahRoz2[i][j]:
                for k in range(sizeOfCont):
                    if matrix[j][k] > 0: shliahRoz3[i][k].append(path + [k])

    return shliahRoz2, shliahRoz3

matrix = matrixForDirected

shliahRoz2 = shliah(matrix)
shliahRoz3 = shliah(matrix)

print("Шляхи, довжина 2:")
for i in range(len(shliahRoz2)):
    for j in range(len(shliahRoz2[i])):
        if shliahRoz2[i][j]: print(f"Шляхи від {i + 1} до {j + 1}: {shliahRoz2[i][j]}")

print("\nШляхи, довжина 3:")
for i in range(len(shliahRoz3)):
    for j in range(len(shliahRoz3[i])):
        if shliahRoz3[i][j]: print(f"Шляхи від {i + 1} до {j + 1}: {shliahRoz3[i][j]}")

def reachAndCon_M(matrix):
    # Обчислення досяжності та сильної зв'язності
    intN = len(matrix)
    matrixOdynych = [[1 if i == j else 0 for j in range(intN)] for i in range(intN)]
    matrixKvadr = np.linalg.matrix_power(matrix, 2)
    matrixCubich = np.linalg.matrix_power(matrix, 3)
    matrixTetr = np.linalg.matrix_power(matrix, 4)
    resultOfSum = resOfSum_M(resOfSum_M(resOfSum_M(resOfSum_M(matrixOdynych, matrix), matrixKvadr), matrixCubich), matrixTetr)
    matrixRea = [[1 if resultOfSum[i][j] != 0 else 0 for j in range(intN)] for i in range(intN)]
    matrixTrans = matrixTransposing(matrixRea)
    matrixCon = prodOfEl(matrixRea, matrixTrans)
    return matrixRea, matrixCon

def resOfSum_M(matrix1, matrix2): return [[matrix1[i][j] + matrix2[i][j] for j in range(len(matrix1[0]))] for i in range(len(matrix1))]
def matrixTransposing(matr): return [[matr[j][i] for j in range(len(matr))] for i in range(len(matr))]
def prodOfEl(matrix1, matrix2): return [[matrix1[i][j] * matrix2[i][j] for j in range(len(matrix1[0]))] for i in range(len(matrix1))]
def getComps(matrixCon):
    compUni = set(tuple(row) for row in matrixCon)
    compCon = []
    for component in compUni:
        ind = [i + 1 for i, row in enumerate(matrixCon) if tuple(row) == component]
        compCon.append(ind)
    return compCon

def condensGraph(compS):
    # Малювання конденсованого графа
    turtle.color('blue')
    turtle.speed(1)
    turtle.clear()
    intComps = len(compS)
    stepKuta = 360 / intComps
    radius2 = 200
    for i, component in enumerate(compS):
        kut = stepKuta * i
        x = radius2 * math.cos(math.radians(kut))
        y = radius2 * math.sin(math.radians(kut))
        turtle.up()
        turtle.goto(x, y)
        turtle.down()
        turtle.circle(40)
        turtle.up()
        turtle.goto(x, y + 15)
        turtle.write(f"{i + 1}", False, 'center', ('Century gothic', 20, 'normal'))

    turtle.done()

justGraph = matrixForDirected
matrixRea, matrixCon = reachAndCon_M(justGraph)

def matrix(matrix, innerInf):
    print(innerInf)
    for stovp in matrix: print(stovp)


matrixRea, matrixCon = reachAndCon_M(justGraph)
matrix(matrixRea, "Матриця досяжності:")
matrix(matrixCon, "Матриця сильної зв'язності:")

compS = getComps(matrixCon)
print("Компоненти:" ,compS)
condensGraph(compS)
