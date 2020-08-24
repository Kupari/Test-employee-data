from random import randint
    
class SSN_generator(object):

    def __init__(self,gender='random',custom=False):
        '''| gender: default is random, (M)ale or (F)emale | birthdate: ddmmyyyy... |'''

        if gender =='random' and custom==False: self.gender = ['M','F'][randint(0,1)]
        else: self.gender = input('Gender: ').capitalize()
        
        if not custom:
            month = str(randint(1,12)).zfill(2)
            day = str(randint(1,30)).zfill(2)
            year = str(randint(78,99))
        else:
            birthday = input("Birthday (ddmmyyyy): ")
            day = birthday[:2]
            month = birthday[2:4]
            year = birthday[6:8]
            


        characters = '0123456789ABCDEFHJKLMNPRSTUVWXY'
        birthdate = day+month+'19'+year
        datessn = day+month+year
        
        if month == '02' and day>='28': #Special case for february (Leap years not included for simplicity. If used in test data creation, remember to test leap year cases manually!)
            day='28'
        
        if self.gender == 'M':
            sotu = datessn+'9'+str((randint(5,49))*2+1)  #Odd ssn end for males

        if self.gender == 'F':
            sotu = datessn+'9'+str((randint(5,49))*2)    #Even ssn end for females

        if int(birthday[4:8]) > 2000:
            self.ssn = sotu[0:6]+'A'+sotu[6:]+str(characters[int(sotu)%31])
        else:
            self.ssn = sotu[0:6]+'-'+sotu[6:]+str(characters[int(sotu)%31]) #Add the nth character in the list (n = int(SSN) mod 31)
        
        self.birthdate = birthdate

if __name__ == '__main__':
    print(SSN_generator(custom=True).ssn)