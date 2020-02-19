import math


class Vector:

    def __init__(self, *args):
        self.values = list(args)

    def __str__(self):
        str = "[" + ' %f,' * len(self.values)
        if len(str) > 1:
            str = str[:-1]
        str += "]"
        return str % tuple(self.values)

    def magnitude(self, ):
        totalSum = 0
        for e in self.values:
            totalSum += e * e
        return math.sqrt(totalSum)

    def size(self):
        return len(self.values)

    def __add__(self, other):
        if isinstance(other, Vector):
            if len(self.values) == len(other.values):
                tmpValues = []
                for i in range(len(self.values)):
                    tmpValues.append(self.values[i] + other.values[i])
                return Vector(*tuple(tmpValues))
            else:
                raise Exception('Vector: error add, different size of vectors!')
        else:
            raise Exception('Vector: error add, not with vector!')

    def __sub__(self, other):
        if isinstance(other, Vector):
            if len(self.values) == len(other.values):
                tmpValues = []
                for i in range(len(self.values)):
                    tmpValues.append(self.values[i] - other.values[i])
                return Vector(*tuple(tmpValues))
            else:
                raise Exception('Vector: error sub, different size of vectors!')
        else:
            raise Exception('Vector: error sub, not with vector!')

    def __getitem__(self, item):
        if 0 <= item < len(self.values):
            return self.values[item]
        else:
            raise Exception('Vector: error, getitem index problem!')

    def __setitem__(self, item, val):
        if 0 <= item < len(self.values):
            self.values[item] = val
        else:
            raise Exception('Vector: error, setitem index problem!')

    def __neg__(self):
        return Vector(*tuple(map(lambda x: -x, self.values)))

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector(*tuple(map(lambda x: x * other, self.values)))
        elif isinstance(other, Vector3D):
            if len(self.values) == len(other.values):
                return Vector3D(*tuple(map(lambda x, y: x * y, self.values, other.values)))
            else:
                raise Exception('Vector: error, multiplication with vectors with different size!')
        elif isinstance(other, Vector):
            if len(self.values) == len(other.values):
                return Vector(*tuple(map(lambda x, y: x * y, self.values, other.values)))
            else:
                raise Exception('Vector: error, multiplication with vectors with different size!')
        else:
            raise Exception('Vector: error, multiplication with not vector, int or float!')

    def __floordiv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            if other:
                return Vector(*tuple(map(lambda x: x // other, self.values)))
            else:
                raise Exception('Vector: error, division with zero!')
        elif isinstance(other, Vector):
            if len(self.values) == len(other.values):
                for i in range(len(other.values)):
                    if not other.values[i]:
                        raise Exception('Vector: error, division with zero!')
                return Vector(*tuple(map(lambda x, y: x // y, self.values, other.values)))
            else:
                raise Exception('Vector: error, division with vectors with different size!')
        else:
            raise Exception('Vector: error, division with not vector, int or float!')

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            if other:
                return Vector(*tuple(map(lambda x: x / other, self.values)))
            else:
                raise Exception('Vector: error, division with zero!')
        elif isinstance(other, Vector):
            if len(self.values) == len(other.values):
                for i in range(len(other.values)):
                    if not other.values[i]:
                        raise Exception('Vector: error, division with zero!')
                return Vector(*tuple(map(lambda x, y: x / y, self.values, other.values)))
            else:
                raise Exception('Vector: error, division with vectors with different size!')
        else:
            raise Exception('Vector: error, division with not vector, int or float!')

    def normalize(self):
        mag = self.magnitude()
        if mag > 0:
            tmpValues = map(lambda x: x / mag, self.values)
            self.values = tmpValues
        else:
            raise Exception('Vector: error, normalizing with zero!')

    def dot(self, v):
        if isinstance(v, Vector):
            if len(v.values) == len(self.values):
                return sum([x * y for x, y in zip(v.values, self.values)])
            else:
                raise Exception('Vector: error, dot product between vectors with wrong size!')
        else:
            raise Exception('Vector: error, dot product not with a vector!')


class Vector3D(Vector):
    def __init__(self, x=0, y=0, z=0, w=1):
        Vector.__init__(self, x, y, z, w)

    def cross(self, v):
        if isinstance(v, Vector):
            if v.size() == 3:
                return Vector3D(self.values[1] * v.values[2] - self.values[2] * v.values[1],
                                self.values[2] * v.values[0] - self.values[0] * v.values[2],
                                self.values[0] * v.values[1] - self.values[1] * v.values[0])
            else:
                raise Exception('Vector3D: error, dot product between vectors with wrong size!')
        else:
            raise Exception('Vector3D: error, dot product not with a vector!')


class Matrix:

    def __init__(self, *args, createIdentity=True):
        if len(args):
            if isinstance(args[0], list):
                tmpList = args[0]

                if not isinstance(tmpList[0], list):
                    raise Exception('Matrix: error, initialization with wrong type!')

                self.rows = len(tmpList)
                self.cols = len(tmpList[0])

                self.mat = [[0.0] * self.cols for x in range(self.rows)]

                for i in range(self.rows):
                    if len(tmpList[i]) != self.cols:
                        raise Exception('Matrix: error, cols are not same length!')
                    for j in range(self.cols):
                        if isinstance(tmpList[i][j], float) or isinstance(tmpList[i][j], int):
                            self.mat[i][j] = tmpList[i][j]
                        else:
                            raise Exception('Matrix: error, element on {}, {} is not int or float'.format(i, j))
            else:
                rows = args[0]
                cols = args[1]
                if len(args) > 2:
                    createIdentity = args[2]
                if rows < 1 or cols < 1:
                    raise Exception('Matrix: error, invalid number of columns or rows!')
                self.rows = rows
                self.cols = cols

                self.mat = [[0.0] * cols for x in range(rows)]

                if self.isQuadratic() and createIdentity:
                    for i in range(self.rows):
                        self.mat[i][i] = 1.0

    def __str__(self):
        s = ''
        for row in self.mat:
            s += '%s\n' % row
        return s

    def copy(self):
        cpy = Matrix(self.rows, self.cols, False)
        for i in range(self.rows):
            for j in range(self.cols):
                cpy.mat[i][j] = self.mat[i][j]
        return cpy

    def __getitem__(self, index):
        if self.rows > index[0] >= 0 <= index[1] < self.cols:
            return self.mat[index[0]][index[1]]
        else:
            raise Exception('Matrix: error, getitem, index problem!')

    def __setitem__(self, index, val):
        if self.rows > index[0] >= 0 <= index[1] < self.cols:
            self.mat[index[0]][index[1]] = val
        else:
            raise Exception('Matrix: error, setitem, index problem!')

    def rowsNum(self):
        return self.rows

    def colsNum(self):
        return self.cols

    def getRow(self, i):
        if 0 <= i < self.rows:
            return Exception('Matrix: error, row(i) index problem!')

    def getCol(self, j):
        if 0 <= j < self.cols:
            return [row[j] for row in self.mat]
        else:
            raise Exception('Matrix: error, col(i) index problem!')

    def __add__(self, other):
        if isinstance(other, Matrix):
            if self.cols == other.cols and self.rows == other.rows:
                r = Matrix(self.rows, self.cols, False)
                for i in range(self.rows):
                    for j in range(self.cols):
                        r.mat[i][j] = self.mat[i][j] + other.mat[i][j]
                return r
            else:
                raise Exception('Matrix: error, add(), matrices are not of the same type!')
        else:
            raise Exception('Matrix: error, add operand is not a matirx!')

    def __sub__(self, other):
        if isinstance(other, Matrix):
            if self.cols == other.cols and self.rows == other.rows:
                r = Matrix(self.rows, self.cols, False)
                for i in range(self.rows):
                    for j in range(self.cols):
                        r.mat[i][j] = self.mat[i][j] - other.mat[i][j]
                return r
            else:
                raise Exception('Matrix: error, sub(), matrices are not of the same type!')
        else:
            raise Exception('Matrix: error, sub operand is not a matirx!')

    def __mul__(self, other):
        if isinstance(other, Matrix):
            if self.cols == other.rows:
                r = Matrix(self.rows, other.cols, False)
                for i in range(self.rows):
                    for j in range(other.cols):
                        for k in range(self.cols):
                            r.mat[i][j] += self.mat[i][k] * other.mat[k][j]
                return r
            else:
                raise Exception('Matrix: error, matrix multiplication with incomatible matrix!')
        elif isinstance(other, Vector3D):
            if self.cols == other.size():
                r = [0] * self.cols
                for i in range(self.rows):
                    for j in range(other.size()):
                        r[i] += self.mat[i][j] * other[j]
                r[:] = [r[x] / r[3] for x in range(len(r))]
                return Vector3D(*tuple(r))
            else:
                raise Exception('Matrix: error, matrix multiplication with incompatible vector!')
        elif isinstance(other, Vector):
            if self.cols == other.size():
                r = [0] * self.cols
                for i in range(self.rows):
                    for j in range(other.size()):
                        r[i] += self.mat[i][j] * other[j]
                return Vector(*tuple(r))
            else:
                raise Exception('Matrix: error, matrix multiplication with incompatible vector!')
        elif isinstance(other, int) or isinstance(other, float):
            r = Matrix(self.rows, self.cols, False)
            for i in range(self.rows):
                for j in range(self.cols):
                    r.mat[i][j] = self.mat[i][j] * other
            return r
        else:
            raise Exception('Matrix: error, matrix multiplication with incompatible type!')

    def isQuadratic(self):
        return self.rows == self.cols

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            r = Matrix(self.rows, self.cols, False)
            for i in range(self.rows):
                for j in range(self.cols):
                    r.mat[i][j] = self.mat[i][j] / other
            return r
        else:
            raise Exception('Matrix: error, matrix division with not int or float!')

    def __floordiv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            r = Matrix(self.rows, self.cols, False)
            for i in range(self.rows):
                for j in range(self.cols):
                    r.mat[i][j] = self.may[i][j] // other
            return r
        else:
            raise Exception('Matrix: error, matrix division with not int or float!')

    def transpose(self):
        t = Matrix(self.cols, self.rows, False)
        for j in range(self.cols):
            for i in range(self.rows):
                t.mat[j][i] = self.mat[i][j]

        return t

    def det(self):
        if not self.isQuadratic():
            raise Exception('Matrix: error, determinant of non-quadratic matrix!')
        if self.rows == 2:
            return self.mat[0][0] * self.mat[1][1] - self.mat[0][1] * self.mat[1][0]

        return self.expandByMinorsOnRow(0)

    def expandByMinorsOnRow(self, row):
        assert (row < self.rows)
        d = 0
        for col in range(self.cols):
            d += (-1) ** (row + col) * self.mat[row][col] * self.minor(row, col).det()

        return d

    def expandByMinorsOnRow(self, col):
        assert (col < self.cols)
        d = 0
        for row in range(self.rows):
            d += (-1) ** (row + col) * self.mat[row][col] * self.minor(row, col).det()

        return d

    def minor(self, i, j):
        if i < 0 or i >= self.rows:
            raise Exception('Matrix: error, Determinant-row value is out of range!')
        if j < 0 or j >= self.cols:
            raise Exception('Matrix: error, Determinant-row value is out of range!')

        # Nova matica s rozmermy row - 1 col - 1

        mat = Matrix(self.rows - 1, self.cols - 1)

        minor_row = minor_col = 0

        for self_row in range(self.rows):
            if not self_row == i:  # Preskocenie i teho riadku
                for self_col in range(self.cols):
                    if not self_col == j:
                        mat.mat[minor_row][minor_col] = self.mat[self_row][self_col]
                        minor_col += 1

                minor_col = 0
                minor_row += 1
        return mat

    def invert(self):
        if not self.isQuadratic():
            raise Exception('Matrix: error, determinant of non-quadratic matrix!')
        else:
            N = self.cols
            # Jednotkova matica
            mat = Matrix(N, N)
            # Kopia povodnej matice
            mo = self.copy()

            for column in range(N):
                if (mo.mat[column][column] == 0):
                    big = column
                    for row in range(N):
                        if (math.fabs(mo.mat[row][column]) > math.fabs(mo.m[big][column])):
                            big = row

                    if big == column:
                        print(self)
                        print('Is singular matrix')
                    else:
                        for j in range(N):
                            mo.mat[column][j], mo.mat[big][j] = mo.mat[big][j], mat.mat[column][j]
                            mat.mat[column][j], mat.mat[big][j] = mat.mat[big][j], mat.mat[column][j]

                for row in range(N):
                    if row != column:
                        coeff = mo.mat[row][column] / mo.mat[column][column]
                        if coeff != 0:
                            for j in range(N):
                                mo.mat[row][j] -= coeff * mo.mat[column][j]
                                mat.mat[row][j] -= coeff * mat.mat[column][j]

                            mo.mat[row][column] = 0

            for row in range(N):
                for column in range(N):
                    mat.mat[row][column] /= mo.mat[row][row]

            return mat

'''
matTest = Matrix([
    [2,-4, 6],
    [3,-5, 8],
    [-2,6,-10] ])
print(matTest.invert())

print(matTest.invert())
vector1 = Vector(1, 2, 3)
vector2 = Vector(0.5, 2, 4)
print(2 / 3)
vector3 = vector1 / vector2

mat = Matrix(3, 3)
mat1 = Matrix(3, 3)
mat1[(2, 2)] = 2
mat[(2, 2)] = 2
print(mat1)
mat2 = mat * mat1 * 2
print(mat2)
vector3 = mat2 * vector1
print(vector3)


testDet = Matrix(3, 3, False)

testDet.mat[0] = [2,-4, 6]
testDet.mat[1] = [3,-5, 8]
testDet.mat[2] = [-2,6,-10]

print(testDet.invert())
'''
