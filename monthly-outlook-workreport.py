import win32com.client
import win32com
from pywintypes import com_error
import os
import sys
import datetime
import calendar

# Pre-requisite: install pywin32 using 'pip install pywin32'
# Resources:
# https://docs.microsoft.com/en-us/office/vba/api/Outlook.NameSpace
# https://stackoverflow.com/questions/22813814/clearly-documented-reading-of-emails-functionality-with-python-win32com-outlook
# https://docs.microsoft.com/en-us/office/vba/api/outlook.recipient


today = datetime.date.today()

f = open("emailsummary-{}.csv".format(today.strftime("%b").upper()),"w")

outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
sentmailbox=outlook.GetDefaultFolder(5)


firstdayofthismonth=today.replace(day=1).strftime("%d-%m-%y")
firstdayofnextmonth=(today.replace(day=1) + datetime.timedelta(days=calendar.monthrange(today.year,today.month)[1])).strftime("%d-%m-%y")

messages=sentmailbox.Items.restrict("[SentOn] > '{} 12:00 AM' And [SentOn]  < '{} 12:00 AM'".format(firstdayofthismonth, firstdayofnextmonth))

for message in messages:
    subject = message.Subject;

    if (not subject.startswith("Canceled:") and not subject.startswith("Accepted:") and not subject.startswith("Declined:")):
        try:
            recipients = str(message.To).strip();
            sender = str(message.Sender).strip();
            senttime = message.SentOn;

            if (sender != recipients and not "@gmail.com" in recipients): 
                toprint = "{},'{}',{}".format(senttime, subject, recipients);
                print(toprint,file=f)
                print(toprint)
                
        except com_error as e:
            toprint = "{},'{}',{}".format("<encrypted email>", subject, "<encrypted email>");            
            print(toprint,file=f);
            print(toprint);
        except:            
            pass;
        

# TODO: retrieve outlook meetings for this month.

f.close()
