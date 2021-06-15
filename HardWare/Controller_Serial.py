import serial, time

serial_port = serial.Serial('COM3',baudrate=57600, timeout=1)
class Led_Matrix:
    matrix = [[0, 0, 1, 0, 0, 1, 0, 0],
              [0, 1, 1, 1, 1, 1, 1, 0],
              [0, 1, 1, 1, 1, 1, 1, 0],
              [0, 1, 1, 1, 1, 1, 1, 0],
              [0, 0, 1, 1, 1, 1, 0, 0],
              [0, 0, 0, 1, 1, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 1]]

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

    def change_flag(self):
        if self.Flag == True:
            self.Flag = False
        else:
            self.Flag = True

    def time_to_sec(self, time, time_unit):
        if time_unit == "Seg":
            return time
        elif time_unit == "Mil":
            return time/1000
        elif time_unit == "Min":
            return time*60

    def matrix_to_list(self):
        led_list = []
        for rows in Led_Matrix.matrix:
            for state in rows:
                led_list.append(state)
        return led_list

def write_list_to_arduino(_list):
    msg = ""
    for i in range(0,8):
        for j in range(0,8):
            msg = msg+str(Led_Matrix.matrix[i][j])
    return msg
    
def blink():
    
    test = Led_Matrix()
    counter = 0
    while counter < 5:
        counter+=1
        time.sleep(1)    
        matrix = write_list_to_arduino(test.matrix_to_list())

        try:
            print(serial_port.readline().decode('ascii'))
        except:
            pass

blink()
