import pycurl
import cStringIO
import numpy as np

buf = cStringIO.StringIO()

c = pycurl.Curl()
c.setopt(c.URL,'https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/horaria/08056/?api_key=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJuaWNvbGFzLm1hcmluZ0BnbWFpbC5jb20iLCJqdGkiOiJjMDAxY2M0Yy1hMzliLTRmOTQtODU4NC01MGEzMmJjM2EzMjIiLCJleHAiOjE1MDgzNDY0ODEsImlzcyI6IkFFTUVUIiwiaWF0IjoxNTAwNTcwNDgxLCJ1c2VySWQiOiJjMDAxY2M0Yy1hMzliLTRmOTQtODU4NC01MGEzMmJjM2EzMjIiLCJyb2xlIjoiIn0.k9TCxoryl6VOMMsf4wiq48nBTm9PnNiBVLTdv8JP7X8')
c.setopt(c.WRITEFUNCTION, buf.write)
c.perform()

a =  buf.getvalue()
#print(a)
buf.close()


#print(len(a))

str = 'datos'
start = a.find(str)

str = 'metadatos'
stop = a.find(str)

a = a[start+10:stop-6]
print(a)


buf = cStringIO.StringIO()

c = pycurl.Curl()
c.setopt(c.URL,a)
c.setopt(c.WRITEFUNCTION, buf.write)
c.perform()

a =  buf.getvalue()
#print(a)
buf.close()


#index of second precipitation (tomorrow)
start = a.find('precipitacion',a.find('precipitacion')+10)
#print(start)
a = a[start:len(a)]
#print(a[0:2000])
dateind = a.find('fecha')
date = a[dateind+10:dateind+20]
print(date)

hours =  np.arange(24)
values =  np.array([])
ind = -5

for i in hours:
  ind = a.find('value',ind+5)
  str = a[ind+7:ind+20]
  i1 = str.find('"')
  i2 = str.find('"',i1+1)
  str=str[i1+1:i2]
  if str=='Ip':
    str=0
  values = np.append(values,float(str))

print(values) 

sum = np.sum(values[0:6])
prob1 = sum*6.03+2.51

sum = np.sum(values[7:12])
prob2 = sum*6.03+2.51

sum = np.sum(values[13:18])
prob3 = sum*6.03+2.51

sum = np.sum(values[19:24])
prob4 = sum*6.03+2.51

message = 'Dear Kutlu, Your powecut forecast for '+date+' is ready.... \nPowercut probabilities are... \nfrom 0 to 6: {}% \nfrom 6 to 12: {}% \nfrom 12 to 18: {}% \nfrom 18 to 24: {}% \n\nYou are welcome\n\nCheers,\nYour secret lover'.format(prob1,prob2,prob3,prob4)
message2print = 'Powecut forecast for '+date+'... \nfrom 0 to 6: {}% \nfrom 6 to 12: {}% \nfrom 12 to 18: {}% \nfrom 18 to 24: {}%'.format(prob1,prob2,prob3,prob4)
print(message2print)

import smtplib

if (prob1>=30) or (prob2>=30) or (prob3>=30) or (prob4>=30):
  server = smtplib.SMTP('smtp.gmail.com:587')
  server.ehlo()
  server.starttls()
  #Next, log in to the server
  server.login("XXXXX", "XXXXX")
  #Send the mail
  #msg = "Your powecut forcast for tomorrow..."+date # The /n separates the message from the headers
  server.sendmail("XXXXX@gmail.com", "XXXXX@gmail.com", message2print)
  server.sendmail("XXXXX@gmail.com", "XXXXX@gmail.com", message)