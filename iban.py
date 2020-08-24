from random import randint
import json
import os

file_path = os.path.dirname(os.path.abspath(__file__))

class IBAN:
    


    def __init__(self):
        with open(file_path+'\BIC.txt','r') as biclist:
            biclist = json.load(biclist)
            randombic = biclist[randint(1,665)]
            self.code = randombic['Code']
            self.bic = randombic['BIC']
            self.bank = randombic['BANK']
        self.branch_code = self.code + str(randint(100,999))
        self.rand_acc = str(randint(1000000,9999999))
        self.country_code = "1518" #F=15, I=18
        self.account_check =''


    def bban(self):
        
        self.account_code = self.branch_code + self.rand_acc
        account_check=''
        
        step=-1
        for x in range(13): #Length of banknumber to be validated
            
            if x != 0:
                step+=1
            
            if int(self.account_code[x]) * 2 > 9 and step%2 != 0:
                account_check += str(int(str(int(self.account_code[x])*2)[0])+int(str(int(self.account_code[x])*2)[1]))
            
            elif int(self.account_code[x]) * 2 < 9 and step%2 != 0:
                account_check += str(int(self.account_code[x])*2)
            
            else:
                account_check += (self.account_code[x])
        
        sumofdigits = 0
        for i in range(len(account_check)):
            sumofdigits += int(account_check[i])
        bban_check_digit = (sumofdigits*9)%10

        self.acc = self.account_code + str(bban_check_digit)
        
        self.complete_form =self.acc + self.country_code+'00'
        return self.complete_form
    
    def generate_iban(self):
        check_digit = 98-int(self.bban())%97
        if check_digit < 10:
            check_digit = '0'+str(check_digit)
        return check_digit


    def calculate_random_iban(self):
        self.iban = 'FI'+str(self.generate_iban())+str(self.acc)
        return self.iban

    def details(self):
        return self.calculate_random_iban() +' : '+ self.bic +' : '+ self.bank



if __name__ == "__main__":
    account = IBAN()
    print(account.calculate_random_iban())
    print(account.details())
    
    pass




