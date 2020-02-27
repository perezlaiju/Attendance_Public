import requests
from bs4 import BeautifulSoup
from termcolor import colored

URL = "https://sahrdaya.linways.com/"
r = requests.get(url = URL + "student/parent.php")
__cfduid = r.headers['Set-Cookie'].split(";")[0]
phpsessid = r.headers['Set-Cookie'].split("PHPSESSID=")[1].split(";")[0]
cookies = { "__cfduid" : __cfduid,"PHPSESSID" : phpsessid,"tabstat" : ""}

def make75(attended,total):
        temp=attended
        while(attended/total<0.75):
                attended=attended+1
                total=total+1
        #print('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')
        print("\tHours to suffer:",attended-temp,"\n\tPersent after sufferage:",attended/total)

                
def bunkable_hours(attended,total):
        temp=total
        while(attended/total>0.75):
                total=total+1
        if(total-temp>1):
                print("\tBunkable Hours:",total-temp-1)
        else:
                print("\t :(")
        
def bunk(x,y):
        attended=float(x)
        total=float(y)
        print("\tPercentage:",attended/total)
        if(attended/total>0.75):
                bunkable_hours(attended,total)
        elif(attended/total==0.75):
                print("\t :(")
        else:
                make75(attended,total)
        
        
def login(username,password):
        credentials = { "studentAccount":username,"parentPassword":password }
        r = requests.post(url = URL + "student/parent.php", data = credentials, cookies = cookies)
        #r = requests.get(url = URL + "/student/student.php?menu=attendance&action=subjectwise", cookies = cookies)

def attendance():
        r = requests.get(url = URL + "student/attendance/ajax/ajax_subjectwise_attendance.php?action=GET_REPORT", cookies = cookies)
        soup = BeautifulSoup(r.text,"lxml")
        table = soup.find("table")
        output_rows = []
        for table_row in table.findAll('tr'):
                columns = table_row.findAll('td')
                output_row = []
                for column in columns:
                        output_row.append(column.text)
                output_rows.append(output_row)
        for i in range(1,13):
                print("\n\n")
                for j in range(1,4):
                        if(j==1):
                                print(output_rows[i][j])
                        else:
                                print("\t",output_rows[i][j])
                        if(j==3):
                                bunk(output_rows[i][2],output_rows[i][3])
        global data
        data=output_rows



username=input("Username:")
password=input("Password:")
login(username,password)
attendance()
i=input("Exit.")
