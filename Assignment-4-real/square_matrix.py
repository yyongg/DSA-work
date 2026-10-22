"""Class for square matrix implementation"""

class SquareMatrix():
    """
    An n x n matrix of floats, stored as a list of rows.
    """
    def __init__(self) -> None:
        """
        Create an empty 0 x 0 matrix. Call zeros(n) to give it a size.
        """
        self.matrix: list[list[float]] = []
        self.size: int = 0

    def zeros(self, n: int) -> None:
        """
        Reset the matrix to an n x n matrix filled with zeros.
        param n the number of rows and columns
        """
        self.matrix = []
        self.size = n
        for _ in range(n):
            self.matrix.append([0]*n)

    def set_elem(self, row: int, col: int, elem: float):
        """
        Set the element at (row, col) to [elem].
        param row the row index, from 0 to size - 1
        param col the column index, from 0 to size - 1
        param elem the value to store
        """
        self.matrix[row][col] = elem

    def get_elem(self,row:int, col:int) -> float:
        """
        Get the element at (row, col).
        param row the row index, from 0 to size - 1
        param col the column index, from 0 to size - 1
        return the value stored at (row, col)
        """
        return self.matrix[row][col]

    def get_row(self, row:int) -> list[float]:
        return self.matrix[row]

    def get_col(self, col:int) -> list[float]:
            res: list[float] = []
            for i in range(self.size):
                res.append(self.matrix[i][col])

            return res
    

    def __add__(self, mat: SquareMatrix) -> SquareMatrix:
        """
        Add two matrices of the same size element by element (self + mat).
        param mat the matrix to add to this one
        return a new matrix where each element is the sum of the
        elements at the same position in self and mat
        """
        if mat.size != self.size:
            raise ValueError("Matrices not same size")

        # Build each row directly from the two rows instead of calling
        # get_elem/set_elem for every element
        res = SquareMatrix()
        res.size = self.size
        res.matrix = [[x + y for x, y in zip(row1, row2)]
                      for row1, row2 in zip(self.matrix, mat.matrix)]

        return res

    def __sub__(self, mat: SquareMatrix) -> SquareMatrix:
        """
        Subtracts two matrices of the same size element by element (self - mat).
        param mat the matrix to subtract to this one
        return a new matrix where each element is the difference of the
        elements at the same position in self and mat
        """
        if mat.size != self.size:
            raise ValueError("Matrices not same size")

        # Build each row directly from the two rows instead of calling
        # get_elem/set_elem for every element
        res = SquareMatrix()
        res.size = self.size
        res.matrix = [[x - y for x, y in zip(row1, row2)]
                      for row1, row2 in zip(self.matrix, mat.matrix)]

        return res

    def div4(self) -> tuple[SquareMatrix,SquareMatrix,SquareMatrix,SquareMatrix]:
        """
        Split the matrix into four (size / 2) x (size / 2) quadrants.
        return the quadrants in the order
        (top-left, top-right, bottom-left, bottom-right)
        """
        half = self.size//2
        mat1 = SquareMatrix()
        mat1.zeros(half)
        mat2 = SquareMatrix()
        mat2.zeros(half)
        mat3 = SquareMatrix()
        mat3.zeros(half)
        mat4 = SquareMatrix()
        mat4.zeros(half)

        for i in range(half):
            for j in range(half):
                mat1.set_elem(i,j, self.get_elem(i,j))
                mat2.set_elem(i,j, self.get_elem(i,j + half))
                mat3.set_elem(i,j, self.get_elem(i + half,j))
                mat4.set_elem(i,j, self.get_elem(i + half,j + half))

        return mat1, mat2, mat3, mat4

    def __mul__(self, mat: SquareMatrix) -> SquareMatrix:
        if mat.size != self.size:
            raise ValueError("Matrices not same size")

        res = SquareMatrix()
        res.zeros(self.size)

        for i in range(self.size):
            for j in range(self.size):
                row = self.get_row(i)
                col = mat.get_col(j)
                res.set_elem(i,j, sum([x * y for x, y in zip(row, col)]))

        return res

    def strassen_multiply(self, mat: SquareMatrix) -> SquareMatrix:
        """
        Multiply two matrices of the same size (self * mat) using Strassen's
        algorithm. Each matrix is split into four quadrants, and the result
        is built from 7 recursive multiplications of the quadrants instead of
        the usual 8, giving O(n^2.81) time instead of O(n^3).
        Matrices of size 64 or smaller are multiplied with regular
        multiplication, since it is faster at small sizes.
        The size must be a power of 2.
        param mat the matrix to multiply this one by
        return a new matrix equal to self * mat
        """
        if mat.size != self.size:
            raise ValueError("Matrices not same size")

        if self.size <= 64:
            return self*mat

        a11, a12, a21, a22 = self.div4()
        b11, b12, b21, b22 = mat.div4()

        # calculate p1
        s: SquareMatrix = a11 + a22
        p1 = s.strassen_multiply(b11 + b22)

        # calculate p2
        s = a21 + a22
        p2 = s.strassen_multiply(b11)

        # calculate p3
        p3 = a11.strassen_multiply(b12 - b22)

        # calculate p4
        p4 = a22.strassen_multiply(b21 - b11)

        # calculate p5
        s = a11 + a12
        p5 = s.strassen_multiply(b22)

        # calculate p6
        s = a21 - a11
        p6 = s.strassen_multiply(b11 + b12)

        # calculate p7
        s = a12 - a22
        p7 = s.strassen_multiply(b21 + b22)

        # calculate c1
        c11 = p1 + p4 - p5 + p7
        c12 = p3 + p5
        c21 = p2 + p4
        c22 = p1 - p2 + p3 + p6

        # combine quadrants
        res = SquareMatrix()
        full_size = self.size
        half = full_size//2
        res.zeros(full_size)

        for i in range(full_size):
            for j in range(full_size):
                if i < half and j < half:
                    res.set_elem(i,j, c11.get_elem(i,j))
                elif i < half and j >= half:
                    res.set_elem(i,j, c12.get_elem(i,j-half))
                elif i >= half and j < half:
                    res.set_elem(i,j, c21.get_elem(i-half,j))
                elif i >= half and j >= half:
                    res.set_elem(i,j, c22.get_elem(i-half,j-half))

        return res
