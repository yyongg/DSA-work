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

        res = SquareMatrix()
        res.zeros(self.size)
        for i in range(self.size):
            for j in range(self.size):
                s = self.get_elem(i,j) + mat.get_elem(i,j)
                res.set_elem(i, j, s)

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


