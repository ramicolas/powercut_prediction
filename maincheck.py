


import schedule
import time

def job(t):
    import mailsend
    return

schedule.every().day.at("19:13").do(job,'SENT')

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute