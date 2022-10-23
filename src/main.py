from time import sleep
import pyfiglet
import shortuuid
import sqlite3

#############
print("\033c")
result = pyfiglet.figlet_format("MFZ Bank",font='banner3-D')
print(result)
#############

################ SQLite3

conn=sqlite3.connect('bankAccount.db')
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS accounts(suuid TEXT ,name TEXT, dob TEXT, adrs TEXT, mob TEXT, gender TEXT, strt_amt REAL )")

conn.commit()



######## Variables
accId,name,dob,address,mob_num,gender,atm_job,starting_amt ="null","null","null","null","null","null","null",0


def welcmScreen():
    print("WELCOME TO THE BANK OF MFZ\n\n")

    print("Please Enter Your Account Id: ")
    print("(type 'mkacc' for creating a new account)")
    global accId,name,dob,address,mob_num,gender,starting_amt
    accId = input();

    if accId == "mkacc":
        print("\033c")
        print(result+"\n")
        print("ENTER THE FOLLOWING DETAILS:\n")
        uuid = shortuuid.ShortUUID().random(length=6)
        name=input("Name:")
        address=input("Address:")
        dob=input("Date of Birth:")
        gender=input("Gender:")
        mob_num=input("Contact Number:")
        starting_amt = int(input("Enter The Starting Amount: "))

        if starting_amt > 450 :
            ## Bank Money
            starting_amt -= 50
            ## Bank Money
            c.execute(f"INSERT INTO accounts (suuid,name,dob,adrs,mob,gender,strt_amt) VALUES (?,?,?,?,?,?,?)",
            (uuid,name,dob,address,mob_num,gender,starting_amt))
            conn.commit()

            print("\033c")
            print(result+"\n\n")
            c.execute(f"SELECT suuid FROM accounts WHERE mob='{mob_num}'")
            for row in c.fetchone():
                print("Your Account ID Is: ")
                print(row)
                print("\n\n (Do not forget this. You cannot recover your account)")

        else:
            print("Account cannot be opened with Rs."+str(starting_amt)+" (Should be more than or equal to 450)")
        
    
    if accId != "mkacc":    
        #
        c.execute(f"SELECT EXISTS(SELECT 1 FROM accounts WHERE suuid='{accId}' LIMIT 1)")
        for row in c.fetchone():
            if row == 1:
                job1()
            else:
                print("\033c")
                print(result+"\n")
                print("No Account Found !")
    if accId == "exit":
        print("\033c")

def widthdraw():
    print("\033c")
    print(result+"\n")
    wdrw_amt = int(input("Enter The Amount To Be WithDrawen: "))
    c.execute(f"SELECT strt_amt FROM accounts WHERE suuid='{accId}'")
    for frow in c.fetchone():
        amt = frow
        if wdrw_amt > amt :
            print('Amount Withdrawn is more than Account Balance')
            print('Process Failed !')
        else:
            deducted_amt = amt - wdrw_amt
            ### Bank Money
            deducted_amt -= (0.2*deducted_amt)/100
            ####
            c.execute(f"UPDATE accounts SET strt_amt=(?) WHERE strt_amt=(?) ",
            (deducted_amt,amt))
        
            print("Processing...")
            sleep(3)
            conn.commit()
            print('Withdrawl Successful !')

def deposit():

    print("\033c")
    print(result+"\n")

    deposit_amt = int(input('Enter the Amount you want to deposit :'))



    if deposit_amt >= 25000:
        print("Depositing Amount should be less than 25000")
        print('Process Failed !')

    else:
        c.execute(f"SELECT strt_amt FROM accounts WHERE suuid='{accId}'")
        for frow in c.fetchone():
            amt = frow
            added_amt = amt + deposit_amt
            c.execute(f"UPDATE accounts SET strt_amt=(?) WHERE strt_amt=(?) ",
                (added_amt,amt))

            print("Processing...")
            sleep(3)
            conn.commit()
            print('Amount Deposited !')

def transfer():
    print("\033c")
    print(result+"\n")

    transfer_amt = int(input("Enter the amount to be transfered: "))
    transfer_from = input("Enter the Account ID from : ")
    
    c.execute(f"SELECT strt_amt FROM accounts WHERE suuid='{accId}'")
    for row in c.fetchone():
        transerer_amt = row
        transerer_amt -=transfer_amt
        c.execute(f"UPDATE accounts SET strt_amt=(?) WHERE suuid=(?) ",
                (transerer_amt,accId))
        conn.commit()

    c.execute(f"SELECT strt_amt FROM accounts WHERE suuid='{transfer_from}'")
    for row in c.fetchone():
        self_amt = row
        transered_amt = transfer_amt + self_amt
        c.execute(f"UPDATE accounts SET strt_amt=(?) WHERE suuid=(?) ",
                (transered_amt,transfer_from))
        conn.commit()
        print("\033c")
        print(result+"\n")
        print("Processing...")
        sleep(3)
        print('Amount Transfered !')   

    

def balance():

    c.execute(f"SELECT strt_amt FROM accounts WHERE suuid='{accId}'")
    for row in c.fetchone():
        print("\033c")
        print(result+"\n")
        print("Processing...")
        sleep(3)
        print("\033c")
        print(result+"\n")
        print("Your Account balance is Rs."+str(row))




def job1():
    global atm_job
    print("\033c")
    print(result+"\n")
    print("[1] Withdrawal")
    print("[2] Deposit")
    print("[3] Transfer")
    print("[4] Balance Enquiry \n")

    atm_job = input(" : ")

    if atm_job =="1":
        widthdraw()
    elif atm_job =="2":
        deposit()
    elif atm_job =="3":
        transfer()
    elif atm_job =="4":
        balance()
    else:
        print("Process Failed !")


    
welcmScreen()
print("\n\n")
c.close()
conn.close()

# c.execute(f"SELECT * FROM accounts WHERE suuid='{accId}'")
                # for frow in c.fetchall():
                #     print(frow)



