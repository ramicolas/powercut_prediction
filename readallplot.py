import re
import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import numpy as np
import os
import glob

from xlrd import open_workbook



countRain = 0

result = []

dates = [] #array event date
hours = [] #array event hour

# Open events file
with open('events2.txt', 'r') as my_file:
    events = csv.reader(my_file, delimiter=',')
    for row in events:
        event = row
        dates.append(event[0])
        hours.append(float(event[1]))


path = 'DatosEstaciones'
for filename in os.listdir(path):
#    print filename
  startrecord = 0
  i = 0
  historain = np.array([]) #array with rain data 
  histocoinc = np.array([]) #array with rain data of coincidence events
  # Open weather file
  with open(path+'/'+filename, 'r') as f:
      datas = csv.reader(f, delimiter=';')
      header = next(datas) #header
      for row in datas:    #start from second row
          data = row
          if data[1] == '2015-10-03':
              startrecord = 1
          if data[12] == '':
              data[12] = 0
          if data[13] == '':
              data[13] = 0
          if data[14] == '':
              data[14] = 0
          if data[15] == '':
              data[15] = 0
          data[12] = float(data[12]) #convert to float
          data[13] = float(data[13])
          data[14] = float(data[14])
          data[15] = float(data[15])
          data[11] = data[12]+data[13]+data[14]+data[15]
          if startrecord == 1:
              if data[11]>0:              #if there is recorded rain on day
                  #print data[1]
                  if data[12]>0:
                      countRain+=1
                      i=0
                      historain=np.append(historain,data[12])
                      for date in dates:
                          if date == data[1]:
                              if hours[i]<6:
                                  histocoinc=np.append(histocoinc,data[12])
                          i+=1
                  if data[13]>0:
                      countRain+=1
                      i=0
                      historain=np.append(historain,data[13])
                      for date in dates:
                          if date == data[1]:
                              if hours[i]>=6 and hours[i]<12:
                                  histocoinc=np.append(histocoinc,data[13])
                          i+=1                            
                  if data[14]>0:
                      countRain+=1
                      i=0
                      historain=np.append(historain,data[14])
                      for date in dates:
                          if date == data[1]:
                              if hours[i]>=12 and hours[i]<18:
                                  histocoinc=np.append(histocoinc,data[14])
                          i+=1
                  if data[15]>0:
                      countRain+=1
                      i=0
                      historain=np.append(historain,data[15])
                      for date in dates:
                          if date == data[1]:
                              if hours[i]>=18:
                                  histocoinc=np.append(histocoinc,data[15])
                          i+=1  
  #print countRain
  #print historain
  #print histocoinc
  
  coincpers = float(len(histocoinc))/len(dates)*100
  #print coincpers
  if coincpers>0:
      coincrainpers = float(len(histocoinc))/len(historain)*100
      #print coincrainpers
  
      g2 = float(len(histocoinc))*float(len(histocoinc))/len(dates)/len(historain)
      #if g2>0.045:
          #print [data[0],coincpers,coincrainpers,g2]
      #print g2
  result.append([data[0],coincpers,coincrainpers,g2])

  f.close()
  my_file.close()
#print result





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



j = 0
k = 0
z =  np.array([])
for name in nameid:
#  print(name)
  for row in result:
    temp = row
    if temp[0]==name:
      #print("match")
      k+=1
      z = np.append(z,temp[3])
  j+=1
  
if j==k:
  print("name match")
 
fig = plt.figure()
#fig.patch.set_facecolor('black')
plt.scatter(y,x,c=z,s=60, cmap='copper', edgecolors='none')
plt.show()