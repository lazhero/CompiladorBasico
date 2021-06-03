import time
from pyfirmata2 import Arduino, util, OUTPUT

class Arduino_Controller:
    board = Arduino('COM3')
    d_pin_2 = board.get_pin('d:2:o')
    d_pin_3 = board.get_pin('d:3:o')
    d_pin_4 = board.get_pin('d:4:o')
    d_pin_5 = board.get_pin('d:5:o')
    d_pin_6 = board.get_pin('d:6:o')
    d_pin_7 = board.get_pin('d:7:o')
    d_pin_8 = board.get_pin('d:8:o')
    d_pin_9 = board.get_pin('d:9:o')
    d_pin_10 = board.get_pin('d:10:o')
    d_pin_11 = board.get_pin('d:11:o')
    d_pin_12 = board.get_pin('d:12:o')
    d_pin_13 = board.get_pin('d:13:o')

    d_pin_2.mode = OUTPUT
    d_pin_3.mode = OUTPUT
    d_pin_4.mode = OUTPUT
    d_pin_5.mode = OUTPUT
    d_pin_6.mode = OUTPUT
    d_pin_7.mode = OUTPUT
    d_pin_8.mode = OUTPUT
    d_pin_9.mode = OUTPUT
    d_pin_10.mode = OUTPUT
    d_pin_11.mode = OUTPUT
    d_pin_12.mode = OUTPUT
    d_pin_13.mode = OUTPUT

    a_pin_2 = board.get_pin('d:16:o')
    a_pin_3 = board.get_pin('d:17:o')
    a_pin_4 = board.get_pin('d:18:o')
    a_pin_5 = board.get_pin('d:19:o')
    a_pin_2.mode = OUTPUT
    a_pin_3.mode = OUTPUT
    a_pin_4.mode = OUTPUT
    a_pin_5.mode = OUTPUT

    columns = [d_pin_9, d_pin_8, d_pin_4, a_pin_3, d_pin_3, d_pin_10, d_pin_11, d_pin_6]

    rows = [a_pin_2, d_pin_12, a_pin_4, d_pin_13, d_pin_5, a_pin_5, d_pin_7, d_pin_2]

    matrix = [[0, 0, 1, 0, 0, 1, 0, 0],
              [0, 1, 1, 1, 1, 1, 1, 0],
              [0, 1, 1, 1, 1, 1, 1, 0],
              [0, 1, 1, 1, 1, 1, 1, 0],
              [0, 0, 1, 1, 1, 1, 0, 0],
              [0, 0, 0, 1, 1, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0]]

    def clear(self):
        for i in range(0, 8):
            self.rows[i].write(0)
            self.columns[i].write(1)

    def display(self):
        counter = 0
        while counter < 100:
            for i in range(0, 8):
                self.columns[i].write(0)
                for j in range(0, 8):
                    self.rows[j].write(self.matrix[j][i])
                time.sleep(0.0001)
                self.clear()
            counter += 1
        self.clear()

    def change_matrix(self, new_matrix):
        self.fill_matrix(new_matrix)

    def fill_matrix_aux(self, matrix):
        res_matrix = []
        # makes the res_matrix an 8x8 matrix
        for i in range(0, 8):
            res_matrix.append([0, 0, 0, 0, 0, 0, 0, 0])

        # fills the res_matrix with the corresponding data
        for i in range(0, len(matrix)):
            for j in range(0, len(matrix[0])):
                res_matrix[i][j] = matrix[i][j]
        self.matrix = res_matrix
        print(self.matrix)

    def fill_matrix(self, matrix):
        if self.is_valid_matrix(matrix):
            if len(matrix) < 8 or len(matrix[0]) < 8:
                self.fill_matrix_aux(matrix)
            else:
                self.matrix = matrix
        else:
            raise Exception("ERROR, MATRIZ NO ES VALIDA")

    def is_binary_matrix(self, matrix):
        for element in matrix:
            for number in element:
                if number != 0 and number != 1:
                    return False
        return True

    def is_rectangular_matrix(self, matrix):
        num_columns = len(matrix[0])
        for i in range(1, len(matrix)):
            if len(matrix[i]) != num_columns:
                return False
        return True

    def is_valid_matrix(self, matrix):
        if isinstance(matrix, list):
            for element in matrix:
                if not isinstance(element, list):
                    return False
            if not self.is_binary_matrix(matrix):
                return False
            if not self.is_rectangular_matrix(matrix):
                return False

            else:
                return True

        else:
            return False


Arduino_cont = Arduino_Controller()
Arduino_cont.clear()
'''
Arduino_cont.change_matrix(
             [[0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 1, 0, 0, 1, 0, 0],
              [0, 0, 1, 0, 0, 1, 0, 0],
              [0, 0, 1, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 1, 0, 0, 0, 0, 1, 0],
              [0, 0, 1, 1, 1, 1, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0]])
'''
Arduino_cont.display()

