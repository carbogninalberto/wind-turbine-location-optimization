'''
src/utils.py

this file contains functions and classed used in computation
'''


'''
This function convert a matrix into a vector
'''
def matrix_to_vector(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    res = []
    for row in matrix:
        for element in row:
            res.append(element)
    
    return res, rows, cols

'''
This function convert a vector into a matrix
'''
def vector_to_matrix(vector, n_rows, n_cols):
    matrix = []
    row = []

    for i in range(len(vector)):        
        if i%n_cols == 0 and i != 0:
            matrix.append(row)
            row = [vector[i]]
        else:
            row.append(vector[i])

    matrix.append(row)

    return matrix

'''
This class defines the genotype of the problem.
- matrix: default initialized as a 2x2 with zero values
'''
class Genotype():
    def __init__(self, matrix=[[0, 0], [0, 0]]):
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0])
        self.matrix_vector = matrix_to_vector(self.matrix)[0]

    '''
    accept **kwargs:
    - matrix, [[1, 2, ..., n], ..., m] or
    - vector = [1, 2, ..., n]
    '''
    def update_values(self, **kwargs):
        if kwargs.get('matrix', '') != '':
            self.matrix = kwargs.get('matrix', '')
            self.matrix_vector = matrix_to_vector(self.matrix)
            return True

        elif kwargs.get('vector', '') != '':
            self.matrix_vector = kwargs.get('vector', '')
            self.matrix =  vector_to_matrix(self.matrix_vector, self.rows, self.cols)
            return True
        
        return False
            


if __name__ == "__main__":
    a = [list(range(5))]*4
    print(a)
    conv = matrix_to_vector(a)[0]
    print(conv)
    print(vector_to_matrix(conv, 4, 5))

    print(" CLASS ")
    gen = Genotype(matrix=a)

    print("matrix: ", gen.matrix, " \nvector: ", gen.matrix_vector)

    b = [i*5 for i in conv]
    print("by scalar: ", b)

    print(gen.update_values(vector=b))

    print("matrix: ", gen.matrix, " \nvector: ", gen.matrix_vector)

