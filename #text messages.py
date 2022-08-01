#text messages
import re
cred = []
deb =[]
def check_alerts():
    alerts = [{'threadid': 58, 'type': 'inbox', 'read': True, 'number': 'UNIONBANK', 'received': '2022-07-26 10:09:17', 'body': 'Acct: **3309\nCR: NGN5,000.00\nDesc: OLAKANLA TIMILEYIN PRECIOUSOLAKANLA TIMILEYIN PRECIOUS/via GTWORLD \nDT- 26/JUL/2022 10:08:40\nAvailable Bal: NGN6,030.95CR', '_id': 4527},
{'threadid': 58, 'type': 'inbox', 'read': True, 'number': 'UNIONBANK', 'received': '2022-07-26 18:44:26', 'body': 'Acct: **3309\nDR: NGN1,500.00, COM+VAT:10.75\nDesc: MOBILE/UNION Transfer to LAWAL TAWAKALITU ADEOLA - tf\nDT: 26/JUL/2022 18:41:00\nAvailable Bal: NGN4,520.20CR', '_id': 4536}, 
{'threadid': 5, 'type': 'inbox', 'read': True, 'number': 'UBA', 'received': '2022-07-26 19:00:41', 'body': 'Txn: Credit\nAc:2XX..60X\nAmt:NGN 5,432.00\nDes:TNF-OLAITAN OLABAYO AYOOLA/Transfer from OLAITAN O\nDate:26-Jul-2022 19:00\nBal:NGN 5,609.11\nTransfer with *919#', '_id': 4537},
{'threadid': 5, 'type': 'inbox', 'read': True, 'number': 'UBA', 'received': '2022-07-26 19:04:53', 'body': 'Txn: Debit\nAc:2XX..60X\nAmt:NGN 5,010.75\nDes:MOB/ADEBAYO   FLOUR/UTO/12073821660/Tf\nDate:26-Jul-2022 19:04\nBal:NGN 598.36\nTransfer with *919#', '_id': 4538}, 
{'threadid': 58, 'type': 'inbox', 'read': True, 'number': 'UNIONBANK', 'received': '2022-07-26 19:09:01', 'body': 'Acct: **3309\nDR: NGN500.00, COM+VAT:10.75\nDesc: MOBILE/UNION Transfer to ADEBAYO  FLOURISH - tf\nDT: 26/JUL/2022 19:05:26\nAvailable Bal: NGN4,009.45CR', '_id': 4539}, 
{'threadid': 5, 'type': 'inbox', 'read': True, 'number': 'UBA', 'received': '2022-07-26 19:26:55', 'body': 'Txn: Debit\nAc:2XX..60X\nAmt:NGN 460.75\nDes:MOB/EZEKIEL OLUMIDE/UTO/12074024813/Tf\nDate:26-Jul-2022 19:26\nBal:NGN 137.61\nTransfer with *919#', '_id': 4545},
 {'threadid': 58, 'type': 'inbox', 'read': True, 'number': 'UNIONBANK', 'received': '2022-07-26 19:27:11', 'body': 'Acct: **3309\nCR: NGN400.00\nDesc: OLUMIDE   EZEKIEL/Tf\nDT- 26/JUL/2022 19:26:42\nAvailable Bal: NGN4,409.45CR', '_id': 4546},
  {'threadid': 58, 'type': 'inbox', 'read': True, 'number': 'UNIONBANK', 'received': '2022-07-26 19:28:07', 'body': 'Acct: **3309\nCR: NGN450.00\nDesc: OLUMIDE S EZEKIEL/MOB/EZEKIEL OLUMIDE/UTO/12074024813/Tf\nDT- 26/JUL/2022 19:27:18\nAvailable Bal: NGN4,859.45CR', '_id': 4547}, 
  {'threadid': 127, 'type': 'inbox', 'read': True, 'number': 'ZENITHBANK', 'received': '2022-07-26 22:09:36', 'body': 'Acct:246**041\nDT:26/07/2022:5:47:35PM\nAirtime//07043347784//MTN\nDR Amt:500.00\nBal:450.04\nREF:122915646\nChat with ZiVA on WhatsApp bit.ly/chatziva', '_id': 4550}]
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




