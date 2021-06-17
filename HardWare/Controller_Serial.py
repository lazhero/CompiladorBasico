from tkinter import EXCEPTION
import serial, time, sys
sys.tracebacklimit = 1
try:
    serial_port = serial.Serial('COM3',baudrate=57600, timeout=1)
except:
    print("NO SE CONECTO EL ARDUINO")

class Led_Matrix:
    F_matrix=[[0, 0, 1, 0, 0, 1, 0, 0],
              [0, 1, 1, 1, 1, 1, 1, 0],
              [0, 1, 1, 1, 1, 1, 1, 0],
              [0, 1, 1, 1, 1, 1, 1, 0],
              [0, 0, 1, 1, 1, 1, 0, 0],
              [0, 0, 0, 1, 1, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0]]

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
            msg = msg+str(int(matrix[row][i]))
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
        return not data
    elif isinstance(data, list):
        res = []
        for element in data:
            element = NEG(element)
            res.append(element)
        return res
    else:
        raise Exception("data not valid")

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

def INSERT(matrix, boolean_list,type,index):
    helper = Led_Matrix()
    new_matrix = helper.fill_matrix_val(0,0)
    bool_list = boolean_list
    while len(boolean_list)<8:
        bool_list.append(0)
    #filas
    if type == 0:
        for i in range(0,len(matrix)+1):
            if i < index:
                new_matrix[i] = matrix[i]
            elif i == index:
                new_matrix[i] = bool_list
            else:
                try:
                    new_matrix[i] = matrix[i-1]
                except:
                    new_matrix.append([0,0,0,0,0,0,0,0])
                    new_matrix[i] = matrix[i-1]
    #columnas
    elif type == 1:
        for i in range(0, len(matrix)):
            for j in range(0, len(matrix[i])+1):
                if j < index:
                    new_matrix[i][j] = matrix[i][j]
                elif i == index:
                    new_matrix[i][j] = bool_list[j]
                else:
                    try:
                        new_matrix[i][j] = matrix[i][j-1]
                    except:
                        for r in new_matrix:
                            r.append(0)
                        new_matrix[i][j] = matrix[i][j-1]
    for r in new_matrix:
        while len(r)<8:
            r.append(0)
    return helper.fill_matrix_aux(new_matrix)

def TYPE(n):
    return type(n)

def LEN(n):
    return len(n)

def RANGE(num, boolean):
    _list = []
    for i in range(0,num):
        _list += [boolean]
    return _list

def SHAPE_F(matrix):
    return len(matrix)

def SHAPE_C(matrix):
    return len(matrix[0])

def T(data):
    if isinstance(data,bool):
        return True
    else:
        for i in range(0,len(data)):
            if isinstance(data[i],list):
                T(data[i])
            else:
                data[i] = True
        return data

def F(data):
    if isinstance(data,bool):
        return False
    else:
        for i in range(0,len(data)):
            if isinstance(data[i],list):
                T(data[i])
            else:
                data[i] = False
        return data

def index_in_all_columns(matrix,index):
    for rows in matrix:
        if len(rows)<=index:
            return False
    return True

def DELETE(matrix, index, type):
    #filas
    if type == 0:
        if index < len(matrix):
            matrix.pop(index)
            return matrix
    #columnas
    elif type == 1:
        if index_in_all_columns(matrix,index):
            for row in matrix:
                row.pop(index)
            return matrix
    raise Exception("INIDICE NO ES VALIDO")

def columnAccess(lista,index):
    columnList=[]
    for i in range(len(lista)):
        columnList+=lista[i][index]
    return columnList

def TEC():
    msg = "tec"
    res = ""
    while True:
        if res != "":
            break
        serial_port.write(msg.encode('ascii'))
        res = serial_port.readline().decode('ascii')
def HEART():
    msg = "heart"
    res = ""
    while True:
        if res != "":
            break
        serial_port.write(msg.encode('ascii'))
        res = serial_port.readline().decode('ascii')
def SMILE():
    msg = "smile"
    res = ""
    while True:
        if res != "":
            break
        serial_port.write(msg.encode('ascii'))
        res = serial_port.readline().decode('ascii')
