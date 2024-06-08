import numpy as np
import turtle
import time
import random
import math

radius = 16
random.seed(3214)
NodePositions = []
k = 1.0 - 1 * 0.01 - 4 * 0.005 - 0.15

matrix = [[random.uniform(0, 2) for j in range(11)] for i in range(11)]
matrixMultipliedBy_k = np.multiply(matrix, k)
matrixForDirected = np.floor(matrixMultipliedBy_k)
matrixForUndirected = np.maximum(matrixForDirected, np.transpose(matrixForDirected))
print("Матриця суміжності напрямленого графа:\n", matrixForDirected)

class GraphVisualizer:
    def __init__(self, node_positions, radius):
        self.node_positions = node_positions
        self.radius = radius

    def numbers(self):
        turtle.speed(0)
        turtle.penup()
        turtle.goto(-300, 300)
        intCounting = 1
        vertSpacing = -120 * 1.2
        horizSpacing = 180 * 1.2
        for i in range(4):
            self.node_positions.append(turtle.position())
            turtle.color("white")
            turtle.write(intCounting, align="center")
            turtle.color("black")
            intCounting += 1
            turtle.goto(turtle.xcor(), turtle.ycor() + vertSpacing)
        for i in range(3):
            self.node_positions.append(turtle.position())
            turtle.color("white")
            turtle.write(intCounting, align="center")
            turtle.color("black")
            intCounting += 1
            turtle.goto(turtle.xcor() + horizSpacing, turtle.ycor())
        for i in range(4):
            self.node_positions.append(turtle.position())
            turtle.color("white")
            turtle.write(intCounting, align="center")
            turtle.color("black")
            intCounting += 1
            turtle.goto(turtle.xcor() - horizSpacing / 1.5, turtle.ycor() - vertSpacing)
        turtle.hideturtle()

    def circles(self):
        turtle.color('blue')
        turtle.speed(0)
        def circle(x, y):
            turtle.begin_fill()
            turtle.penup()
            turtle.goto(x, y - self.radius)
            turtle.pendown()
            turtle.circle(self.radius)
            turtle.end_fill()
        for pos in self.node_positions: circle(pos[0], pos[1])

class GraphDrawer:
    def __init__(self, node_positions, radius):
        self.node_positions = node_positions
        self.radius = radius

    def startPos(self, firstPosition, topPos):
        vector = (topPos - firstPosition)
        vector = vector / self.calcDistSize(firstPosition, topPos)
        return firstPosition + vector * self.radius

    def calcDistSize(self, start, end):
        distSize = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
        return distSize

    def getOrto(self, x, y):
        orthVect = (-y, x)
        value = math.sqrt(orthVect[0] ** 2 + orthVect[1] ** 2)
        vectUnit = (orthVect[0] / value, orthVect[1] / value)
        return np.array(vectUnit)

    def drawArrow(self, firstPosition, secondPosition, directed, k, boolSearch):
        firstPosition = np.array(firstPosition)
        secondPosition = np.array(secondPosition)
        vectorArrow = secondPosition - firstPosition
        mid = (secondPosition + firstPosition) / 2
        firstOrt = self.getOrto(*vectorArrow)
        koefOfDistance = k / self.calcDistSize(firstPosition, secondPosition) * 110
        side = 1 if koefOfDistance > 40 else -1
        firstOrt *= side
        topPos = mid + firstOrt * koefOfDistance + firstOrt * 40
        turtle.penup()
        startPosition = self.startPos(firstPosition, topPos)
        turtle.goto(startPosition[0], startPosition[1])
        turtle.pendown()
        turtle.goto(topPos[0], topPos[1])
        finalPosition = self.startPos(secondPosition, topPos)
        turtle.goto(finalPosition[0], finalPosition[1])
        turtle.penup()
        if directed: self.dirArrow(finalPosition, topPos, secondPosition)
        if boolSearch:
            turtle.penup()
            turtle.goto(secondPosition[0], secondPosition[1] - self.radius)
            turtle.pendown()
            turtle.color("pink")
            turtle.begin_fill()
            turtle.circle(self.radius)
            turtle.end_fill()
            turtle.color("black")

    def dirArrow(self, endPosition, topPosition, secondPosition):
        length = 14
        width = length / 2
        secondOrt = self.getOrto(*(topPosition - secondPosition))
        backVector = (topPosition - endPosition) / self.calcDistSize(topPosition, endPosition)
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

    def samoloop(self, position, sizeOfTheLoop, directed):
        turtle.penup()
        turtle.goto(position[0], position[1] + self.radius)
        turtle.pendown()
        turtle.circle(sizeOfTheLoop)
        if directed:
            arrStartAng = 120
            arrLen = 15
            arrWidth = 10
            arrPos_x = position[0] + sizeOfTheLoop * math.cos(math.radians(arrStartAng))
            arrPos_y = position[1] + 0.25 * self.radius + sizeOfTheLoop * math.sin(math.radians(arrStartAng))
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

    def drawGraph(self, matrix, isDir):
        for i in range(11):
            for j in range(i + 1):
                if matrix[i][j]:
                    if i == j: self.samoloop(self.node_positions[i], 30, isDir)
                    else:
                        if i == 7: k = 350
                        elif i == 8 and 200 <= self.calcDistSize(self.node_positions[i], self.node_positions[j]) <= 280: k = 50
                        elif i > 8: k = 30
                        else: k = 120
                        self.drawArrow(self.node_positions[i], self.node_positions[j], directed=isDir, k=k, boolSearch=False)

