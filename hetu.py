from random import randint
from datetime import datetime
    
class SSN_generator(object):

    def __init__(self,custom=False):
        '''| gender: default is random, (M)ale or (F)emale | birthday: ddmmyyyy... |'''

        if custom==False: self.gender = ['M','F'][randint(0,1)]
        else: self.gender = input('Gender: ').capitalize()
        
        if not custom:
            month = str(randint(1,12)).zfill(2)
            day = str(randint(1,30)).zfill(2)
            year = str(randint(78,99))
            birthday = day+month+'19'+year
        else:
            birthday = input("Birthday (ddmmyyyy): ")
            day = birthday[:2]
            month = birthday[2:4]
            year = birthday[6:8]
        
        characters = '0123456789ABCDEFHJKLMNPRSTUVWXY'
        datessn = day+month+year
        
        if month == '02' and day>='28': #Special case for february (Leap years not included for simplicity. If used in test data creation, remember to test leap year cases manually!)
            day='28'
        
        if self.gender == 'M':
            sotu = datessn+'9'+str((randint(5,49))*2+1)  #Odd ssn end for males

        if self.gender == 'F':
            sotu = datessn+'9'+str((randint(5,49))*2)    #Even ssn end for females

        if int(birthday[4:8]) >= 2000:
            self.ssn = sotu[0:6]+'A'+sotu[6:]+str(characters[int(sotu)%31])
        else:
            self.ssn = sotu[0:6]+'-'+sotu[6:]+str(characters[int(sotu)%31]) #Add the nth character in the list (n = int(SSN) mod 31)
        
        self.birthdate = datetime.strptime(birthday,'%d%m%Y').strftime('%d-%m-%Y')

if __name__ == '__main__':
    RorC = input('Generate (r)andom or (c)ustom SSN: ').capitalize()
    
    if RorC == 'C':
        a = SSN_generator(custom=True)
        print(a.ssn)
        print(a.birthdate)
    if RorC == 'R':
        a = SSN_generator(custom=False)
        print(a.ssn, 'Male' if a.gender == 'M' else 'Female')
        print(a.birthdate)