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
              [0, 1, 0, 1, 1, 0, 1, 0]]

    def change_matrix(self, new_matrix):
        self.fill_matrix(new_matrix)

    def fill_matrix_aux(self, new_matrix):
        res_matrix = []
        # makes the res_matrix an 8x8 matrix
        for i in range(0, 8):
            res_matrix.append([0, 0, 0, 0, 0, 0, 0, 0])
        
        # fills the res_matrix with the corresponding data
        if self.is_valid_matrix(new_matrix):
            for i in range(0, len(new_matrix)):
                for j in range(0, len(new_matrix[0])):
                    res_matrix[i][j] = int(new_matrix[i][j])
        #fills the res_matrix with the only led to write to
        else:
            row = new_matrix//8
            col = new_matrix%8
            res_matrix[row][col] = 1
        return res_matrix
    def fill_matrix_aux_val(self, new_matrix,value):
        res_matrix = []
        # makes the res_matrix an 8x8 matrix
        for i in range(0, 8):
            res_matrix.append([0, 0, 0, 0, 0, 0, 0, 0])
        
        # fills the res_matrix with the corresponding data
        if self.is_valid_matrix(new_matrix):
            for i in range(0, len(new_matrix)):
                for j in range(0, len(new_matrix[0])):
                    res_matrix[i][j] = int(new_matrix[i][j])
        #fills the res_matrix with the only led to write to
        else:
            row = new_matrix//8
            col = new_matrix%8
            res_matrix[row][col] = value
        return res_matrix

    def fill_matrix(self, new_matrix):
        if self.is_valid_matrix(new_matrix):
            if len(new_matrix) < 8 or len(new_matrix[0]) < 8:
                return self.fill_matrix_aux(new_matrix)
            else:
                return new_matrix
        elif isinstance(new_matrix,int):
            if new_matrix>64 or new_matrix<0:
                raise Exception("ERROR, MATRIZ NO ES VALIDA")
            else:
                return self.fill_matrix_aux(new_matrix)
        elif isinstance(new_matrix,list):
            temp = [new_matrix]
            return self.fill_matrix_aux(temp)
        else:
            raise Exception("ERROR, MATRIZ NO ES VALIDA")
    
    def fill_matrix_val(self, new_matrix, value):
        if self.is_valid_matrix(new_matrix):
            if len(new_matrix) < 8 or len(new_matrix[0]) < 8:
                return self.fill_matrix_aux_val(new_matrix)
            else:
                return new_matrix
        if isinstance(new_matrix,int):
            if new_matrix>64 or new_matrix<0:
                raise Exception("ERROR, MATRIZ NO ES VALIDA")
            else:
                return self.fill_matrix_aux_val(new_matrix,value)
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

def write_matrix_to_arduino(matrix):
    row = 0
    data_rec = ""
    while data_rec != "8":
        if data_rec == "8\n":
            break
        try:
            row = int(data_rec)
        except:
            pass
        if row == 8:
            break
        msg = "fill_matrix,"+str(row)+","
        for i in range(0,8):
            msg = msg+str(matrix[row][i])
        serial_port.write(msg.encode('ascii'))
        data_rec = serial_port.readline().decode('ascii')
    
def BLINK(data, time, time_unit, state):
    helper = Led_Matrix()
    matrix_to_send = helper.fill_matrix(data)
    msg = "blink,"+str(time)+","
    #add time unit to msg
    if time_unit == "Seg":
        msg = msg + str(1) + ","
    elif time_unit == "Min":
        msg = msg + str(2) + ","
    elif time_unit == "Mil":
        msg = msg + str(0) + ","
    else:
        raise Exception("NOT VALID TIME UNIT")
    #add state to msg
    if state == True:
        msg = msg + str(1)
    elif state == False:
        msg = msg + str(0)
    else:
        raise Exception("NOT VALID STATE")
    write_matrix_to_arduino(matrix_to_send)
    serial_port.write(msg.encode('ascii'))

def DELAY(_time, time_unit):
    if time_unit == "Seg":
        time.sleep(_time)
    elif time_unit == "Min":
        time.sleep(_time*60)
    elif time_unit == "Mil":
        time.sleep(_time/1000)
    else:
        raise Exception("NOT VALID TIME_UNIT")

def NEG(data):
    if isinstance(data, bool):
        if data == True:
            return False
        return True
    elif isinstance(data, list):
        res = []
        for element in data:
            if element == True:
                res.append(False)
            else:
                res.append(True)
        return res

def PRINT_LED(col, row, value):
    index = row*8+col
    helper = Led_Matrix()
    if value == True:
        mat_to_send = helper.fill_matrix_val(index, 1)
    elif value == False:
        mat_to_send = helper.fill_matrix_val(index, 0)
    else:
        raise Exception("Value is not valid")
    write_matrix_to_arduino(mat_to_send)
    
def PRINT_LED_X(type,index,values):
    helper = Led_Matrix()
    mat_to_send = helper.fill_matrix_val(0,0)
    if type == "F":
        for i in range(0,len(values)):
            if values[i] == True:
                mat_to_send[index][i] = 1
            else:
                mat_to_send[index][i] = 0
    elif type == "C":
        for i in range(0,len(values)):
            if values[i] == True:
                mat_to_send[i][index] = 1
            else:
                mat_to_send[i][index] = 0
    elif type == "M":
        for i in range(0,len(values)):
            for j in range(0,len(values[i])):
                if values[i][j] == True:
                    mat_to_send[i][j] = 1
                else:
                    mat_to_send[i][j] = 0
    else:
        raise Exception("ERROR EN TIPO DE OBJETO")
    write_matrix_to_arduino(mat_to_send) 

def LIST(n):
    return list(n)

def test():
    BLINK(55,1000,"Mil",True)

