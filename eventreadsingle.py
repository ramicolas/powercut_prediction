import csv
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
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


#rain threshold mm
thr = np.arange(20)
#cut probability
cutprob = np.array([])
errcutprob = np.array([])
for threshold in thr:
  path = 'DatosEstaciones'
  #    print filename
  startrecord = 0
  i = 0
  historain = np.array([]) #array with rain data 
  histocoinc = np.array([]) #array with rain data of coincidence events
  # Open weather file
  with open(path+'/0076.csv', 'r') as f:
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
                  if data[12]>=threshold:
                      countRain+=1
                      i=0
                      historain=np.append(historain,data[12])
                      for date in dates:
                          if date == data[1]:
                              if hours[i]<6:
                                  histocoinc=np.append(histocoinc,data[12])
                          i+=1
                  if data[13]>=threshold:
                      countRain+=1
                      i=0
                      historain=np.append(historain,data[13])
                      for date in dates:
                          if date == data[1]:
                              if hours[i]>=6 and hours[i]<12:
                                  histocoinc=np.append(histocoinc,data[13])
                          i+=1                            
                  if data[14]>=threshold:
                      countRain+=1
                      i=0
                      historain=np.append(historain,data[14])
                      for date in dates:
                          if date == data[1]:
                              if hours[i]>=12 and hours[i]<18:
                                  histocoinc=np.append(histocoinc,data[14])
                          i+=1
                  if data[15]>=threshold:
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
  #print(coincpers)
  if coincpers>0:
      coincrainpers = float(len(histocoinc))/len(historain)*100
      errcoincrainpers = coincrainpers*np.sqrt(1/float(len(histocoinc))+1/float(len(historain)))
      print(coincrainpers)
      print(errcoincrainpers)
  
      g2 = float(len(histocoinc))*float(len(histocoinc))/len(dates)/len(historain)
      #if g2>0.045:
          #print([data[0],coincpers,coincrainpers,g2])
      #print(g2)
  result.append([data[0],coincpers,coincrainpers,g2])
  
  #print(historain)
  #print(histocoinc)
  #plt.hist(historain, np.floor(np.amax(historain)), facecolor='green', alpha=0.75)
  #plt.hist(histocoinc, np.floor(np.amax(histocoinc)), facecolor='red', alpha=0.75)
  #plt.show()
  
  f.close()
  my_file.close()
  
  #print result
  
  #cut probability
  cutprob = np.append(cutprob,coincrainpers)
  errcutprob = np.append(errcutprob,errcoincrainpers)
  
  
z = np.polyfit(thr,cutprob,1)
print(z)
fit = thr*z[0]+z[1]
  
plt.figure()
plt.errorbar(thr, cutprob, xerr=0, yerr=errcutprob,fmt='o')
plt.plot(thr,fit)
plt.show()