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
    for i in day_messages:
        if i["number"].lower() in banks:
            alerts.append(i)    
    return alerts   

#'''check if alert is credit or debit
def check_alerts():
    alerts = access_alerts()
    cred = []
    deb =[]
    for al in alerts:
        # if alert is credit,extract credit amount
        if "cr:" in al["body"].lower() or "txn: credit"  in al["body"].lower():
            cr = re.compile(r'(cr|amt)\w*.?.?\w*.?.?ngn.?\d{1,3}.?\d{1,3}.?\d{1,3}.?\d{1,3}.?\d{1,3}')
            extract_figs = re.compile(r'\d{1,3}.?\d{1,3}.?\d{1,3}.?')
            credit = cr.finditer(al['body'].lower())
            for i in credit:
                credit_amount = extract_figs.finditer(i.group())
            for i in credit_amount:
                b = float(i.group().replace(",",""))
                cred.append(b)


        # if alert is debit, extract debit amount
        if "dr:" in al["body"].lower() or "txn: debit" in al['body'].lower() or "dt:"in al['body'].lower():
            de = re.compile(r'(d|amt)\w*.?.?\w*.?.?ngn.?\d{1,3}.?\d{1,3}.?\d{1,3}.?\d{1,3}')
            extract_figs = re.compile(r'\d{1,3}.?\d{1,3}.?\d{1,3}.?')
            debit = de.finditer(al['body'].lower())
            
            for i in debit:
                debit_amount = extract_figs.finditer(i.group())
                for i in debit_amount:
                    # b = float(i.group().replace(",",""))
                    b = float(i.group().replace(",",""))
                    deb.append(b)
    
    # find the sum of total credits against total debits 
    total_credit = sum(cred)
    total_debit = sum(deb)
    return total_credit,total_debit

    print("your total amount received today is :",sum(cred))
    print("your total amount spent so far today is :",sum(deb))




# calculate the percentage of debit against credit
def notif():
    ea = check_alerts()
    credit = ea[0]
    debit = ea[1]
    percent = debit/credit * 100
    print(f"your percentage expenditure is {percent}%" )

    
# if the percentage of debit to credit  >= 20%: send a mild notification
    if percent < 20:
        return print(f"your percentage expenditure is {percent}%")
# if the percentage of debit to credit  >= 50%: send a warning
    elif percent >=50:
        return print(f"your percentage expenditure is {percent}%\n\n warning: you have spent at least 50% of your daily income so far")
# if the percentage of debit to credit  >= 70%: send a wild warning
    elif percent >= 70:
        return print(f"your percentage expenditure is {percent}% oi watch it, you have spent at least 70% of your daily income so far")

# if the percentage of debit to credit  >= 100%: "send spent more than income warning"  '''
    elif percent >= 100: 
        return print(f"your percentage expenditure is {percent}% are you nuts!, you have spent at least all of your daily income so far")
