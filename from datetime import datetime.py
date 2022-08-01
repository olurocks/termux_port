from datetime import datetime
import os
import subprocess
import json
import re


def check_time(init_time):
    time_t = datetime.strptime(init_time, '%Y-%m-%d %H:%M:%S')
    if time_t.date() < datetime.today().date():
        return True
    return False

def get_msg(record):
    raw_msg = subprocess.Popen(f"termux-sms-list -l {record}",shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    out , err = raw_msg.communicate()
    messages = json.loads(out.decode('utf-8'))
    return messages

def get_required_messages():
    list = 30
    while True:
        msgs = get_msg(list)
        if check_time(msgs[0]["received"]):
            return msgs
        list+=15

def get_specific_messages():
    textMsg = get_required_messages()
    for each_msg in textMsg:
        time_received = datetime.strptime(each_msg["received"], '%Y-%m-%d %H:%M:%S')
        if time_received.date() == datetime.today().date():
            return textMsg[textMsg.index(each_msg):]

def access_alerts():
    banks = "UNIONBANK UBA ZENITHBANK ".lower().split()
    alerts = []
    day_messages = get_specific_messages()
    for i in day_messages:
        if i["number"].lower() in banks:
            alerts.append(i)    
    return alerts   

def check_alerts():
    alerts = access_alerts()
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
                    # b = float(i.group().replace(",",""))
                    b = float(i.group().replace(",",""))
                    deb.append(b)
    total_credit = sum(cred)
    total_debit = sum(deb)
    print("your total amount received today is :",sum(cred))
    print("your total amount spent so far today is :",sum(deb))
    return total_credit,total_debit

def notif():
    ea = check_alerts()
    credit = ea[0]
    debit = ea[1]
    percent = debit/credit * 100
    print(f"your percentage expenditure is {percent}%" )
    if percent < 20:
        return print(f"your percentage expenditure is {percent}%")
    elif percent <=50:
        os.system("termux-toast -b teal -c green -g top -s warning: you have spent at almost 50% of your daily income so far")
        return print(f"your percentage expenditure is {percent}%\n\n warning: you have spent at almost 50% of your daily income so far")
    elif percent <= 70:
        os.system("termux-toast -b teal -c green -g top -s warning: you have spent at almost 50% of your daily income so far")
        #return print(f"your percentage expenditure is {percent}% oi watch it, you have spent almost 70% of your daily income so far")
    elif percent <= 100: 
        os.system("termux-toast -b teal -c green -g top -s warning: you have spent at almost 50% of your daily income so far")
        #return print(f"your percentage expenditure is {percent}% are you nuts!, you have spent almost all of your daily income so far")
    elif percent >100 :
        excess = percent-100
        notif_message 
        os.system("termux-toast -b teal -c green -g top -s warning: you have spent at almost 50% of your daily income so far")
        
        #return print(
