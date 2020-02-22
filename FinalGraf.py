import math
import tkinter as tk
import myMatrix
import heapq
import shapes
import time

class Graph(tk.Frame):
    WIDTH = 640.0
    HEIGHT = 640.0

    RATE = 2
    SPEED = 3

    ZOOMRATE = 2
    ZOOMSPEED = 3

    GRAPH_COLOR = '#eaeaea'

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.__Graph = tk.Canvas(self, width=Graph.WIDTH, height=Graph.HEIGHT, bg='white')
        self.__Graph.pack()
        self.pack()
        self.__Parent = parent
        # Axes of graph in the middle

        self.__SceneChange = True
        self.__CordsSys = [
            myMatrix.Vector3D(0.0, 0.0, 0.0),  # Origin
            myMatrix.Vector3D(1, 0.0, 0.0),  # X
            myMatrix.Vector3D(0.0, 1, 0.0),  # Y
            myMatrix.Vector3D(0.0, 0.0, 1)  # Z
        ]

        self.__GraphCube = [
            myMatrix.Vector3D(-1, 1, -1),
            myMatrix.Vector3D(1, 1, -1),
            myMatrix.Vector3D(1, -1, -1),
            myMatrix.Vector3D(-1, -1, -1),
            myMatrix.Vector3D(-1, 1, 1),
            myMatrix.Vector3D(1, 1, 1),
            myMatrix.Vector3D(1, -1, 1),
            myMatrix.Vector3D(-1, -1, 1)
        ]

        self.__AxisNumbersPosition = [
            [
                [myMatrix.Vector3D(-0.8, -1, -1), myMatrix.Vector3D(-0.8, -1, 1)],
                [myMatrix.Vector3D(-0.6, -1, -1), myMatrix.Vector3D(-0.6, -1, 1)],
                [myMatrix.Vector3D(-0.4, -1, -1), myMatrix.Vector3D(-0.4, -1, 1)],
                [myMatrix.Vector3D(-0.2, -1, -1), myMatrix.Vector3D(-0.2, -1, 1)],
                [myMatrix.Vector3D(0, -1, -1), myMatrix.Vector3D(0, -1, 1)],
                [myMatrix.Vector3D(0.2, -1, -1), myMatrix.Vector3D(0.2, -1, 1)],
                [myMatrix.Vector3D(0.4, -1, -1), myMatrix.Vector3D(0.4, -1, 1)],
                [myMatrix.Vector3D(0.6, -1, -1), myMatrix.Vector3D(0.6, -1, 1)],
                [myMatrix.Vector3D(0.8, -1, -1), myMatrix.Vector3D(0.8, -1, 1)],
            ],
            [
                [myMatrix.Vector3D(-1, -0.8, -1), myMatrix.Vector3D(-1, -0.8, 1)],
                [myMatrix.Vector3D(-1, -0.6, -1), myMatrix.Vector3D(-1, -0.6, 1)],
                [myMatrix.Vector3D(-1, -0.4, -1), myMatrix.Vector3D(-1, -0.4, 1)],
                [myMatrix.Vector3D(-1, -0.2, -1), myMatrix.Vector3D(-1, -0.2, 1)],
                [myMatrix.Vector3D(-1, 0, -1), myMatrix.Vector3D(-1, 0, 1)],
                [myMatrix.Vector3D(-1, 0.2, -1), myMatrix.Vector3D(-1, 0.2, 1)],
                [myMatrix.Vector3D(-1, 0.4, -1), myMatrix.Vector3D(-1, 0.4, 1)],
                [myMatrix.Vector3D(-1, 0.6, -1), myMatrix.Vector3D(-1, 0.6, 1)],
                [myMatrix.Vector3D(-1, 0.8, -1), myMatrix.Vector3D(-1, 0.8, 1)],
            ],
            [
                [myMatrix.Vector3D(1, -1, -0.8), myMatrix.Vector3D(-1, -1, -0.8)],
                [myMatrix.Vector3D(1, -1, -0.6), myMatrix.Vector3D(-1, -1, -0.6)],
                [myMatrix.Vector3D(1, -1, -0.4), myMatrix.Vector3D(-1, -1, -0.4)],
                [myMatrix.Vector3D(1, -1, -0.2), myMatrix.Vector3D(-1, -1, -0.2)],
                [myMatrix.Vector3D(1, -1, 0), myMatrix.Vector3D(-1, -1, 0)],
                [myMatrix.Vector3D(1, -1, 0.2), myMatrix.Vector3D(-1, -1, 0.2)],
                [myMatrix.Vector3D(1, -1, 0.4), myMatrix.Vector3D(-1, -1, 0.4)],
                [myMatrix.Vector3D(1, -1, 0.6), myMatrix.Vector3D(-1, -1, 0.6)],
                [myMatrix.Vector3D(1, -1, 0.8), myMatrix.Vector3D(-1, -1, 0.8)],
            ],
        ]

        self.__AxisEdges = [
            [
                [2, 3],
                [6, 7],
                [0, 1],
                [4, 5]
            ],
            [
                [0, 3],
                [4, 7],
                [1, 2],
                [5, 6]
            ],
            [
                [6, 2],
                [3, 7],
                [1, 5],
                [0, 4],
            ],
        ]

        self.__FacesMid = [
            myMatrix.Vector3D(0.0, 0.0, -1.0),
            myMatrix.Vector3D(1.0, 0.0, 0.0),
            myMatrix.Vector3D(0.0, 0.0, 1.0),
            myMatrix.Vector3D(-1.0, 0.0, 0.0),
            myMatrix.Vector3D(0.0, 1.0, 0.0),
            myMatrix.Vector3D(0.0, -1.0, 0.0),
        ]

        #self.dotz = myMatrix.Vector3D(1, 0, 0)

        self.__Points = [
            shapes.Point(5, -1.0, 1.0),
            shapes.Point(4, -1.0, 1.0,),
            shapes.Point(3, -1.0, 1.0),
            shapes.Point(2, -1.0, 1.0),
            shapes.Point(1, -1.0, 1.0, '#00ff00'),
            shapes.Point(0.0, -1.0, 1.0),
            shapes.Point(-1, -1.0, 1.0),
            shapes.Point(-2, -1.0, 1.0, '0000ff'),
            shapes.Point(-3, -1.0, 1.0),
            shapes.Point(-4, -1.0, 1.0),
            shapes.Point(-5, -1.0, 1.0),
        ]

        self.Polygons = [
            shapes.Polygon(0, 0, 0, 2, -1, 2, 15, 15, 15)
        ]

        self.PolyGonePeaks = [
            myMatrix.Vector3D(0, 0, 0),
            myMatrix.Vector3D(0, 1, 0),
            myMatrix.Vector3D(-2, 1, 0),
            myMatrix.Vector3D(-1, 0, 0),
            myMatrix.Vector3D(-1, 0, -1),
            myMatrix.Vector3D(-1, 2, -1),
            myMatrix.Vector3D(0, 1, -1),
            myMatrix.Vector3D(0, 0, -1),
        ]

        self.PoygonEdges = [
            [0, 3],
            [0, 1],
            [0, 7],
            [1, 2],
            [3, 2],
            [3, 4],
            [4, 5],
            [4, 7],
            [5, 6],
            [5, 2],
            [6, 7],
            [6, 1],
        ]
        # Steny kociek s cislami vrcholov
        self.__CubeFaces = [
            [0, 1, 2, 3],
            [1, 5, 6, 2],
            [5, 4, 7, 6],
            [4, 0, 3, 7],
            [0, 4, 5, 1],
            [3, 2, 6, 7]
        ]

        #self.__Points = [
         #   myMatrix.Vector3D(1.0, 1, 1),
        #]

        self.__Show = [0, 0, 0]
        self.__LabelCords = []

        # Uhly ktore sa pouzivaju pri rotaciach

        self.__RotationMatX = myMatrix.Matrix(4, 4)

        self.__RotationMatY = myMatrix.Matrix(4, 4)

        self.__RotationMatZ = myMatrix.Matrix(4, 4)

        self.__Rot = myMatrix.Matrix(4, 4)

        self.__Angles = [15.0, 45.0, 0.0]
        self.rotationUpdate()

        # Translation matrix, na posun kamery
        self.m_TranslationCam = [0.0, 0.0, 0.0]

        # Zvacsovnaie
        scaleX = 0.5
        scaleY = 0.5
        scaleZ = 0.5
        self.__Scale = myMatrix.Matrix(4, 4)
        self.__Scale[(0, 0)] = scaleX
        self.__Scale[(1, 1)] = scaleY
        self.__Scale[(2, 2)] = scaleZ

        self.__Tsf = myMatrix.Matrix(4, 4)

        # self.Tr = myMatrix.Matrix(4, 4)
        # self.Tr[(0, 3)] = 2

        self.__InnerTranslation = [0, 0, 0]

        self.__InnerTsf = myMatrix.Matrix(4, 4)
        self.__InnerTsf[(0, 0)] = 1
        self.__InnerTsf[(1, 1)] = 1
        self.__InnerTsf[(2, 2)] = 1
        self.__InnerTsf[(0, 3)] = self.__InnerTranslation[0]
        self.__InnerTsf[(1, 3)] = self.__InnerTranslation[1]
        self.__InnerTsf[(2, 3)] = self.__InnerTranslation[2]

        self.__BaseScaledNumber = []
        self.m_OutterStartPosition = [0, 0, 0]
        for i in range(3):
            self.__BaseScaledNumber.append([])
            lastNum = -0.8
            for j in range(9):
                self.__BaseScaledNumber[i].append(round(lastNum - self.m_OutterStartPosition[i] * 0.8, 2) / self.__InnerTsf[i, i])
                lastNum += 0.2

        self.__Projection = myMatrix.Matrix(4, 4)

        # self.__Projection[(2, 3)] = -1.0
        # self.__Projection[(3, 3)] = 0.0
        # self.__Projection[(3, 2)] = -0.5

        fov = 90.0  # between 30 and 90 ?
        zfar = 100.0
        znear = 0.1
        S = 1 / (math.tan(math.radians(fov / 2)))
        # 1st version (Perspective __Projection)
        self.__Projection[(0, 0)] = S
        self.__Projection[(1, 1)] = S
        self.__Projection[(2, 2)] = -zfar / (zfar - znear)
        self.__Projection[(3, 2)] = -0.05
        # self.Proj[(2, 3)] = -(zfar * znear) / (zfar - znear)

        self.lctrl_pressed = False

        self.__Graph.bind("<B1-Motion>", self.dragcallback)
        self.__Graph.bind("<ButtonRelease-1>", self.releasecallback)

        self.__Graph.bind("<B3-Motion>", self.dragcallbackRight)
        self.__Graph.bind("<ButtonRelease-3>", self.releasecallbackRight)

        # self.__Graph.bind_all("<d>", self.move)
        self.__LabelAngle = [0.0, 0.0, 0.0]
        self.cnt = Graph.RATE
        self.cntRight = Graph.RATE
        self.prevmouseX = 0.0
        self.prevmouseY = 0.0
        self.previousTmpScale = [self.__InnerTsf[0, 0], self.__InnerTsf[1, 1], self.__InnerTsf[2, 2]]
        self.prevmouseYright = 0.0
        self.__ScaleFactor = 1.02

        for i in range(3):
            self.updateAxisNumberPositions(i, 1)

        self.numerifyAxis()
        self.outterTransformationMatrixUpdate()
        time_st = time.time()
        time.sleep(1)
        print(time.time() - time_st)
        self.update()


    def updateAxisNumberPositions(self, dim, koeficient, multiply=True):
        if multiply:
            for i in range(len(self.__BaseScaledNumber[dim])):
                self.__BaseScaledNumber[dim][i] *= koeficient
                self.__AxisNumbersPosition[dim][i][0].values[dim] = self.__BaseScaledNumber[dim][i] + self.__InnerTsf[(dim, 3)]
                self.__AxisNumbersPosition[dim][i][1].values[dim] = self.__BaseScaledNumber[dim][i] + self.__InnerTsf[(dim, 3)]
        else:
            for i in range(len(self.__BaseScaledNumber[dim])):
                self.__BaseScaledNumber[dim][i] /= koeficient
                self.__AxisNumbersPosition[dim][i][0].values[dim] = self.__BaseScaledNumber[dim][i] + self.__InnerTsf[(dim, 3)]
                self.__AxisNumbersPosition[dim][i][1].values[dim] = self.__BaseScaledNumber[dim][i] + self.__InnerTsf[(dim, 3)]

    def move(self, event):
        self.__InnerTranslation[0] += 1
        self.innerTransformationMatrixUpdate()

    def drawGraphCubeWall(self):
        self.__Show = [0, 0, 0]
        listOfFaces = []
        # tstovanie stien
        transformedPoint1 = self.__Tsf * self.__FacesMid[2]
        transformedPoint2 = self.__Tsf * self.__FacesMid[0]
        if transformedPoint1.values[2] <= transformedPoint2.values[2]:
            listOfFaces.append(2)
        else:
            listOfFaces.append(0)
            self.__Show[0] += 1
            self.__Show[1] += 1
        transformedPoint1 = self.__Tsf * self.__FacesMid[3]
        transformedPoint2 = self.__Tsf * self.__FacesMid[1]
        if transformedPoint1.values[2] <= transformedPoint2.values[2]:
            listOfFaces.append(3)
        else:
            listOfFaces.append(1)
            self.__Show[1] += 2
            self.__Show[2] += 1
        transformedPoint1 = self.__Tsf * self.__FacesMid[5]
        transformedPoint2 = self.__Tsf * self.__FacesMid[4]
        if transformedPoint1.values[2] <= transformedPoint2.values[2]:
            listOfFaces.append(5)
        else:
            listOfFaces.append(4)
            self.__Show[0] += 2
            self.__Show[2] += 2

        # print('ShowX: {}  ShowY: {}  ShowZ: {}'.format(show[0], show[1], show[2]))
        for faceNumber in listOfFaces:
            inviewvingvolume = False
            poly = []
            for peak in range(len(self.__CubeFaces[faceNumber])):
                peakPositionVector = self.__GraphCube[self.__CubeFaces[faceNumber][peak]]
                # Vlozenie bodu obrazovky do listu transformovanych vrcholov
                screenProjectionCords = self.outterPointToScreen(peakPositionVector)
                x = int(screenProjectionCords.values[0])
                y = int(screenProjectionCords.values[1])
                poly.append((x, y))

                # Ak je aspon jedene vrchol vo viditelnej oblasti, vykresli cely polygon
                # if (-1.0 <= ps.values[0] < 1.0) and (-1.0 <= ps.values[1] < 1.0) and (-1.0 <= ps.values[2] < 1.0):
                inviewvingvolume = True

            self.__Graph.create_polygon(poly[0][0], poly[0][1], poly[1][0], poly[1][1], poly[2][0], poly[2][1],
                                          poly[3][0], poly[3][1], fill=Graph.GRAPH_COLOR)
            for k in range(len(poly) - 1):
                self.__Graph.create_line(poly[k][0], poly[k][1], poly[k + 1][0], poly[k + 1][1], fill='white')
                self.__Graph.create_line(poly[len(poly) - 1][0], poly[len(poly) - 1][1], poly[0][0], poly[0][1],
                                       fill='white')

    def drawGraphCubeAxis(self):
        labels = ['Label X', 'Label Y', 'Label Z']
        self.__LabelCords = []
        lineAndLabelCords = []
        for axeFace in range(3):
            edgeNodeVector0 = self.__GraphCube[self.__AxisEdges[axeFace][self.__Show[axeFace]][0]]
            edgeNodeVector1 = self.__GraphCube[self.__AxisEdges[axeFace][self.__Show[axeFace]][1]]
            transformedPointVector0 = self.__Tsf * edgeNodeVector0
            transformedPointVector1 = self.__Tsf * edgeNodeVector1
            projectedPointVector0 = self.__Projection * transformedPointVector0
            projectedPointVector1 = self.__Projection * transformedPointVector1
            screenProjectionCords0 = self.toScreenCords(projectedPointVector0)
            screenProjectionCords1 = self.toScreenCords(projectedPointVector1)

            self.__LabelAngle[axeFace] = math.degrees(
                math.acos(math.fabs(projectedPointVector0[0] - projectedPointVector1[0]) / math.sqrt(
                    math.fabs(projectedPointVector0[0] - projectedPointVector1[0]) ** 2 + math.fabs(
                        projectedPointVector0[1] - projectedPointVector1[1]) ** 2)))

            # print('{}: {} {} {}'.format(labels[cord], self.__Angles[0], self.__Angles[1], self.__LabelAngle[cord]))
            if self.__Angles[0] < 180:
                if self.__Angles[1] > 270:
                    if axeFace != 2:
                        self.__LabelAngle[axeFace] = 360 - self.__LabelAngle[axeFace]
                elif self.__Angles[1] > 180:
                    if axeFace == 2:
                        self.__LabelAngle[axeFace] = 360 - self.__LabelAngle[axeFace]
                elif self.__Angles[1] > 90:
                    if axeFace != 2:
                        self.__LabelAngle[axeFace] = 360 - self.__LabelAngle[axeFace]
                elif self.__Angles[1] >= 0.0:
                    if axeFace == 2:
                        self.__LabelAngle[axeFace] = 360 - self.__LabelAngle[axeFace]

            else:
                if self.__Angles[1] <= 90:
                    self.__LabelAngle[axeFace] = 360 - self.__LabelAngle[axeFace]
                if 180 <= self.__Angles[1] <= 270:
                    if axeFace != 2:
                        self.__LabelAngle[axeFace] = 360 - self.__LabelAngle[axeFace]
                elif axeFace == 2:
                    self.__LabelAngle[axeFace] = 360 - self.__LabelAngle[axeFace]

            distance = 1.2
            if self.__Show[axeFace] < 2:
                if self.__Show[axeFace] < 1:
                    if axeFace != 2:
                        self.__LabelCords.append(myMatrix.Vector3D(-distance, -distance, -distance))
                    else:
                        self.__LabelCords.append(myMatrix.Vector3D(distance, -distance, -distance))
                    self.__LabelCords[axeFace].values[axeFace] = 0
                else:
                    self.__LabelCords.append(myMatrix.Vector3D(-distance, -distance, distance))
                    self.__LabelCords[axeFace].values[axeFace] = 0
            else:
                if self.__Show[axeFace] < 3:
                    if axeFace != 2:
                        self.__LabelCords.append(myMatrix.Vector3D(distance, distance, -distance))
                    else:
                        self.__LabelCords.append(myMatrix.Vector3D(distance, distance, -distance))
                    self.__LabelCords[axeFace].values[axeFace] = 0
                else:
                    if axeFace != 2:
                        self.__LabelCords.append(myMatrix.Vector3D(distance, distance, distance))
                    else:
                        self.__LabelCords.append(myMatrix.Vector3D(-distance, distance, distance))
                    self.__LabelCords[axeFace].values[axeFace] = 0

            self.drawGraphAxisNumberAndLines(axeFace)
            screenProjectionCords = self.outterPointToScreen(self.__LabelCords[axeFace])
            lineAndLabelCords.append([screenProjectionCords0, screenProjectionCords1, screenProjectionCords])

        # aby neboli prekryte osy sivymi ciarami
        for i in range(3):
            self.__Graph.create_line(lineAndLabelCords[i][0].values[0], lineAndLabelCords[i][0].values[1],
                                   lineAndLabelCords[i][1].values[0], lineAndLabelCords[i][1].values[1], fill='black')
            self.__Graph.create_text(lineAndLabelCords[i][2].values[0], lineAndLabelCords[i][2].values[1], fill='black',
                                   text=labels[i],
                                   angle=self.__LabelAngle[i])

    def drawGraphAxisNumberAndLines(self, axeFace):
        nlLength = 0.03
        changeVector0 = myMatrix.Vector3D(1, 1, 1, 1)
        changeVector1 = myMatrix.Vector3D(1, 1, 1, 1)
        if self.__Show[axeFace] < 2:
            if self.__Show[axeFace] > 0:
                if axeFace == 0:
                    changeVector0.values[2] = -1
                    changeVector1.values[2] = -1
                elif axeFace == 1:
                    changeVector0.values[2] = -1
                    changeVector1.values[2] = -1
                elif axeFace == 2:
                    changeVector0.values[0] = -1
                    changeVector1.values[0] = -1
        else:
            if self.__Show[axeFace] < 3:
                if axeFace == 0:
                    changeVector0.values[1] = -1
                    changeVector1.values[1] = -1
                elif axeFace == 1:
                    changeVector0.values[0] = -1
                    changeVector1.values[0] = -1
                elif axeFace == 2:
                    changeVector0.values[1] = -1
                    changeVector1.values[1] = -1
            else:
                if axeFace == 0:
                    changeVector0.values[1] = -1
                    changeVector0.values[2] = -1
                    changeVector1.values[1] = -1
                    changeVector1.values[2] = -1
                elif axeFace == 1:
                    changeVector0.values[0] = -1
                    changeVector0.values[2] = -1
                    changeVector1.values[0] = -1
                    changeVector1.values[2] = -1
                elif axeFace == 2:
                    changeVector0.values[0] = -1
                    changeVector0.values[1] = -1
                    changeVector1.values[0] = -1
                    changeVector1.values[1] = -1
        for perpenLinePointsVectorTuple in self.__AxisNumbersPosition[axeFace]:
            lineStartPointVector = self.innerCordsToOutter(perpenLinePointsVectorTuple[0] * changeVector0, axeFace)
            if not (math.fabs(lineStartPointVector.values[0]) - 1 <= 0.000001) or not (
                    math.fabs(lineStartPointVector.values[1]) - 1 <= 0.000001) or not (
                    math.fabs(lineStartPointVector.values[2]) - 1 <= 0.000001):
                continue

            p1 = self.outterPointToScreen(lineStartPointVector)

            # druhy bod dlhej ciary
            lineEndPointVector = self.innerCordsToOutter(perpenLinePointsVectorTuple[1] * changeVector1, axeFace)
            p2 = self.outterPointToScreen(lineEndPointVector)
            # vykreslenie dlhej ciary
            self.__Graph.create_line(p1[0], p1[1], p2[0], p2[1], fill='gray')

            # kolma ciara
            perpendicularEndPointVector = perpenLinePointsVectorTuple[1] * changeVector1
            perpendicularEndPointVector.values[(axeFace + 1) % 2] *= -1

            perpendicularEndPointVector = self.innerCordsToOutter(perpendicularEndPointVector, axeFace)
            p1 = self.outterPointToScreen(perpendicularEndPointVector)
            self.__Graph.create_line(p2[0], p2[1], p1[0], p1[1], fill='gray')

            # ciarka na ciselenj osy
            axeMarkStartPointVector = self.innerCordsToOutter(perpenLinePointsVectorTuple[0] * changeVector0, axeFace)
            if axeFace != 2:
                axeMarkStartPointVector.values[2] = perpenLinePointsVectorTuple[0][2] * changeVector0[2] + nlLength
            else:
                axeMarkStartPointVector.values[0] = perpenLinePointsVectorTuple[0][0] * changeVector0[0] + nlLength

            p1 = self.outterPointToScreen(axeMarkStartPointVector)

            # dalsi bod
            axeMarkEndPointVector = self.innerCordsToOutter(perpenLinePointsVectorTuple[0] * changeVector0, axeFace)
            if axeFace != 2:
                axeMarkEndPointVector.values[2] = perpenLinePointsVectorTuple[0][2] * changeVector0[2] - nlLength
            else:
                axeMarkEndPointVector.values[0] = perpenLinePointsVectorTuple[0][0] * changeVector0[0] - nlLength

            p2 = self.outterPointToScreen(axeMarkEndPointVector)

            self.__Graph.create_line(p1[0], p1[1], p2[0], p2[1],fill='black')

            numberPositionVector = self.innerCordsToOutter(perpenLinePointsVectorTuple[0] * changeVector0, axeFace)
            for cord in range(3):
                if cord != axeFace:
                    if self.__LabelCords[axeFace].values[cord] < 0:
                        numberPositionVector.values[cord] = self.__LabelCords[axeFace].values[cord] + (
                                math.fabs(self.__LabelCords[axeFace].values[cord]) - 1) / 2
                    else:
                        numberPositionVector.values[cord] = self.__LabelCords[axeFace].values[cord] - (
                                math.fabs(self.__LabelCords[axeFace].values[cord]) - 1) / 2

            p1 = self.outterPointToScreen(numberPositionVector)
            self.__Graph.create_text(p1[0], p1[1],text=round(perpenLinePointsVectorTuple[0].values[axeFace], 3))

    def innerCordsToOutter(self, p, axe=-1):
        if axe < 0:
            r = myMatrix.Vector3D()
            for i in range(3):
                r.values[i] = (p[i] - self.__InnerTsf[(i, 3)]) * self.__InnerTsf[(i, i)]
                r.values[i] += self.m_OutterStartPosition[i]
            return r
        else:
            p.values[axe] = (p.values[axe] - self.__InnerTsf[axe, 3]) * self.__InnerTsf[(axe, axe)]
            p.values[axe] += self.m_OutterStartPosition[axe]
            return p

    def outterPointToScreen(self, outterPoint):
        # Transformacia bodu
        transformedPointVector = self.__Tsf * outterPoint

        # Projekcia bodu
        projectedPointVector = self.__Projection * transformedPointVector

        return self.toScreenCords(projectedPointVector)

    def toScreenCords(self, pv):
        # px = min(((pv[0] + 1) * 0.5 * Graph.WIDTH), Graph.WIDTH - 1)
        px = ((pv[0] + 1) * 0.5 * Graph.WIDTH)

        # py = min(((1 - (pv[1] + 1) * 0.5) * Graph.WIDTH), Graph.HEIGHT - 1)
        py = ((1 - (pv[1] + 1) * 0.5) * Graph.WIDTH)

        return myMatrix.Vector3D(int(px), int(py), 1)


    def MakeGraphCube(self):
        update_start_time = time.time_ns()
        self.drawGraphCubeWall()
        self.drawGraphCubeAxis()
        print('Make cube time: {} ns'.format((time.time_ns() - update_start_time)))
        # print(poziciaMinusJednaHodnota)

    def Move(self, event):
        if event.char == 'a':
            self.__InnerTranslation[0] -= 0.1
        if event.char == 'd':
            self.__InnerTranslation[0] += 0.1
        if event.char == 'w':
            self.__InnerTranslation[2] -= 0.1
        if event.char == 's':
            self.__InnerTranslation[2] += 0.1
        if event.char == 'c':
            self.__InnerTranslation[1] += 0.1
        if event.char == 'v':
            self.__InnerTranslation[1] -= 0.1
        #self.update()

    def update(self):
        if self.__SceneChange:
            self.__Graph.delete('all')

            self.MakeGraphCube()

            # Transformovane vektory, najskor osy
            tvs = []

            for v in self.__CordsSys:
                tvs.append(self.outterPointToScreen(self.innerCordsToOutter(v)))

            # Vykreslenie osy
            self.__Graph.create_line(tvs[0].values[0], tvs[0].values[1], tvs[1].values[0], tvs[1].values[1], fill='red')
            self.__Graph.create_line(tvs[0].values[0], tvs[0].values[1], tvs[2].values[0], tvs[2].values[1], fill='green')
            self.__Graph.create_line(tvs[0].values[0], tvs[0].values[1], tvs[3].values[0], tvs[3].values[1], fill='blue')



            self.drawPoints()

            self.drawPolygons()

            self.__SceneChange = False

        self.__Parent.after(10, self.update)

    def drawPolygons(self):
        update_start_time = time.time_ns()
        for poly in self.Polygons:
            polygonEdges = poly.edges
            polygonPeaks = poly.peaks
            for v in polygonEdges:
                v1 = polygonPeaks[v[0]]
                v2 = polygonPeaks[v[1]]
                r1 = self.innerCordsToOutter(v1)
                r2 = self.innerCordsToOutter(v2)
                p1 = self.outterPointToScreen(r1)
                p2 = self.outterPointToScreen(r2)
                #intersect_calculation_start = time.time_ns()
                rayV = r2 - r1
                epsilon = 0.0000000000000001
                intersect = True
                tmin = 0
                tmax = 1
                for i in range(3):
                    if math.fabs(rayV.values[i]) < epsilon:
                        if r1.values[i] < -1 or r1.values[i] > 1:
                            intersect = False
                            break
                    else:
                        ood = 1/ rayV.values[i]
                        t1 = (-1 - r1.values[i]) * ood
                        t2 = (1 - r1.values[i]) * ood
                        if t1 > t2:
                            t1, t2 = t2, t1
                        tmin = max(tmin, t1)
                        tmax = min(tmax, t2)
                        if tmin > tmax:
                            intersect = False
                            break

                if intersect:
                    q = myMatrix.Vector3D()
                    p1 = None
                    p2 = None
                    if (math.fabs(r2.values[0]) - 1 <= 0.000001) and (math.fabs(r2.values[1]) - 1 <= 0.000001) and (math.fabs(r2.values[2]) - 1 <= 0.000001):
                        for i in range(3):
                            q.values[i] = r1.values[i] + rayV.values[i] * tmin
                        p1 = self.outterPointToScreen(q)
                        p2 = self.outterPointToScreen(r2)
                    else:
                        f = myMatrix.Vector3D()
                        for i in range(3):
                            q.values[i] = r1.values[i] + rayV.values[i] * tmin
                            f.values[i] = r1.values[i] + rayV.values[i] * tmax
                        p1 = self.outterPointToScreen(q)
                        p2 = self.outterPointToScreen(f)
                    self.__Graph.create_line(p1[0], p1[1], p2[0], p2[1], fill='red')
                    #print('Intersect calculation time: {} ns'.format((time.time_ns() - intersect_calculation_start)))
                else:
                    #print('Intersect calculation time: {} ns'.format((time.time_ns() - intersect_calculation_start)))
                    continue
        print('Draw polygons time: {} ms'.format((time.time_ns() - update_start_time)/1000000))

    def drawPoints(self):
        update_start_time = time.time_ns()
        viewablePoints = []
        id = 0
        for p in self.__Points:
            r = self.innerCordsToOutter(p.position)
            if (math.fabs(r.values[0]) - 1 <= 0.000001) and (math.fabs(r.values[1]) - 1 <= 0.000001) and (
                    math.fabs(r.values[2]) - 1 <= 0.000001):

                tmpTest = self.__Tsf * r
                heapq.heappush(viewablePoints, (tmpTest.values[2], id, p))
                id += 1
        while viewablePoints:
            point = heapq.heappop(viewablePoints)[2]
            outter = self.innerCordsToOutter(point.position)
            transofmation = self.__Tsf * outter
            zakladnyOdtien = point.actualShade
            outlineFarba = point.getActualShadeToHex()
            farba = '#{:02x}{:02x}{:02x}'.format(zakladnyOdtien[0], zakladnyOdtien[1], zakladnyOdtien[2])
            if transofmation.values[2] < 0:
                redColor = min(zakladnyOdtien[0] + 255 * math.fabs(transofmation[2]), 255)
                greenColor = min(zakladnyOdtien[1] + 255 * math.fabs(transofmation[2]), 255)
                blueColor = min(zakladnyOdtien[2] + 255 * math.fabs(transofmation[2]), 255)
                farba = '#{:02x}{:02x}{:02x}'.format(int(redColor), int(greenColor), int(blueColor))

            projection = self.__Projection * transofmation
            screenCords = self.toScreenCords(projection)
            self.__Graph.create_oval(screenCords[0] - 5, screenCords[1] - 5, screenCords[0] + 5, screenCords[1] + 5, fill=farba, outline=outlineFarba)
        print('Draw points time: {} ns'.format((time.time_ns() - update_start_time)))

    def rotationUpdate(self):
        self.__RotationMatX[(1, 1)] = math.cos(math.radians(self.__Angles[0]))
        self.__RotationMatX[(1, 2)] = -math.sin(math.radians(self.__Angles[0]))
        self.__RotationMatX[(2, 1)] = math.sin(math.radians(self.__Angles[0]))
        self.__RotationMatX[(2, 2)] = math.cos(math.radians(self.__Angles[0]))

        self.__RotationMatY[(0, 0)] = math.cos(math.radians(self.__Angles[1]))
        self.__RotationMatY[(0, 2)] = math.sin(math.radians(self.__Angles[1]))
        self.__RotationMatY[(2, 0)] = -math.sin(math.radians(self.__Angles[1]))
        self.__RotationMatY[(2, 2)] = math.cos(math.radians(self.__Angles[1]))

        self.__RotationMatZ[(0, 0)] = math.cos(math.radians(self.__Angles[2]))
        self.__RotationMatZ[(0, 1)] = -math.sin(math.radians(self.__Angles[2]))
        self.__RotationMatZ[(1, 0)] = math.sin(math.radians(self.__Angles[2]))
        self.__RotationMatZ[(1, 1)] = math.cos(math.radians(self.__Angles[2]))


    def outterTransformationMatrixUpdate(self):
        self.__Rot = self.__RotationMatX * self.__RotationMatY * self.__RotationMatZ
        # self.Rot = self.__RotationMatY * self.__RotationMatZ
        '''
        self.Tr[(0, 3)] = self.m_TranslationCam[0]
        self.Tr[(1, 3)] = self.m_TranslationCam[1]
        self.Tr[(2, 3)] = self.m_TranslationCam[2]
        '''
        # self.__Tsf = self.Scale * self.Rot * self.Tr
        self.__Tsf = self.__Scale * self.__Rot
        self.__SceneChange = True
        #self.update()

    def innerTransformationMatrixUpdate(self):
        self.__InnerTsf[(0, 3)] = self.__InnerTranslation[0]
        self.__InnerTsf[(1, 3)] = self.__InnerTranslation[1]
        self.__InnerTsf[(2, 3)] = self.__InnerTranslation[2]
        self.__SceneChange = True
        #self.update()

    def numerifyAxis(self):
        for dim in range(3):
            tmpScale = self.__InnerTsf[(dim, dim)]
            rozdiel = math.fabs(tmpScale * (
                        self.__AxisNumbersPosition[dim][0][0].values[dim] - self.__AxisNumbersPosition[dim][1][0].values[dim]))
            if rozdiel < 0.2:
                nasobok = 1
                if self.previousTmpScale[dim] / tmpScale <= 1:
                    nasobok *= 2
                else:
                    nasobok *= 1.25
                    self.previousTmpScale[dim] /= 10
                    if self.previousTmpScale[dim] > 10:
                        self.previousTmpScale[dim] = round(self.previousTmpScale[dim])
                self.updateAxisNumberPositions(dim, nasobok)
            elif rozdiel > 0.4:
                nasobok = 1
                if self.previousTmpScale[dim] / tmpScale >= 0.1:
                    nasobok *= 2
                else:
                    nasobok *= 1.25
                    self.previousTmpScale[dim] *= 10
                    if self.previousTmpScale[dim] > 1:
                        self.previousTmpScale[dim] = round(self.previousTmpScale[dim])
                self.updateAxisNumberPositions(dim, nasobok, multiply=False)

    def dragcallback(self, event):
        self.cnt -= 1
        if self.cnt == 0:
            self.cnt = Graph.RATE
            diffX = event.x - self.prevmouseX
            diffY = event.y - self.prevmouseY

            self.__Angles[0] += diffY * Graph.SPEED
            self.__Angles[1] += diffX * Graph.SPEED
            if self.__Angles[0] >= 360.0:
                self.__Angles[0] -= 360.0
            if self.__Angles[0] < 0.0:
                self.__Angles[0] += 360.0
            if self.__Angles[1] >= 360.0:
                self.__Angles[1] -= 360.0
            if self.__Angles[1] < 0.0:
                self.__Angles[1] += 360.0
            '''
            else:
                self.__Angles[2] += diffX * Graph.SPEED
                if self.__Angles[2] >= 360.0:
                    self.__Angles[2] -= 360.0
                if self.__Angles[2] < 0.0:
                    self.__Angles[2] += 360.0
            '''
            self.rotationUpdate()
            self.outterTransformationMatrixUpdate()

        self.prevmouseX = event.x
        self.prevmouseY = event.y


    def releasecallback(self, event):
        self.cnt = Graph.RATE
        self.prevmouseX = 0.0
        self.prevmouseY = 0.0


    def dragcallbackRight(self, event):
        self.cntRight -= 1
        if self.cntRight == 0:
            self.cntRight = self.ZOOMRATE
            diffY = event.y - self.prevmouseYright
            if diffY < 0 and diffY != 0:
                #for i in range(math.fabs(diffY)):
                self.__InnerTsf[(0, 0)] /= math.pow(self.__ScaleFactor, Graph.ZOOMSPEED)
                self.__InnerTsf[(1, 1)] /= math.pow(self.__ScaleFactor, Graph.ZOOMSPEED)
                self.__InnerTsf[(2, 2)] /= math.pow(self.__ScaleFactor, Graph.ZOOMSPEED)

            elif diffY > 0:
                #for i in range(diffY):
                self.__InnerTsf[(0, 0)] *= math.pow(self.__ScaleFactor, Graph.ZOOMSPEED)
                self.__InnerTsf[(1, 1)] *= math.pow(self.__ScaleFactor, Graph.ZOOMSPEED)
                self.__InnerTsf[(2, 2)] *= math.pow(self.__ScaleFactor, Graph.ZOOMSPEED)

            # print(math.fabs(tmpScale * self.__AxisNumbersPosition[0][0][0].values[0] - tmpScale * self.__AxisNumbersPosition[0][1][0].values[0]))
            self.numerifyAxis()
            self.innerTransformationMatrixUpdate()

        self.prevmouseYright = event.y


    def releasecallbackRight(self, event):
        self.cntRight = Graph.ZOOMRATE
        self.prevmouseYright = 0.0

window = tk.Tk()
window.title("Skuska")
graf = Graph(window)
window.mainloop()
