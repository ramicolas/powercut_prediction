import re
import csv
import matplotlib.pyplot as plt
import numpy as np


from xlrd import open_workbook

x =  np.array([])
y =  np.array([])
nameid = []
wb = open_workbook('ListadoEstaciones2017-02.xlsx')
for sheet in wb.sheets():
    number_of_rows = sheet.nrows
    number_of_columns = sheet.ncols

    items = []

    rows = []
    for row in range(1, number_of_rows):
        values = []
        for col in range(number_of_columns):
            value  = (sheet.cell(row,col).value)
            values.append(value)
        nameid.append(values[0])
        strx = values[5]
        sx = re.findall(r'\d+',values[5])
        if strx[6] == 'N':
            x=np.append(x,float(sx[0]))
        if strx[6] == 'S':
            x=np.append(x,-float(sx[0]))
        stry = values[6]
        sy = re.findall(r'\d+',values[6])
        if stry[6] == 'E':
            y=np.append(y,float(sy[0]))
        if stry[6] == 'W':
            y=np.append(y,-float(sy[0]))

plt.scatter(y, x)
plt.show()

