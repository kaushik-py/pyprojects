import mysql.connector as sql
from datetime import datetime
import csv
'''This project is created by Kaushik Joshi and in this project i have used sql connector for 
making bank management system to store the database of bank users and for related work'''

facilities ='We are giving the following facilities -:\n\
Press 1 to open your account\n\
Press 2 to add  money to your account\n\
Press 3 to check your money\n\
Press 4 to transfer money to other account\n\
Press 5 to Withdraw your money from your account .\n\
Press 6 to convert your account details into a excel file.\n\
Press 7 to close your bank account.\n\
Press 8 to exit.\n\
'
def database_handler(psw): # This function will check in sql that database named "bank" is there or not, if not so it will create automatically.
    var = False
    try :
        var = True
        mydb = sql.connect(user = "root" , host = "localhost" , password = psw)
        mycursor  = mydb.cursor()
        mycursor.execute('show databases')
        result = mycursor.fetchall()
        flag = False
        for i in result :
            if i[0] == "bank" :
                flag = True
            else :
                pass
        if flag :
            pass
        else :
            query = "create database bank"
            mycursor.execute(query)

    except :
        var = False
        print("You have entered wrong password!!!!!!!")
    return var
        



def current_date(): # This function will give us date in the format 'Date Month_name Year'
    day = datetime.now().day
    month = datetime.now().month
    year = datetime.now().year
    month_name = ['January','February','March','April','May','June','July','August','September','October','November','December']
    month_number = [1,2,3,4,5,6,7,8,9,10,11,12]
    month_number = month_name
    temp = month - 1
    month = month_number[temp]
    formatted_date = f'"{day} {month} {year}"'
    return formatted_date

def current_time(): 
    hour = datetime.now().hour
    minute = datetime.now().minute
    second = datetime.now().second
    formatted_time = f'"{hour}:{minute}:{second}"'
    return formatted_time

def connect(psw): # This function will connect our program with sql database named "bank"
    global mydb, mycursor
    mydb = sql.connect(user = "root" , host = "localhost" , password = psw , database = "bank" )
    mycursor = mydb.cursor()

def check_user(user_name,psw):
    connect(psw)
    user_query = "show tables"
    mycursor.execute(user_query)
    result = mycursor.fetchall()
    flag = False
    for x in result :
        value = x[0]
        if value == user_name:
            flag = True
            break
        else:
            flag = False
    return flag


def open_account(user_name,psw):  # This funtion will create a table for each unique user in bank database in sql
    connect(psw)
    is_user = check_user(user_name,psw)
    if is_user:
        print("This username is already registered in our bank. Please try another name.....")
        return False
    else:
        query = f'create table {user_name} (Id int(11) primary key ,Current_balance int(25) , Date varchar(30) , Time varchar(20))'
        mycursor.execute(query)
        mydb.commit()
        return True

def add_money(user_name,money,flag,psw): # This funtion will add entry in Current_balance column in given username table
    connect(psw)
    query = f'select count(Id) from {user_name} '
    mycursor.execute(query)
    result = mycursor.fetchall()
    user_id = result[0][0] + 1
    val = user_id - 1
    sql_query = f'select Current_balance from {user_name} where Id = {val}'
    mycursor.execute(sql_query)
    result = mycursor.fetchall()
    if result == []:
        value = 0 + money
    else:
        value = result[0][0]
        value = value + money
    user_date = current_date()
    time = current_time()
    query = f'insert into {user_name}(Id,Current_balance,Date,Time) values({user_id},{value},{user_date},{time}) '
    mycursor.execute(query)
    mydb.commit()
    if flag:
        print("Congratulations!! Your money is added to your account.")
    else:
        pass

    

def minus_money(user_name,money,psw):  # This funtion will fetch current banlance from username table and deduct given value from it
    connect(psw)
    query = f'select count(Id) from {user_name} '
    mycursor.execute(query)
    result = mycursor.fetchall()
    user_id = result[0][0]
    query = f'select Current_balance from {user_name} where Id = {user_id}'
    mycursor.execute(query)
    result = mycursor.fetchall()
    paisa = result[0][0]
    paisa = paisa - money
    user_id = user_id + 1  
    user_date = current_date()
    time = current_time()
    query = f'insert into {user_name} (Id,Current_balance,Date,Time) values({user_id},{paisa},{user_date},{time}) '
    mycursor.execute(query)
    mydb.commit()




