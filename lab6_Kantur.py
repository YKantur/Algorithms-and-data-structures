import turtle
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random
import math

random.seed(3214)
NodePositions = []
nodes = 11
radius = 16
k = 1.0 - 1 * 0.01 - 4 * 0.005 - 0.05
def roundingUpper(x): return np.ceil(x * 100)

matrix = [[random.uniform(0, 2) for j in range(11)] for i in range(11)]
matrixMultipliedBy_k = np.multiply(matrix, k)
matrixForDirected = np.floor(matrixMultipliedBy_k)
matrixForUndirected = np.maximum(matrixForDirected, np.transpose(matrixForDirected))
matrix1 = np.ones((nodes, nodes))
matrix2 = np.random.uniform(0, 2.0, (nodes, nodes))
matrix3 = np.ceil(matrix2 * 100 * matrix1).astype(int)
matrix4 = np.where(matrix3 > 0, 1, 0)
matrix5 = np.where(matrix4 == matrix4.T, 1, 0)
matrixTransposed = np.triu(np.ones((nodes, nodes)), k = 1)
matrixOfWeights = (matrix4 * matrix5 * matrixTransposed + matrix3)
matrixOfWeights = np.maximum(matrixOfWeights, matrixOfWeights.T)
matrices = [matrix2, matrix3, matrix4, matrix5, matrixTransposed, matrixOfWeights]
print("Матриця суміжності ненапрямленого графа:\n", matrixForUndirected)

def print_matrices(matrices):
    for i, matrix in enumerate(matrices, start = 1): print(f"Matrix {i}:\n{matrix}")
print_matrices(matrices)

def MINSPANTREE_kr(weightOfMatrix):
    ourGRAPH = nx.Graph()
    for i in range(len(weightOfMatrix)):
        for ii in range(i + 1, len(weightOfMatrix)):
            if weightOfMatrix[i][ii] > 0: ourGRAPH.add_edge(i, ii, weight = weightOfMatrix[i][ii])
    MINSPANTREE = nx.minimum_spanning_tree(ourGRAPH, algorithm = 'kruskal')
    return MINSPANTREE
KRUSKALLED_MST = MINSPANTREE_kr(matrixOfWeights)
print("\nМатриця зв'язного дерева за Краскалом:\n", sorted(KRUSKALLED_MST.edges(data=True)))

ourGRAPH = nx.Graph()
for i in range(nodes):
    for ii in range(i + 1, nodes):
        if matrixOfWeights[i][ii] > 0: ourGRAPH.add_edge(i, ii, weight=matrixOfWeights[i][ii])

def numbers():
    global NodePositions
    turtle.speed(0)
    turtle.penup()
    turtle.goto(-300, 300)
    intCounting = 1
    vertSpacing = -120 * 1.2
    horizSpacing = 180 * 1.2
    for i in range(4):
        NodePositions.append(turtle.position())
        turtle.color("white")
        turtle.write(intCounting, align="center")
        turtle.color("black")
        intCounting += 1
        turtle.goto(turtle.xcor(), turtle.ycor() + vertSpacing)
    for i in range(3):
        NodePositions.append(turtle.position())
        turtle.color("white")
        turtle.write(intCounting, align="center")
        turtle.color("black")
        intCounting += 1
        turtle.goto(turtle.xcor() + horizSpacing, turtle.ycor())
    for i in range(4):
        NodePositions.append(turtle.position())
        turtle.color("white")
        turtle.write(intCounting, align="center")
        turtle.color("black")
        intCounting += 1
        turtle.goto(turtle.xcor() - horizSpacing / 1.5, turtle.ycor() - vertSpacing)
    turtle.hideturtle()

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

def startPos(firstPosition, topPos):
    vector = (topPos - firstPosition)
    vector = vector / calcDistSize(firstPosition, topPos)
    return firstPosition + vector * radius

def calcDistSize(start, end):
    distSize = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
    return distSize

def getOrto(x, y):
    orthVect = (-y, x)
    value = math.sqrt(orthVect[0] ** 2 + orthVect[1] ** 2)
    vectUnit = (orthVect[0] / value, orthVect[1] / value)
    return np.array(vectUnit)

def drawArrow(boolsaerch, firstPosition, secondPosition, k, weight = None):
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
    if weight is not None:
        wagPosition = finalPosition + (startPosition - finalPosition) * 0.2
        turtle.penup()
        turtle.goto(wagPosition[0], wagPosition[1])
        turtle.pendown()
        turtle.write(f'{weight:.1f}', align="center", font=("Century gothic", 10, "normal"))
    if boolsaerch:
        turtle.penup()
        turtle.goto(secondPosition[0], secondPosition[1] - radius)
        turtle.pendown()
        turtle.begin_fill()
        turtle.circle(radius)
        turtle.end_fill()

def dirArrow(endPosition, topPosition, secondPosition):
    length = 14
    width = length / 2
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

def samoloop(position, sizeOfTheLoop):
    turtle.penup()
    turtle.goto(position[0], position[1] + radius)
    turtle.pendown()
    turtle.circle(sizeOfTheLoop)

def Graph():
    for i in range(11):
        for ii in range(i + 1):
            weight = 0
            if matrixForUndirected[i][ii]: weight = matrixOfWeights[i][ii]
            if i == ii and weight: samoloop(NodePositions[i], 30)
            else:
                if i == 7: k = 350
                elif i == 8 and 200 <= calcDistSize(NodePositions[i], NodePositions[ii]) <= 280: k = 50
                elif i > 8: k = 30
                else: k = 120
                if weight: drawArrow(False, NodePositions[i], NodePositions[ii], k, weight)
numbers()
circles()
numbers()
Graph()

def MINSPANTREEfun(minspantreeValueOf):
    plt.figure(figsize=(7, 7))
    edge_labels = nx.get_edge_attributes(minspantreeValueOf, 'weight')
    locs = {
        i:NodePositions[i] for i in range(nodes)
    }
    nx.draw(minspantreeValueOf, locs, with_labels=True, node_color='pink', edge_color='purple', node_size=380, font_size=15)
    nx.draw_networkx_edge_labels(minspantreeValueOf, locs, edge_labels=edge_labels)
    plt.title("\nМатриця зв'язного дерева за Краскалом")
    plt.show()
MINSPANTREEfun(KRUSKALLED_MST)

def MINSPANTREE_CalcWeights(minspantreeValueOf):
    weights = sum(data['weight'] for i, ii, data in minspantreeValueOf.edges(data=True))
    return weights
MINSPANTREE_WEIGHT_KR = MINSPANTREE_CalcWeights(KRUSKALLED_MST)
print("\nВага МЗТ:",  MINSPANTREE_WEIGHT_KR)
turtle.exitonclick() #старийбог52


































































































