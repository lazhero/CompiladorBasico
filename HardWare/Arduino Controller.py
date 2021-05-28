import time
from pyfirmata2 import Arduino, util, OUTPUT

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

columns = [d_pin_6, d_pin_11, d_pin_10, d_pin_3, a_pin_3, d_pin_4, d_pin_8, d_pin_9]

rows = [d_pin_2, d_pin_7, a_pin_5, d_pin_5, d_pin_13, a_pin_4, d_pin_12, a_pin_2]

matrix = [[0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 1, 0, 0, 1, 0, 0],
          [0, 0, 1, 0, 0, 1, 0, 0],
          [0, 0, 1, 0, 0, 1, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0],
          [0, 1, 0, 0, 0, 0, 1, 0],
          [0, 0, 1, 1, 1, 1, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0]]


def clear():
    for i in range(0, 8):
        rows[i].write(0)
        columns[i].write(1)


def display():
    counter = 0
    while counter < 100:
        for i in range(0, 8):
            columns[i].write(0)
            for j in range(0, 8):
                rows[j].write(matrix[j][i])
            time.sleep(0.0001)
            clear()
        counter += 1


clear()
display()