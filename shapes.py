import myMatrix
import math

class Point:
    POINT_COUNTER = 0
    def __init__(self, x=0, y=0, z=0, color='#ff0000'):
        self.__PointID = Point.POINT_COUNTER
        Point.POINT_COUNTER += 1
        self.__Position = myMatrix.Vector3D(x, y, z)
        self.__DefaultShade = []
        tmp = ''
        if color:
            tmp = color
            if tmp[0] == '#':
                tmp = tmp[1:]
        else:
            tmp = 'ff0000'

        for i in range(3):
            hexNum = int(tmp[i * 2:(i+1) * 2], 16)
            hexNum = min(max(hexNum, 0), 255)
            self.__DefaultShade.append(hexNum)
        self.__ActualShade = self.__DefaultShade

    def getActualShade(self):
        return self.__ActualShade

    def getActualShadeToHex(self):
        return '#{:02x}{:02x}{:02x}'.format(self.__ActualShade[0], self.__ActualShade[1], self.__ActualShade[2])

    @property
    def position(self):
        return self.__Position

    @position.setter
    def position(self, pos):
        self.__Position = pos

    @property
    def actualShade(self):
        return self.__ActualShade

    @actualShade.setter
    def actualShade(self, shade):
        self.__ActualShade = shade

class Edge:
    def __init__(self, startPoint, endPoint, color='#000000'):
        self.__StartPoint = startPoint
        self.__EndPoint = endPoint
        self.__DefaultShade = []
        tmp = ''
        if color:
            tmp = color
            if tmp[0] == '#':
                tmp = tmp[1:]
        else:
            tmp = 'ff0000'

        for i in range(3):
            hexNum = int(tmp[i * 2:(i + 1) * 2], 16)
            hexNum = min(max(hexNum, 0), 255)
            self.__DefaultShade.append(hexNum)
        self.__ActualShade = self.__DefaultShade

    def getActualShadeToHex(self):
        return '#{:02x}{:02x}{:02x}'.format(self.__ActualShade[0], self.__ActualShade[1], self.__ActualShade[2])

    @property
    def actualShade(self):
        return self.__ActualShade

    @actualShade.setter
    def actualShade(self, shade):
        self.__ActualShade = shade

    @property
    def startPoint(self):
        return self.__StartPoint

    @property
    def startPoint(self):
        return self.__EndPoint

class Polygon:
    def __init__(self, xLower, yLower, zLower,  xUpper, yUpper, zUpper, Xdivide = 2, Ydivide = 2, Zdivide = 2):
        self.__Peaks = []
        self.__Edges = []

        xMaxSize = math.fabs(xLower - xUpper)
        yMaxSize = math.fabs(yLower - yUpper)
        zMaxSize = math.fabs(xLower - xUpper)

        xSign = 1 if xLower < xUpper else -1
        ySign = 1 if yLower < yUpper else -1
        zSign = 1 if zLower < zUpper else -1

        if Xdivide < 1:
            Xdivide = 1
        if Ydivide < 1:
            Ydivide = 1
        if Zdivide < 1:
            Zdivide = 1
        xOffSet = xSign * (xMaxSize / Xdivide)
        yOffSet = ySign * (yMaxSize / Ydivide)
        zOffSet = zSign * (zMaxSize / Zdivide)

        for z in range(Zdivide + 1):
            for y in range(Ydivide + 1):
                for x in range(Xdivide + 1):
                    pointNumber = z * ((Ydivide + 1) * (Xdivide + 1)) + y * (Xdivide + 1) + x
                    self.__Peaks.append(myMatrix.Vector3D(xLower + x * xOffSet, yLower + y * yOffSet, zLower + z * zOffSet))
                    if x != Xdivide:
                        self.__Edges.append([pointNumber, pointNumber + 1])
                    if y != Ydivide:
                        self.__Edges.append([pointNumber, pointNumber + (Xdivide + 1)])
                    if z != Zdivide:
                        self.__Edges.append([pointNumber, pointNumber + (Ydivide + 1) * (Xdivide + 1) ])

    @property
    def edges(self):
        return self.__Edges

    @property
    def peaks(self):
        return self.__Peaks


tmp = Polygon(0,0,0,2,-1,2,1,1,1)
print(tmp.edges)