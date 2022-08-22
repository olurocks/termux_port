from datetime import datetime
import os
import subprocess
import json
import re
from types import NoneType
from apscheduler.schedulers.blocking import BlockingScheduler

os.system("")
os.system("termux-wake-lock")

daily_limit = int(input("enter Your estimate daily limit : "))
time_interval = int(input("\nhow often do you want to receive allerts?" +str("\n\nenter specific time in minutes: ") ))

while datetime.today().date():
    time = time_interval
    break

def check_time(init_time):
    time_t = datetime.strptime(init_time, '%Y-%m-%d %H:%M:%S')
    if time_t.date() < datetime.today().date():
        return True
    return False


#get bulk text_messages from Your phone
def get_msg(record):
    raw_msg = subprocess.Popen(f"termux-sms-list -l {record}",shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    out , err = raw_msg.communicate()
    messages = json.loads(out.decode('utf-8'))
    return messages

# check if the last 30th message is from yesterday
# if it's not from yesterday, check for the next 15 and stop checking once the last nth message is from yesterday
# this is to help ensure we're getting all messages from 12:00am today,which may or may not include messages from yesterday

def get_required_messages():
    list = 30
    while True:
        msgs = get_msg(list)
        if check_time(msgs[0]["received"]):
            return msgs
        list+=15


# ensure each message from required_messages is from today, if not extract the ones from today
# this is to remove messages from yesterday. For cases that included messages from the previous day
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
    if type(day_messages) == NoneType :
        return "You have no alerts alerts for the day"
    else:
        for i in day_messages:
            if i["number"].lower() in banks:
                alerts.append(i)    
        return alerts   

# check if alert is credit or debit
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
                    b = float(i.group().replace(",",""))
                    deb.append(b)

    total_credit = round(sum(cred),2)
    total_debit = round(sum(deb),2)

    os.system(f"""ls $PREFIX| termux-toast -b green -c blue -g top -s 'Daily Income :
     \#{total_credit}' """)

    os.system(f"""ls $PREFIX| termux-notification -c 'Daily income: #{total_credit}' """)

    os.system(f"""ls $PREFIX| termux-toast -b green -c red -g top -s 'Daily Expenditure :
     \#{total_debit}' """)

    os.system(f"""ls $PREFIX| termux-notification -c 'Daily Expenditure : 
    #{total_debit}' """)

    return total_credit,total_debit


#send notifications

def notif():
    ea = check_alerts()
    credit = ea[0]
    debit = ea[1]
    while datetime.today().date():
        limit = daily_limit
        break

    if debit == 0:
       notification = os.system("""ls $PREFIX| termux-toast -b green -c cyan -g top You have zero expenditures as of today""")

    else:
        dl_percent = debit / limit * 100
        if dl_percent <= 10:
            notification = os.system("""ls $PREFIX| termux-toast -b teal -c green -g top At least 10% of daily limit spent""")
            not2 = os.system(f"""ls $PREFIX| termux-notification -c 'You have spent At least 10% of Your daily expenditure limit'""")

        elif dl_percent <= 20:
            notification = os.system("""ls $PREFIX| termux-toast -b teal -c green -g top  At least 20% of daily limit spent""")
            not2 = os.system(f"""ls $PREFIX| termux-notification -c 'You have spent At least 20% of Your daily expenditure limit'""")

        elif dl_percent <= 30:
            notification = os.system("""ls $PREFIX| termux-toast -b teal -c green -g top -s 'At least 30% of Daily limit spent""")
            not2 = os.system(f"""ls $PREFIX| termux-notification -c 'You have spent At least 30% of Your daily expenditure limit'""")

        elif dl_percent <= 50:
            notification = os.system("""ls $PREFIX| termux-toast -b teal -c green -g top -s 'At least 50% of daily limit spent""")
            not2 = os.system(f"""ls $PREFIX| termux-notification -c 'You have spent At least 50% of Your daily expenditure limit'""")

        elif dl_percent <= 75:
            notification = os.system("""ls $PREFIX| termux-toast -b teal -c green -g top -s 'WARNING:
             At least 75% of daily limit spent""")
            not2 = os.system(f"""ls $PREFIX| termux-notification -c 'WARNING: 
      You have spent At least 75% of Your daily expenditure limit'""")
        elif dl_percent == 100:
            notification = os.system("""""ls $PREFIX| termux-toast -b teal -c green -g top -s 'WARNING: 
            At least 100% of daily expenditure limit spent' """)
            not2 = os.system(f"""ls $PREFIX| termux-notification -c 'You have spent At least 100% of Your daily expenditure limit'""")
        elif dl_percent > 100:
            notification = os.system(f"""ls $PREFIX| termux-toast -b teal -c green -g top -s 'WARNING:
      You have spent {round((dl_percent - 100),2)}% which is \#{debit - limit} more than Your daily limit  """)
        notification = os.system(f"""ls $PREFIX| termux-toast -b teal -c green -g top -s 'WARNING:
      You have spent {round(dl_percent,2)}% of Your daily limit' """)
    
    if debit > credit:

        notification = os.system(f"""ls $PREFIX| termux-toast -b teal -c red -g top -s 'WARNING:
      You have spent \#{debit - credit} more than Your daily income' """)
        not2 = os.system(f"""ls $PREFIX| termux-nptification -c 'WARNING:
      You have spent \#{debit - credit} more than Your daily income' """)


    if debit < limit:
        notification = os.system(f"""ls $PREFIX | termux-toast -b teal -c brown -g top -s 'CAUTION:
      You have \#{limit - debit} left of Your daily expenditure for the day' """)
        not2 = os.system(f"""ls $PREFIX | termux-notification -c 'CAUTION:
      You have \#{limit - debit} left of Your daily expenditure for the day' """)

    return notification, not2

#schedule to run periodically
scheduler = BlockingScheduler()
scheduler.add_job(notif, 'interval', minutes = time)
scheduler.start()
