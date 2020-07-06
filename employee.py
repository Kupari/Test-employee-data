import numpy as np
import pandas as pd
import random
from bs4 import BeautifulSoup as BS
from datetime import datetime
import os
from iban import IBAN #Imports the class IBAN from the iban.py file

#Note to reader/implementer: This is a tool for creating test data for Posti Oy, and as such parts of the script have been redacted and modified limiting its usability.
#
#Summary: This script is designed to create "people" with random names, addresses, social security numbers, bank account numbers and so on. Main usage was in HRM platform integration testing.
#If you want to use this tool from the terminal a good option is to run it in interactive mode using "python -i (path/to/this/file)" 

directory_path = os.path.dirname(os.path.abspath(__file__))


def read_namefiles(dir_path=directory_path): #Move readfiles(folder) to same directory
    """fetches the name files(*.json) from a subfolder in the working directory named readfiles. Path to parent directory required as dir_path='your working directory'. """
    return pd.read_json(str(dir_path)+r"\readfiles\FemaleNames.json"), pd.read_json(str(dir_path)+r"\readfiles\MaleNames.json"), pd.read_json(str(dir_path)+r"\readfiles\surname.json")

def street_names(dir_path=directory_path):
    """Generate a list of streets from a hmtl file of Helsinki street names. This page is no longer available, but you can visit: http://www.puhdistussuunnitelmat.fi/helsinki/kehitt%C3%A4jille to get up-to-date data"""
    with open(str(dir_path)+r"\readfiles\PuhdistussuunnitelmatHelsinki.html") as fp:
        soup = BS(fp,'html.parser')
    #soup.findAll to find every street name tagged as a list object (<li>...</li>) in the html file and create a python friendly array/list. (Street names containing nordic letters excluded to avoid encoding issues.)    
    return [x.text for x in soup.findAll('li') if str(x.text).isalpha()]


#Assign variables to use in "Employee" object. Note: These variables need to be assigned here, since there is no subclass structure to handle this more sophisticatedly inside the object(s).

f,m,s = read_namefiles()
kadut = street_names()
genders = {0:'Male',1:'Female'}


class Employee:

    

    def __init__(self):
        r = random.randint(0,1)             #Assign a Key:Value pairing for the gender
        self.gender = genders[r]

        if self.gender == 'Male':
            self.first_name  = m['name'][random.randint(0,len(m))].lower().capitalize()
        elif self.gender == 'Female':
            self.first_name = f['name'][random.randint(0,len(f))].lower().capitalize()
        self.lastname = s[0][random.randint(0,len(s))]

        self.full_name = self.first_name +' '+ self.lastname
        self.email = self.first_name.lower()+'.'+self.lastname.lower()+'@testemail.com'

        def hetu(self,choice=1):
            '''returns a list object of format: [birthday(with end part of ssn),birthday(without end part of ssn),birthday (DDMMYYYY),SSN]'''
        
            month = str(random.randint(1,12))
            day = str(random.randint(1,30))
            if len(day) == 1:  #Add a leading zero in case rndm number is in range 1-9
                day='0'+day
            if len(month) == 1: #See above but apply for months.
                month='0'+month
            
            if month == '02' and day>='28': #Special case for february (Leap years not included for simplicity. If used in test data creation, remember to test leap year cases manually!)
                day='28'
            
            if self.gender == 'Male':
                birthday_w_end = day+month+str(random.randint(78,99))+'9'+str((random.randint(5,49))*2+1)  #Odd ssn end for males
                birthday_wo_end = birthday_w_end[0:-3]
            if self.gender == 'Female':
                birthday_w_end = day+month+str(random.randint(78,99))+'9'+str((random.randint(5,49))*2)    #Even ssn end for females
                birthday_wo_end = birthday_w_end[0:-3]

            birthday = [birthday_w_end,birthday_wo_end]
            birthday.append(birthday[1][0:4]+'19'+birthday[1][4:])

            characters = '0123456789ABCDEFHJKLMNPRSTUVWXY' #This is how SSN are generated in finland
            n = int(birthday_w_end)%31   #Concatenate the digits in birthday+arbitrary SSN end
            birthday.append(birthday[0][0:6]+'-'+birthday[0][6:]+str(characters[n])) #Add the int(SSN) mod 31 = n (nth character in the list) to make HeTu
            

            if choice == 1:                     #This part serves as reminder in case additional functionality needs to be added
                return birthday
        
        birthdayList = hetu(self)
        
        self.henktun = birthdayList[3]  #hetu() returns a list object of format: [birthday(with end part of ssn),birthday(without end part of ssn),birthday (DDMMYYYY),SSN] so we fetch the 4th/last value which is SSN.
        self.home_street = kadut[random.randint(1,len(kadut))]  #Select a random street in Helsinki 
        self.h_address_num = str(random.randint(1,70))          #Random Street number
        self.birthday = birthdayList[2]                         #Birthday
        self.address = self.home_street+' '+self.h_address_num
        self.iban = IBAN().calculate_random_iban()

        def phone_number_gen():                                 #Generate a randomized phonenumber
            fdigit = random.randint(4,5)
            last7digits = random.randint(1000000,9999999)
            return '0'+str(fdigit)+'0'+str(last7digits)

        self.phonenumber = phone_number_gen()
        self.postalcode ='00'+str(random.randint(10,99))+'0'    #Random postal code, figuring out the real postal code would be to arduous