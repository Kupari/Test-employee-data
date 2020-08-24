import numpy as np
import pandas as pd
from random import randint
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
        r = randint(0,1)             #Assign a Key:Value pairing for the gender
        self.gender = genders[r]

        if self.gender == 'Male':
            self.first_name  = m['name'][randint(0,len(m))].lower().capitalize()
        elif self.gender == 'Female':
            self.first_name = f['name'][randint(0,len(f))].lower().capitalize()
        self.lastname = s[0][randint(0,len(s))]
        self.full_name = self.first_name +' '+ self.lastname
        self.email = self.first_name.lower()+'.'+self.lastname.lower()+'@testemail.com'

        month = str(randint(1,12)).zfill(2)
        day = str(randint(1,30)).zfill(2)
        year = str(randint(78,99))
        characters = '0123456789ABCDEFHJKLMNPRSTUVWXY'

        if month == '02' and day>='28': #Special case for february (Leap years not included for simplicity. If used in test data creation, remember to test leap year cases manually!)
            day='28'
        
        birthdate = day+month+'19'+year
        datessn = day+month+year

        if self.gender == 'Male':
            sotu = datessn+'9'+str((randint(5,49))*2+1)  #Odd ssn end for males

        if self.gender == 'Female':
            sotu = datessn+'9'+str((randint(5,49))*2)    #Even ssn end for females

        self.henktun = sotu[0:6]+'-'+sotu[6:]+str(characters[int(sotu)%31]) #Add the nth character in the list (n = int(SSN) mod 31)
        self.birthdate = birthdate
        self.home_street = kadut[randint(1,len(kadut))]  #Select a random street in Helsinki 
        self.h_address_num = str(randint(1,70))          #Random Street number
        self.birthday = datessn[:2]+'/'+datessn[2:4]+'/19'+datessn[4:]  #Birthday
        self.address = self.home_street+' '+self.h_address_num
        geniban = IBAN()
        self.iban = geniban.calculate_random_iban()
        self.iban_details = geniban.details()
        self.phonenumber = '0'+str(randint(4,5))+'0'+str(randint(1000000,9999999)) #Random finnish phonenumber  
        self.postalcode ='00'+str(randint(10,99))+'0'    #Random postal code, figuring out the real postal code would be to arduous



a = [Employee() for x in range(2)]


methods = ['full_name', 'email', 'gender', 'henktun', 'birthday', 'iban_details', 'phonenumber','address','postalcode']
for x in a:
    print("\n")
    for i in range(len(methods)):
        print(getattr(x,methods[i]))