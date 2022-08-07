from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import os
import subprocess
import json
import re

os.system("termux-wake-lock")
daily_limit = int(input("enter your expected daily expenditure: "))
def check_time(init_time):
    time_t = datetime.strptime(init_time, '%Y-%m-%d %H:%M:%S')
    if time_t.date() < datetime.today().date():
        return True
    return False


#get bulk text_messages from your phone
def get_msg(record):
    raw_msg = subprocess.Popen(f"termux-sms-list -l {record}",shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    out , err = raw_msg.communicate()
    messages = json.loads(out.decode('utf-8'))
    return messages

#'''check if the last 30th message is from yesterday
# if it's not from yesterday, check for the next 15 and stop checking once the last nth message is from yesterday
# this is to help ensure we're getting all messages from 12:00am today,which may or may not include messages from yesterday'''

def get_required_messages():
    list = 30
    while True:
        msgs = get_msg(list)
        if check_time(msgs[0]["received"]):
            return msgs
        list+=15


#'''ensure each message from required_messages is from today, if not extract the ones from today
# this is to remove messages from yesterday. For cases that included messages from the previous day'''
def get_specific_messages():
    textMsg = get_required_messages()
    for each_msg in textMsg:
        time_received = datetime.strptime(each_msg["received"], '%Y-%m-%d %H:%M:%S')
        if time_received.date() == datetime.today().date():
            return textMsg[textMsg.index(each_msg):]

#check for messages that are from banks(i.e alerts)
def access_alerts():
    banks = "UNIONBANK UBA ZENITHBANK ".lower().split()
#    print(banks)
    alerts = []
    day_messages = get_specific_messages()
    try:
        for i in day_messages:
            if i["number"].lower() in banks:
                alerts.append(i)
        return alerts   
    except TypeError as e:
        return "NoMsgs"
#check if alert is credit or debit
def check_alerts():
    alerts = access_alerts()
    if alerts == "NoMsgs":
         return "NoMsgs"
    else:
        cred = []
        deb =[]
        for al in alerts:
            if "cr:" in al["body"].lower() or "txn: credit"  in al["body"].lower():
                cr = re.compile(r'(cr|amt)\w*.?.?\w*.?.?ngn.?\d{1,3}.?\d{1,3}.?\d{1,3}.?\d{1,3}.?\d{1,3}')
                extract_figs = re.compile(r'\d{1,3}.?\d{1,3}.?\d{1,3}.?')
                credit = cr.finditer(al['body'].lower())
                for i in credit:
                    credit_amount = extract_figs.finditer(i.group())
                for i in credit_amount:
                    b = float(i.group().replace(",",""))
                    cred.append(b)
            elif "dr:" in al["body"].lower() or "txn: debit" in al['body'].lower() or "dt:"in al['body'].lower():
                de = re.compile(r'(d|amt)\w*.?.?\w*.?.?ngn.?\d{1,3}.?\d{1,3}.?\d{1,3}.?\d{1,3}')
                extract_figs = re.compile(r'\d{1,3}.?\d{1,3}.?\d{1,3}.?')
                debit = de.finditer(al['body'].lower())
            
                for i in debit:
                    debit_amount = extract_figs.finditer(i.group())
                    for i in debit_amount:
                        b = float(i.group().replace(",",""))
                        deb.append(b)
        total_credit = sum(cred)
        total_debit = sum(deb)
        os.system(f"termux-toast -b green -c blue -g top -s your total amount received today is : \#{total_credit}")
        os.system(f"termux-toast -b green -c blue -g top -s your total amount spent so far today is : \#{total_debit}")
        return total_credit,total_debit





def notif():
    ea = check_alerts()
    if ea == "NoMsgs":
        notification = os.system("termux-toast -b blue -c red -g top -s you have not received any alerts today")
    else:
        credit = ea[0]
        debit = ea[1]

        while datetime.today().date():
            limit = daily_limit
            break
        if debit == 0:
           notification = os.system("termux-toast -b red -c cyan -g top you have zero expenditures as of today")
        else:
            dl_percent = debit / limit * 100
            if dl_percent >= 10:
                notification = os.system("termux-toast -b teal -c red -g top  warning: you have spent at least 10% of your daily expenditure limit")
            elif dl_percent >= 20:
                notification = os.system("termux-toast -b teal -c red -g top  warning: you have spent at least 20% of your daily expenditure limit")
            elif dl_percent >= 30:
                notification = os.system("termux-toast -b teal -c red -g top -s warning: you have spent at least 30% of your daily expenditure limit")
            elif dl_percent >= 50:
                notification = os.system("termux-toast -b teal -c red -g top -s warning: you have spent at least 50% of your daily expenditure limit")
            elif dl_percent >= 75:
                notification = os.system("termux-toast -b teal -c red -g top -s warning: you have spent at least 75% of your daily expenditure limit")
            elif dl_percent == 100:
                notification = os.system("termux-toast -b teal -c red -g top -s warning: you have spent at least 100% of your daily expenditure limit")
            elif dl_percent > 100:
                notification = os.system(f"termux-toast -b teal -c red -g top -s warning: you have spent {round((dl_percent - 100),2)}% more than your daily expenditure limit /n which is {debit - limit}% more than {limit}")
            notification = os.system(f"termux-toast -b teal -c green -g top -s you have spent {round(dl_percent,2)}% of your daily limit \n")
    
        if debit > credit:
            notification = os.system(f"termux-toast -b teal -c red -s -g top you have spent \#{debit - credit} more than your daily income")
        if debit < limit:
            notification = os.system(f"termux-toast -b teal -c brown -g top -s you have \#{limit - debit} left of your daily expenditure for the day")
    return notification

scheduler = BlockingScheduler()
scheduler.add_job(notif, 'interval', minutes = 1)
scheduler.start()