def show_details(user_name,psw): # This funtion will show us all the details of given username table
    connect(psw)
    user = check_user(user_name,psw)
    if user :
        query = f'select * from {user_name}'
        mycursor.execute(query)
        content = mycursor.fetchall()
        if (len(content) == 0):
            print("Your account balance is 0 . Please add some money into your account.....")
        else:
            print('Id','  Current_balance', '         Date','           Time')
            for x in content :
                print(x[0],'     ',x[1],'          ',x[2],'   ',x[3])
    else :
        print(user_name,"does not have account in our bank.............")

def transfer_money(psw): # This function will deduct given value from given username table and will add to another given username table
    connect(psw)
    sender = input("Enter your name-- ")
    sender_check = check_user(sender,psw)
    if sender_check :
        reciever = input("Enter user name in which you want to send the money to its account-- ")
        reciever_check = check_user(reciever,psw)
        query = f'select count(Id) from {sender} '
        mycursor.execute(query)
        result = mycursor.fetchall()
        value = result[0][0]
        query = f'select Current_balance from {sender} where Id = {value}'
        mycursor.execute(query)
        result = mycursor.fetchall()
        paisa = result[0][0]
        if reciever_check:
            money = int(input("Enter the amount you want to tansfer to its account- "))
            if (money < paisa) :
                add_money(reciever,money,False,psw)
                minus_money(sender,money,psw)
                print(f'Congratulations!! Money is successfully transfered from {sender} account to {reciever} account.......')
            elif (money == paisa):
                print("We cannot transfer all money to other account . Your account should have atleast  1 rupees....")
            else:
                print(money,"rupees is not in your account!!!!")
        else :
            print(reciever,"does not have account in our bank...")
    else:
        print(sender,"does not have account in our bank.......")

def convert_ac_into_excel(psw,user_name): # This funtion will fetch all the details of the given username table and will add this details to the csv file
    connect(psw)
    query = f'select * from {user_name} '
    mycursor.execute(query)
    result = mycursor.fetchall()
    fh = open(f'{user_name}.csv','w',newline="")
    empwriter = csv.writer(fh)
    empdata = [
        ['      ','      ','Samadhan Bank','      ','      '],
        ["                Id","             Current_balance","                  Date","                         Time"]
    ]
    for i in range(0,len(result)):
        data = list(result[i])
        empdata.append(data)
    empwriter.writerows(empdata)
    fh.close() 
       
def close_account(psw , user_name) : # This funtion will delete the given table from the 'bank' database
    connect(psw)
    query = f'drop table {user_name}'
    mycursor.execute(query)
    mydb.commit()
    print("Dear user Thanks for using Samadhan bank***********")
    print("Please rate us!!!!")

print("****Welcome Dear user to Samadhan Bank ****")
date = current_date()
print("Todays date is ", date)
print(facilities)
psw = input("Enter the password of your sql: ")
chk_database = database_handler(psw)
exit_user = False
try:
    while (not exit_user) and chk_database :
        try:
            choice = int(input("Please enter your choice number---- "))
        except :
            print("You have entered a wrong input .You have to enter only choice number like 1,2,3,4,etc...........")
            break
        if choice == 1:
            print("Ok!! So you want to create your account .")
            user_name = input("Please enter your name to create your account-- ")
            connect(psw)
            success = open_account(user_name,psw)
            if success:
                print("Congratulations!! Your accont has been successfully created..")
            else:
                pass

        elif choice == 2 :
            name = input("Please enter your name.- ")
            flag = check_user(name,psw)
            if flag:
                money = int(input("Enter how much money you want to add-- "))
                add_money(name,money,True,psw)
            else:
                print("This user dont have account in our bank..")
                print("Seems like you don't have account in our bank . Please open your account by writing choice number as 1....")

        elif choice == 3 :
            user = input("Please enter your name to see your details-- ")
            show_details(user,psw)

        elif choice == 4 :
            transfer_money(psw)

        elif choice == 5 :
            user_name = input("Please enter your name... ")
            money = int(input("Please enter how much money you want to withdraw from your account... "))
            minus_money(user_name,money,psw)
            print("Congrats!! Your money is successfully withdrawn from your account......")

        elif choice == 6 :
            usr_name = input("Enter your account name: ")
            convert_ac_into_excel(psw,usr_name)
            print("Your account details is successfully converted into excel file*********")

        elif choice == 7 :
            user_name = input("Please enter account name which you want to close-- ")
            close_account(psw,user_name)


        elif choice == 8 :
            print("********Thank You for using facilities given by Samadhan bank********")
            exit_user = True
        
except:
    print("There is some error!!!! . Please try again later, we will fix it soon.........")
    
# Thanks by - Kaushik Joshi