def perc():
    ea = check_alerts()
    credit = ea[0]
    debit = ea[1]
    percent = debit/credit * 100
    if percent > 20:
        return print(f"your percentage expenditure is {percent}%")
    
perc()



t = [{'threadid': 58, 'type': 'inbox', 'read': True, 'number': 'UNIONBANK', 'received': '2022-07-26 10:09:17', 'body': 'Acct: **3309\nCR: NGN5,000.00\nDesc: OLAKANLA TIMILEYIN PRECIOUSOLAKANLA TIMILEYIN PRECIOUS/via GTWORLD \nDT- 26/JUL/2022 10:08:40\nAvailable Bal: NGN6,030.95CR', '_id': 4527},
{'threadid': 58, 'type': 'inbox', 'read': True, 'number': 'UNIONBANK', 'received': '2022-07-26 18:44:26', 'body': 'Acct: **3309\nDR: NGN1,500.00, COM+VAT:10.75\nDesc: MOBILE/UNION Transfer to LAWAL TAWAKALITU ADEOLA - tf\nDT: 26/JUL/2022 18:41:00\nAvailable Bal: NGN4,520.20CR', '_id': 4536}, 
{'threadid': 5, 'type': 'inbox', 'read': True, 'number': 'UBA', 'received': '2022-07-26 19:00:41', 'body': 'Txn: Credit\nAc:2XX..60X\nAmt:NGN 5,432.00\nDes:TNF-OLAITAN OLABAYO AYOOLA/Transfer from OLAITAN O\nDate:26-Jul-2022 19:00\nBal:NGN 5,609.11\nTransfer with *919#', '_id': 4537},
{'threadid': 5, 'type': 'inbox', 'read': True, 'number': 'UBA', 'received': '2022-07-26 19:04:53', 'body': 'Txn: Debit\nAc:2XX..60X\nAmt:NGN 5,010.75\nDes:MOB/ADEBAYO   FLOUR/UTO/12073821660/Tf\nDate:26-Jul-2022 19:04\nBal:NGN 598.36\nTransfer with *919#', '_id': 4538}, 
{'threadid': 58, 'type': 'inbox', 'read': True, 'number': 'UNIONBANK', 'received': '2022-07-26 19:09:01', 'body': 'Acct: **3309\nDR: NGN500.00, COM+VAT:10.75\nDesc: MOBILE/UNION Transfer to ADEBAYO  FLOURISH - tf\nDT: 26/JUL/2022 19:05:26\nAvailable Bal: NGN4,009.45CR', '_id': 4539}, 
{'threadid': 5, 'type': 'inbox', 'read': True, 'number': 'UBA', 'received': '2022-07-26 19:26:55', 'body': 'Txn: Debit\nAc:2XX..60X\nAmt:NGN 460.75\nDes:MOB/EZEKIEL OLUMIDE/UTO/12074024813/Tf\nDate:26-Jul-2022 19:26\nBal:NGN 137.61\nTransfer with *919#', '_id': 4545},
 {'threadid': 58, 'type': 'inbox', 'read': True, 'number': 'UNIONBANK', 'received': '2022-07-26 19:27:11', 'body': 'Acct: **3309\nCR: NGN400.00\nDesc: OLUMIDE   EZEKIEL/Tf\nDT- 26/JUL/2022 19:26:42\nAvailable Bal: NGN4,409.45CR', '_id': 4546},
  {'threadid': 58, 'type': 'inbox', 'read': True, 'number': 'UNIONBANK', 'received': '2022-07-26 19:28:07', 'body': 'Acct: **3309\nCR: NGN450.00\nDesc: OLUMIDE S EZEKIEL/MOB/EZEKIEL OLUMIDE/UTO/12074024813/Tf\nDT- 26/JUL/2022 19:27:18\nAvailable Bal: NGN4,859.45CR', '_id': 4547}, 
  {'threadid': 127, 'type': 'inbox', 'read': True, 'number': 'ZENITHBANK', 'received': '2022-07-26 22:09:36', 'body': 'Acct:246**041\nDT:26/07/2022:5:47:35PM\nAirtime//07043347784//MTN\nDR Amt:500.00\nBal:450.04\nREF:122915646\nChat with ZiVA on WhatsApp bit.ly/chatziva', '_id': 4550}]