class GraphSearch:
    def __init__(self, matrix, node_positions, radius=16):
        self.matrix = matrix
        self.node_positions = node_positions
        self.radius = radius
        self.drawer = GraphDrawer(node_positions, radius)

    def highlight_node(self, index, color="pink"):
        turtle.penup()
        turtle.goto(self.node_positions[index][0], self.node_positions[index][1] - self.radius)
        turtle.pendown()
        turtle.color(color)
        turtle.begin_fill()
        turtle.circle(self.radius)
        turtle.end_fill()
        turtle.color("black")

    def BREADTH_SEARCH(self):
        queue = []
        order = 1
        start = 0
        visited = [0] * len(self.matrix)
        search_matrix = [[0] * len(self.matrix) for _ in range(len(self.matrix))]
        self.highlight_node(start)
        while any(v == 0 for v in visited):
            visited[start] = order
            queue.append(start)
            while queue:
                node = queue.pop(0)
                for neighbor, connected in enumerate(self.matrix[node]):
                    if connected and not visited[neighbor]:
                        order += 1
                        visited[neighbor] = order
                        queue.append(neighbor)
                        search_matrix[node][neighbor] = 1
                        turtle.pencolor('orange')
                        self.drawer.drawArrow(self.node_positions[node], self.node_positions[neighbor], directed=True, k=120, boolSearch=True)
                        turtle.pencolor('orange')
                        time.sleep(1)
            if any(v == 0 for v in visited):
                start = visited.index(0)
                self.highlight_node(start)
        print("\nBFS order:")
        for i in range(len(visited)): print(visited[i], end=" ")
        print("\nBFS adjacency matrix:")
        for row in search_matrix: print(row)


    def DEPTH_SEARCH(self):
        stack = []
        order = 1
        start = 0
        visited = [0] * len(self.matrix)
        search_matrix = [[0] * len(self.matrix) for _ in range(len(self.matrix))]
        self.highlight_node(start)
        while any(v == 0 for v in visited):
            visited[start] = order
            stack.append(start)
            while stack:
                node = stack[-1]
                is_continue = False
                for neighbor, connected in enumerate(self.matrix[node]):
                    if connected and not visited[neighbor]:
                        order += 1
                        visited[neighbor] = order
                        stack.append(neighbor)
                        search_matrix[node][neighbor] = 1
                        turtle.pencolor('orange')
                        self.drawer.drawArrow(self.node_positions[node], self.node_positions[neighbor], directed=True, k=120, boolSearch=True)
                        turtle.pencolor('orange')
                        time.sleep(1)
                        is_continue = True
                        break
                if not is_continue: stack.pop()
            if any(v == 0 for v in visited):
                start = visited.index(0)
                self.highlight_node(start)
        print("\nDFS order:")
        for vertex in visited: print(vertex, end=" ")
        print("\nDFS adjacency matrix:")
        for row in search_matrix: print(row)

visualizer = GraphVisualizer(NodePositions, radius)
visualizer.numbers()
visualizer.circles()
visualizer.numbers()
graph_drawer = GraphDrawer(NodePositions, radius)
graph_drawer.drawGraph(matrixForUndirected, True)
graph_search = GraphSearch(matrixForUndirected, NodePositions)
graph_search.BREADTH_SEARCH()
visualizer.numbers()
time.sleep(2)
turtle.clear()
visualizer.numbers()
visualizer.circles()
graph_drawer.drawGraph(matrixForUndirected, True)
graph_search.DEPTH_SEARCH()
visualizer.numbers()
turtle.done()