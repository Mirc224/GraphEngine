import math
import tkinter as tk
import myMatrix
import copy


class Graph(tk.Frame):
    WIDTH = 640.0
    HEIGHT = 640.0

    RATE = 2
    SPEED = 3

    ZOOMRATE = 1
    ZOOMSPEED = 1

    GRAPH_COLOR = '#eaeaea'

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.Graph = tk.Canvas(self, width=Graph.WIDTH, height=Graph.HEIGHT, bg='white')
        self.Graph.pack()
        self.pack()


        self.Show = [0, 0, 0]
        self.LabelCords = []
        # Axes of graph in the middle
        self.CordsSys = [
            myMatrix.Vector3D(0.0, 0.0, 0.0),  # Origin
            myMatrix.Vector3D(1, 0.0, 0.0),  # X
            myMatrix.Vector3D(0.0, 1, 0.0),  # Y
            myMatrix.Vector3D(0.0, 0.0, 1)  # Z
        ]

        self.GraphCube = [
            myMatrix.Vector3D(-1, 1, -1),
            myMatrix.Vector3D(1, 1, -1),
            myMatrix.Vector3D(1, -1, -1),
            myMatrix.Vector3D(-1, -1, -1),
            myMatrix.Vector3D(-1, 1, 1),
            myMatrix.Vector3D(1, 1, 1),
            myMatrix.Vector3D(1, -1, 1),
            myMatrix.Vector3D(-1, -1, 1)
        ]

        self.AxisNumbersPosition = [
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

        self.AxisEdges = [
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

        self.stenyStred = [
            myMatrix.Vector3D(0.0, 0.0, -1.0),
            myMatrix.Vector3D(1.0, 0.0, 0.0),
            myMatrix.Vector3D(0.0, 0.0, 1.0),
            myMatrix.Vector3D(-1.0, 0.0, 0.0),
            myMatrix.Vector3D(0.0, 1.0, 0.0),
            myMatrix.Vector3D(0.0, -1.0, 0.0),
        ]

        self.dotz = myMatrix.Vector3D(1, 0, 0)

        self.Points = [
            myMatrix.Vector3D(5, -1.0, 1.0),
            myMatrix.Vector3D(4, -1.0, 1.0),
            myMatrix.Vector3D(3, -1.0, 1.0),
            myMatrix.Vector3D(2, -1.0, 1.0),
            myMatrix.Vector3D(1, -1.0, 1.0),
            myMatrix.Vector3D(0.0, -1.0, 1.0),
            myMatrix.Vector3D(-1, -1.0, 1.0),
            myMatrix.Vector3D(-2, -1.0, 1.0),
            myMatrix.Vector3D(-3, -1.0, 1.0),
            myMatrix.Vector3D(-4, -1.0, 1.0),
            myMatrix.Vector3D(-5, -1.0, 1.0),
        ]

        self.Points = [
            myMatrix.Vector3D(1.0, 6,6),
        ]
        # Steny kociek s cislami vrcholov
        self.CubeFaces = [
            [0, 1, 2, 3],
            [1, 5, 6, 2],
            [5, 4, 7, 6],
            [4, 0, 3, 7],
            [0, 4, 5, 1],
            [3, 2, 6, 7]
        ]

        # Uhly ktore sa pouzivaju pri rotaciach
        self.Angles = [0.0, 0.0, 0.0]

        # Translation matrix, na posun kamery
        self.TranslationCam = [0.0, 0.0, 0.0]

        # Zvacsovnaie
        scaleX = 0.5
        scaleY = 0.5
        scaleZ = 0.5
        self.Scale = myMatrix.Matrix(4, 4)
        self.Scale[(0, 0)] = scaleX
        self.Scale[(1, 1)] = scaleY
        self.Scale[(2, 2)] = scaleZ

        self.InnerTranslation = [2.3, 0, 0]

        self.tmpZobrazujeSa = False

        self.RotationMatX = myMatrix.Matrix(4, 4)

        self.RotationMatY = myMatrix.Matrix(4, 4)

        self.RotationMatZ = myMatrix.Matrix(4, 4)

        self.Rot = myMatrix.Matrix(4, 4)

        self.Tsf = myMatrix.Matrix(4, 4)

        #self.Tr = myMatrix.Matrix(4, 4)
        #self.Tr[(0, 3)] = 2

        self.InnerTsf = myMatrix.Matrix(4, 4)
        self.InnerTsf[(0, 0)] = 1
        self.InnerTsf[(1, 1)] = 1
        self.InnerTsf[(2, 2)] = 1
        self.InnerTsf[(0, 3)] = self.InnerTranslation[0]
        self.InnerTsf[(1, 3)] = self.InnerTranslation[1]
        self.InnerTsf[(2, 3)] = self.InnerTranslation[2]

        self.Projection = myMatrix.Matrix(4, 4)

        # self.Projection[(2, 3)] = -1.0
        # self.Projection[(3, 3)] = 0.0
        # self.Projection[(3, 2)] = -0.5

        fov = 90.0  # between 30 and 90 ?
        zfar = 100.0
        znear = 0.1
        S = 1 / (math.tan(math.radians(fov / 2)))
        # 1st version (Perspective Projection)
        self.Projection[(0, 0)] = S
        self.Projection[(1, 1)] = S
        self.Projection[(2, 2)] = -zfar / (zfar - znear)
        self.Projection[(3, 2)] = -0.05
        # self.Proj[(2, 3)] = -(zfar * znear) / (zfar - znear)

        self.lctrl_pressed = False

        self.Graph.bind("<B1-Motion>", self.dragcallback)
        self.Graph.bind("<ButtonRelease-1>", self.releasecallback)

        self.Graph.bind("<B3-Motion>", self.dragcallbackRight)
        self.Graph.bind("<ButtonRelease-3>", self.releasecallbackRight)

        self.LabelAngle = [0.0, 0.0, 0.0]
        self.Odtien = 0
        self.cnt = Graph.RATE
        self.cntRight = Graph.RATE
        self.prevmouseX = 0.0
        self.prevmouseY = 0.0
        self.previousTmpScale = 1
        self.prevmouseYright = 0.0
        self.ScaleFactor = 1.01

        self.numerifyAxis()
        self.outterTransformationMatrixUpdate()

    def drawGraphCubeWall(self):
        self.Show = [0, 0, 0]
        listOfFaces = []
        # tstovanie stien
        transformedPoint1 = self.Tsf * self.stenyStred[2]
        transformedPoint2 = self.Tsf * self.stenyStred[0]
        if transformedPoint1.values[2] <= transformedPoint2.values[2]:
            listOfFaces.append(2)
        else:
            listOfFaces.append(0)
            self.Show[0] += 1
            self.Show[1] += 1
        transformedPoint1 = self.Tsf * self.stenyStred[3]
        transformedPoint2 = self.Tsf * self.stenyStred[1]
        if transformedPoint1.values[2] <= transformedPoint2.values[2]:
            listOfFaces.append(3)
        else:
            listOfFaces.append(1)
            self.Show[1] += 2
            self.Show[2] += 1
        transformedPoint1 = self.Tsf * self.stenyStred[5]
        transformedPoint2 = self.Tsf * self.stenyStred[4]
        if transformedPoint1.values[2] <= transformedPoint2.values[2]:
            listOfFaces.append(5)
        else:
            listOfFaces.append(4)
            self.Show[0] += 2
            self.Show[2] += 2

        # print('ShowX: {}  ShowY: {}  ShowZ: {}'.format(show[0], show[1], show[2]))
        for faceNumber in listOfFaces:
            inviewvingvolume = False
            poly = []
            for peak in range(len(self.CubeFaces[faceNumber])):
                peakPositionVector = self.GraphCube[self.CubeFaces[faceNumber][peak]]

                # Transformacia bodu
                transformedPointVector = self.Tsf * peakPositionVector

                # Projekcia bodu
                projectedPointVector = self.Projection * transformedPointVector

                # Vlozenie bodu obrazovky do listu transformovanych vrcholov
                screenProjectionCords = self.toScreenCords(projectedPointVector)
                x = int(screenProjectionCords.values[0])
                y = int(screenProjectionCords.values[1])
                poly.append((x, y))

                # Ak je aspon jedene vrchol vo viditelnej oblasti, vykresli cely polygon
                # if (-1.0 <= ps.values[0] < 1.0) and (-1.0 <= ps.values[1] < 1.0) and (-1.0 <= ps.values[2] < 1.0):
                inviewvingvolume = True

            if inviewvingvolume:
                self.Graph.create_polygon(poly[0][0], poly[0][1], poly[1][0], poly[1][1], poly[2][0], poly[2][1],
                                          poly[3][0], poly[3][1], fill=Graph.GRAPH_COLOR)
                for k in range(len(poly) - 1):
                    self.Graph.create_line(poly[k][0], poly[k][1], poly[k + 1][0], poly[k + 1][1], fill='white')
                self.Graph.create_line(poly[len(poly) - 1][0], poly[len(poly) - 1][1], poly[0][0], poly[0][1],
                                       fill='white')

    def drawGraphCubeAxis(self):
        labels = ['Label X', 'Label Y', 'Label Z']
        self.LabelCords = []
        for axeFace in range(3):
            edgeNodeVector0 = self.GraphCube[self.AxisEdges[axeFace][self.Show[axeFace]][0]]
            edgeNodeVector1 = self.GraphCube[self.AxisEdges[axeFace][self.Show[axeFace]][1]]
            transformedPointVector0 = self.Tsf * edgeNodeVector0
            transformedPointVector1 = self.Tsf * edgeNodeVector1
            projectedPointVector0 = self.Projection * transformedPointVector0
            projectedPointVector1 = self.Projection * transformedPointVector1
            screenProjectionCords0 = self.toScreenCords(projectedPointVector0)
            screenProjectionCords1 = self.toScreenCords(projectedPointVector1)

            self.LabelAngle[axeFace] = math.degrees(
                math.acos(math.fabs(projectedPointVector0[0] - projectedPointVector1[0]) / math.sqrt(
                    math.fabs(projectedPointVector0[0] - projectedPointVector1[0]) ** 2 + math.fabs(
                        projectedPointVector0[1] - projectedPointVector1[1]) ** 2)))

            # print('{}: {} {} {}'.format(labels[cord], self.Angles[0], self.Angles[1], self.LabelAngle[cord]))
            if self.Angles[0] < 180:
                if self.Angles[1] > 270:
                    if axeFace != 2:
                        self.LabelAngle[axeFace] = 360 - self.LabelAngle[axeFace]
                elif self.Angles[1] > 180:
                    if axeFace == 2:
                        self.LabelAngle[axeFace] = 360 - self.LabelAngle[axeFace]
                elif self.Angles[1] > 90:
                    if axeFace != 2:
                        self.LabelAngle[axeFace] = 360 - self.LabelAngle[axeFace]
                elif self.Angles[1] >= 0.0:
                    if axeFace == 2:
                        self.LabelAngle[axeFace] = 360 - self.LabelAngle[axeFace]

            else:
                if self.Angles[1] <= 90:
                    self.LabelAngle[axeFace] = 360 - self.LabelAngle[axeFace]
                if 180 <= self.Angles[1] <= 270:
                    if axeFace != 2:
                        self.LabelAngle[axeFace] = 360 - self.LabelAngle[axeFace]
                elif axeFace == 2:
                    self.LabelAngle[axeFace] = 360 - self.LabelAngle[axeFace]

            distance = 1.2
            if self.Show[axeFace] < 2:
                if self.Show[axeFace] < 1:
                    if axeFace != 2:
                        self.LabelCords.append(myMatrix.Vector3D(-distance, -distance, -distance))
                    else:
                        self.LabelCords.append(myMatrix.Vector3D(distance, -distance, -distance))
                    self.LabelCords[axeFace].values[axeFace] = 0
                else:
                    self.LabelCords.append(myMatrix.Vector3D(-distance, -distance, distance))
                    self.LabelCords[axeFace].values[axeFace] = 0
            else:
                if self.Show[axeFace] < 3:
                    if axeFace != 2:
                        self.LabelCords.append(myMatrix.Vector3D(distance, distance, -distance))
                    else:
                        self.LabelCords.append(myMatrix.Vector3D(distance, distance, -distance))
                    self.LabelCords[axeFace].values[axeFace] = 0
                else:
                    if axeFace != 2:
                        self.LabelCords.append(myMatrix.Vector3D(distance, distance, distance))
                    else:
                        self.LabelCords.append(myMatrix.Vector3D(-distance, distance, distance))
                    self.LabelCords[axeFace].values[axeFace] = 0

            tsfLabelPosistionVector = self.Tsf * self.LabelCords[axeFace]
            projectedPointVector = self.Projection * tsfLabelPosistionVector

            screenProjectionCords = self.toScreenCords(projectedPointVector)
            self.Graph.create_line(screenProjectionCords0.values[0], screenProjectionCords0.values[1],
                                   screenProjectionCords1.values[0], screenProjectionCords1.values[1], fill='black')
            self.Graph.create_text(screenProjectionCords.values[0], screenProjectionCords.values[1], fill='black',
                                   text=labels[axeFace],
                                   angle=self.LabelAngle[axeFace])

    def drawGraphAxisNumberAndLines(self):
        nlLength = 0.03
        for axeFace in range(3):
            changeVector0 = myMatrix.Vector3D(1, 1, 1, 1)
            changeVector1 = myMatrix.Vector3D(1, 1, 1, 1)
            if self.Show[axeFace] < 2:
                if self.Show[axeFace] > 0:
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
                if self.Show[axeFace] < 3:
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
            for perpenLinePointsVectorTuple in self.AxisNumbersPosition[axeFace]:
                lineStartPointVector = perpenLinePointsVectorTuple[0] * changeVector0
                if axeFace == 1:
                    pass
                    #print('Vector: {}    scale*1:  {}   rozdiel:   {}'.format(lineStartPointVector.values[1], 1 * self.InnerTsf[(axeFace, axeFace)],math.fabs(lineStartPointVector.values[1]) - 1 * self.InnerTsf[(axeFace, axeFace)]))
                    #print(lineStartPointVector[axeFace] + self.InnerTsf[(axeFace, 3)])
                lineStartPointVector.values[axeFace] *= self.InnerTsf[(axeFace, axeFace)]
                if not (math.fabs(lineStartPointVector.values[0]) - 1 <= 0.000001) or not (
                        math.fabs(lineStartPointVector.values[1]) - 1 <= 0.000001) or not (
                        math.fabs(lineStartPointVector.values[2]) - 1 <= 0.000001):
                    continue
                tsfStartPointVector = self.Tsf * lineStartPointVector

                projectedStartPointVector = self.Projection * tsfStartPointVector
                startPointScreenProjectionCords = self.toScreenCords(projectedStartPointVector)

                # druhy bod dlhej ciary
                lineEndPointVector = perpenLinePointsVectorTuple[1] * changeVector1
                lineEndPointVector.values[axeFace] *= self.InnerTsf[(axeFace, axeFace)]
                tsfEndPointVector = self.Tsf * lineEndPointVector
                projectedEndPointVector = self.Projection * tsfEndPointVector
                endPointScreenProjectionCords = self.toScreenCords(projectedEndPointVector)
                # vykreslenie dlhej ciary
                self.Graph.create_line(startPointScreenProjectionCords[0], startPointScreenProjectionCords[1],
                                       endPointScreenProjectionCords[0], endPointScreenProjectionCords[1], fill='gray')

                # kolma ciara
                perpendicularEndPointVector = perpenLinePointsVectorTuple[1] * changeVector1
                perpendicularEndPointVector.values[(axeFace + 1) % 2] *= -1
                perpendicularEndPointVector.values[axeFace] *= self.InnerTsf[(axeFace, axeFace)]
                tsfPerpendicularEndPointVector = self.Tsf * perpendicularEndPointVector
                projectedPerpendicularEndPointVector = self.Projection * tsfPerpendicularEndPointVector
                perpendicularEndPointScreenProjectionCords = self.toScreenCords(projectedPerpendicularEndPointVector)
                self.Graph.create_line(endPointScreenProjectionCords[0], endPointScreenProjectionCords[1],
                                       perpendicularEndPointScreenProjectionCords[0],
                                       perpendicularEndPointScreenProjectionCords[1], fill='gray')

                # ciarka na ciselenj osy
                axeMarkStartPointVector = perpenLinePointsVectorTuple[0] * changeVector0
                axeMarkStartPointVector.values[axeFace] = self.InnerTsf[(axeFace, axeFace)] * \
                                                          axeMarkStartPointVector.values[axeFace]
                if axeFace != 2:
                    axeMarkStartPointVector.values[2] = perpenLinePointsVectorTuple[0][2] * changeVector0[2] + nlLength
                else:
                    axeMarkStartPointVector.values[0] = perpenLinePointsVectorTuple[0][0] * changeVector0[0] + nlLength
                tsfAxeMarkStartPointVector = self.Tsf * axeMarkStartPointVector
                projectedAxeMarkStartPointVector = self.Projection * tsfAxeMarkStartPointVector
                axeMarkStartPointScreenProjectionCords = self.toScreenCords(projectedAxeMarkStartPointVector)

                axeMarkEndPointVector = perpenLinePointsVectorTuple[0] * changeVector0
                axeMarkEndPointVector.values[axeFace] = self.InnerTsf[(axeFace, axeFace)] * \
                                                        axeMarkEndPointVector.values[axeFace]
                if axeFace != 2:
                    axeMarkEndPointVector.values[2] = perpenLinePointsVectorTuple[0][2] * changeVector0[2] - nlLength
                else:
                    axeMarkEndPointVector.values[0] = perpenLinePointsVectorTuple[0][0] * changeVector0[0] - nlLength
                tsfAxeMarkEndPointVector = self.Tsf * axeMarkEndPointVector
                projectedAxeMarkEndPointVector = self.Projection * tsfAxeMarkEndPointVector
                axeMarkEndPointScreenProjectionCords = self.toScreenCords(projectedAxeMarkEndPointVector)

                self.Graph.create_line(axeMarkStartPointScreenProjectionCords[0],
                                       axeMarkStartPointScreenProjectionCords[1],
                                       axeMarkEndPointScreenProjectionCords[0], axeMarkEndPointScreenProjectionCords[1],
                                       fill='black')

                numberPositionVector = perpenLinePointsVectorTuple[0] * changeVector0
                numberPositionVector.values[axeFace] = self.InnerTsf[(axeFace, axeFace)] * numberPositionVector.values[
                    axeFace]
                for cord in range(3):
                    if cord != axeFace:
                        if self.LabelCords[axeFace].values[cord] < 0:
                            numberPositionVector.values[cord] = self.LabelCords[axeFace].values[cord] + (
                                        math.fabs(self.LabelCords[axeFace].values[cord]) - 1) / 2
                        else:
                            numberPositionVector.values[cord] = self.LabelCords[axeFace].values[cord] - (
                                        math.fabs(self.LabelCords[axeFace].values[cord]) - 1) / 2

                tsfNumberPositionVector = self.Tsf * numberPositionVector
                projectedNumberPositionVector = self.Projection * tsfNumberPositionVector
                numberPositionScreenProjectionCords = self.toScreenCords(projectedNumberPositionVector)
                self.Graph.create_text(numberPositionScreenProjectionCords[0], numberPositionScreenProjectionCords[1],
                                       text=round(
                                           perpenLinePointsVectorTuple[0].values[axeFace] + self.InnerTranslation[
                                               axeFace], 3))

    def MakeGraphCube(self):
        self.drawGraphCubeWall()
        self.drawGraphCubeAxis()
        self.drawGraphAxisNumberAndLines()
            #print(poziciaMinusJednaHodnota)


    def ChangeColor(self, event):
        if event.char == 'u':
            self.Odtien += 1
            if self.Odtien > 200:
                self.Odtien = 200
        if event.char == 'i':
            self.Odtien -= 1
            if self.Odtien < 0:
                self.Odtien = 0
        self.update()

    def Move(self, event):
        if event.char == 'a':
            self.InnerTranslation[0] -= 0.1
        if event.char == 'd':
            self.InnerTranslation[0] += 0.1
        if event.char == 'w':
            self.InnerTranslation[2] -= 0.1
        if event.char == 's':
            self.InnerTranslation[2] += 0.1
        if event.char == 'c':
            self.InnerTranslation[1] += 0.1
        if event.char == 'v':
            self.InnerTranslation[1] -= 0.1
        self.update()


    def toScreenCords(self, pv):
        #px = min(((pv[0] + 1) * 0.5 * Graph.WIDTH), Graph.WIDTH - 1)
        px = ((pv[0] + 1) * 0.5 * Graph.WIDTH)

        #py = min(((1 - (pv[1] + 1) * 0.5) * Graph.WIDTH), Graph.HEIGHT - 1)
        py = ((1 - (pv[1] + 1) * 0.5) * Graph.WIDTH)

        return myMatrix.Vector3D(int(px), int(py), 1)

    def update(self):
        self.Graph.delete('all')

        self.MakeGraphCube()

        # Transformovane vektory, najskor osy
        tvs = []

        for v in self.CordsSys:
            r = self.InnerTsf * v
            r = self.Tsf * r
            ps = self.Projection * r
            tvs.append(self.toScreenCords(ps))

        # Vykreslenie osy
        self.Graph.create_line(tvs[0].values[0], tvs[0].values[1], tvs[1].values[0], tvs[1].values[1], fill='red')
        self.Graph.create_line(tvs[0].values[0], tvs[0].values[1], tvs[2].values[0], tvs[2].values[1], fill='green')
        self.Graph.create_line(tvs[0].values[0], tvs[0].values[1], tvs[3].values[0], tvs[3].values[1], fill='blue')

        r = self.InnerTsf * self.dotz

        if (math.fabs(r.values[0]) - 1 <= 0.000001) and (math.fabs(r.values[1]) - 1 <= 0.000001) and (
                math.fabs(r.values[2]) - 1 <= 0.000001):
            farba = '#ff{}{}'.format('{:02x}'.format(self.Odtien), '{:02x}'.format(self.Odtien))
            r = self.Tsf * r
            ps = self.Projection * r
            tmp = self.toScreenCords(ps)
            self.Graph.create_oval(tmp[0] - 5, tmp[1] - 5, tmp[0] + 5, tmp[1] + 5, fill=farba, outline='red')

        for p in self.Points:
            r = myMatrix.Vector3D()
            for i in range(3):
                r.values[i] = (p[i] - self.InnerTsf[(i, 3)]) * self.InnerTsf[(i, i)]
            if (math.fabs(r.values[0]) - 1 <= 0.000001) and (math.fabs(r.values[1]) - 1 <= 0.000001) and (math.fabs(r.values[2]) - 1 <= 0.000001):
                farba = '#ff{}{}'.format('{:02x}'.format(self.Odtien), '{:02x}'.format(self.Odtien))
                r = self.Tsf * r
                ps = self.Projection * r
                tmp = self.toScreenCords(ps)
                self.Graph.create_oval(tmp[0] - 5, tmp[1] - 5, tmp[0] + 5, tmp[1] + 5, fill='black')


    def rotationUpdate(self):
        self.RotationMatX[(1, 1)] = math.cos(math.radians(self.Angles[0]))
        self.RotationMatX[(1, 2)] = -math.sin(math.radians(self.Angles[0]))
        self.RotationMatX[(2, 1)] = math.sin(math.radians(self.Angles[0]))
        self.RotationMatX[(2, 2)] = math.cos(math.radians(self.Angles[0]))

        self.RotationMatY[(0, 0)] = math.cos(math.radians(self.Angles[1]))
        self.RotationMatY[(0, 2)] = math.sin(math.radians(self.Angles[1]))
        self.RotationMatY[(2, 0)] = -math.sin(math.radians(self.Angles[1]))
        self.RotationMatY[(2, 2)] = math.cos(math.radians(self.Angles[1]))

        self.RotationMatZ[(0, 0)] = math.cos(math.radians(self.Angles[2]))
        self.RotationMatZ[(0, 1)] = -math.sin(math.radians(self.Angles[2]))
        self.RotationMatZ[(1, 0)] = math.sin(math.radians(self.Angles[2]))
        self.RotationMatZ[(1, 1)] = math.cos(math.radians(self.Angles[2]))

        self.outterTransformationMatrixUpdate()

    def outterTransformationMatrixUpdate(self):
        self.Rot = self.RotationMatX * self.RotationMatY * self.RotationMatZ
        # self.Rot = self.RotationMatY * self.RotationMatZ
        '''
        self.Tr[(0, 3)] = self.TranslationCam[0]
        self.Tr[(1, 3)] = self.TranslationCam[1]
        self.Tr[(2, 3)] = self.TranslationCam[2]
        '''
        # self.Tsf = self.Scale * self.Rot * self.Tr
        self.Tsf = self.Scale * self.Rot
        self.update()

    def dragcallback(self, event):
        self.cnt -= 1
        if self.cnt == 0:
            self.cnt = Graph.RATE
            diffX = event.x - self.prevmouseX
            diffY = event.y - self.prevmouseY
            # print(diffX, diffY)
            if not self.lctrl_pressed:
                self.Angles[0] += diffY * Graph.SPEED
                self.Angles[1] += diffX * Graph.SPEED
                if self.Angles[0] >= 360.0:
                    self.Angles[0] -= 360.0
                if self.Angles[0] < 0.0:
                    self.Angles[0] += 360.0
                if self.Angles[1] >= 360.0:
                    self.Angles[1] -= 360.0
                if self.Angles[1] < 0.0:
                    self.Angles[1] += 360.0

            else:
                self.Angles[2] += diffX * Graph.SPEED
                if self.Angles[2] >= 360.0:
                    self.Angles[2] -= 360.0
                if self.Angles[2] < 0.0:
                    self.Angles[2] += 360.0

            self.rotationUpdate()

        self.prevmouseX = event.x
        self.prevmouseY = event.y

    def releasecallback(self, event):
        self.cnt = Graph.RATE
        self.prevmouseX = 0.0
        self.prevmouseY = 0.0

    def innerTransformationMatrixUpdate(self):
        self.InnerTsf[(0, 3)] = self.InnerTranslation[0]
        self.InnerTsf[(1, 3)] = self.InnerTranslation[1]
        self.InnerTsf[(2, 3)] = self.InnerTranslation[2]
        self.update()

    def dragcallbackRight(self, event):
        diffY = event.y - self.prevmouseYright
        tmpScale = self.InnerTsf[(0, 0)]
        if diffY < 0 and diffY != 0:
            self.InnerTsf[(0, 0)] /= self.ScaleFactor
            self.InnerTsf[(1, 1)] /= self.ScaleFactor
            self.InnerTsf[(2, 2)] /= self.ScaleFactor

        elif diffY > 0:
            self.InnerTsf[(0, 0)] *= self.ScaleFactor
            self.InnerTsf[(1, 1)] *= self.ScaleFactor
            self.InnerTsf[(2, 2)] *= self.ScaleFactor

        #print(math.fabs(tmpScale * self.AxisNumbersPosition[0][0][0].values[0] - tmpScale * self.AxisNumbersPosition[0][1][0].values[0]))
        self.numerifyAxis()
        self.innerTransformationMatrixUpdate()

        self.prevmouseYright = event.y

    def releasecallbackRight(self, event):
        self.prevmouseYright = 0.0

    def numerifyAxis(self):
        #print(-1 / tmpScale + self.InnerTranslation[0],'    ' , 1 / tmpScale + self.InnerTranslation[0])
        tmpScale = self.InnerTsf[(0, 0)]
        if -1 / tmpScale + self.InnerTranslation[0] < 0 and 1 / tmpScale + self.InnerTranslation[0] > 0:
            #print('0 sa zobrazuje')
            #print(self.InnerTranslation[0] * tmpScale)
            self.tmpZobrazujeSa = True
        rozdiel = math.fabs(tmpScale * (self.AxisNumbersPosition[0][0][0].values[0] - self.AxisNumbersPosition[0][1][0].values[0]))
        if rozdiel < 0.2:
            nasobok = 1
            if self.previousTmpScale / tmpScale <= 1:
                nasobok *= 2
            else:
                nasobok *= 1.25
                self.previousTmpScale /= 10
                if self.previousTmpScale > 10:
                    self.previousTmpScale = round(self.previousTmpScale)
            for i in range(3):
                for v in self.AxisNumbersPosition[i]:
                    v[0].values[i] *= nasobok
                    v[1].values[i] *= nasobok
        elif rozdiel > 0.4:
            nasobok = 1
            if self.previousTmpScale / tmpScale >= 0.1:
                nasobok *= 2
            else:
                nasobok *= 1.25
                self.previousTmpScale *= 10
                if self.previousTmpScale > 1:
                    self.previousTmpScale = round(self.previousTmpScale)
            for i in range(3):
                for v in self.AxisNumbersPosition[i]:
                    v[0].values[i] /= nasobok
                    v[1].values[i] /= nasobok

vector = myMatrix.Vector(1, 2, 3)
window = tk.Tk()
window.title("Skuska")
graf = Graph(window)

window.mainloop()