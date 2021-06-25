#Solve splitting without empty strings

import unidecode
import random
import sys
import unicodedata
import PySimpleGUI as sg
import keyboard
import os
#What is 0PS2o000000R5DJGA0
#WTF is this group? X00e2o0000013J6tAAE
#ProfileID "00e2o0000013J6tAAE"
#CTI_Permission_Group 
#  PermissionSetID:         "0PS2o000000HzULGA0"
#  PermissionsetgroupID:    "0PG2o000000GmhtGAC"
#Performance "0PS2o000000HytTGAS"
#  PermissionSetID:         "0PS2o000000HytTGAS"
#  PermissionsetgroupID:    ""
#PerformanceGroupC "a0e2o0000106E0rAAE"
#Nezrusene_ucty "00G2o000009BH9AEAW"
#Broker "00G2o000009c00qEAA"

vowels = "aeiouy"

consonants = "bcdfghjklmnpqrsvwxz"

csvFolder = "mockupCSVs/"

def generagePassword():
    passwordLength = random.randint(8, 10)
    x = 0

    password = ""

    while x < 3*passwordLength/5:
        if x%2 == 0:
            password += random.choice(consonants)
        else:
            password += random.choice(vowels)
        x += 1

    upperChar = random.randint(0, x-1)
    password = password[:upperChar] + password[upperChar].upper() + password[(upperChar+1):]

    while x < passwordLength:
        password += str(random.randint(0,9))
        x += 1
    return password


class user(object):
    def __init__(self, firstName, middleName, secondName, zeteoID = -1):
        self.firstName = firstName
        self.middleName = middleName
        self.secondName = secondName
        self.email = self.createEmail()
        self.emailPass = generagePassword()
        self.zeteoName = self.createZeteoName()
        self.zeteoPass = generagePassword()
        self.zeteoID = zeteoID
        self.ustrednaName = self.email
        self.ustrednaPass = generagePassword()

    def createEmail(self):
        firstName = unidecode.unidecode(self.firstName).lower()
        secondName = unidecode.unidecode(self.secondName).lower()
        email = firstName+"."+secondName+"@rixo.cz"
        return email

    def createZeteoName(self):
        firstName = unidecode.unidecode(self.firstName).lower()
        secondName = unidecode.unidecode(self.secondName).lower()
        zeteoName = firstName+"."+secondName
        return zeteoName

    def __str__(self):
        return self.firstName + self.middleName + " " + self.secondName + " " + self.email 

class fileCreatorHandler(object):
    def __init__(self, inputFileName, lastZeteoID = -1, firstName_SecondName = True, azureUserAddFileWanded = True, azureGroupAddFileWanded = True, zeteoFileWanded = True, ustrednaFileWanded = True, jaachymFileWanded = True, nSureFileWanted = True, azureCredentialsWanted = True, salesforceCredentialsFileWanted = True, salesforcePerformanceGroupFileWanted = True):
        self.inputFileName = inputFileName
        self.lastZeteoID = lastZeteoID+1
        self.firstName_secondName = firstName_SecondName
        self.newUsers = self.readUsersFromFile()
        self.azureUserAddFileWanded = azureUserAddFileWanded
        self.azureUserAddFileName = csvFolder + "Azure_Bulk_User_Create.csv"
        self.azureGroupAddFileWanded = azureGroupAddFileWanded
        self.azureGroupAddFileName = csvFolder + "Azure_Bulk_Group_Add.csv"
        self.zeteoFileWanded = zeteoFileWanded
        self.zeteoFileName = csvFolder + "Zeteo_User_Credentials.csv"
        self.ustrednaFileWanded = ustrednaFileWanded
        self.ustrednaFileName = csvFolder + "Ustredna_User_Credentials.csv"
        self.jaachymFileWanded = jaachymFileWanded
        self.jaachymFileName = csvFolder + "Zeteo_For_Jaachym.csv"
        self.nSureFileWanted = nSureFileWanted
        self.nSureFileName = csvFolder + "nSure_User_Credentials.csv"
        self.azureCredentialsWanted = azureCredentialsWanted
        self.azureCredentialsFileName = csvFolder + "Azure_User_Credentials.csv"
        self.salesforceCredentialsFileWanted = salesforceCredentialsFileWanted
        self.salesforceCredentialsFileName = csvFolder + "Salesforce_Credentials.csv"
        self.salesforcePerformanceGroupWanted = salesforcePerformanceGroupFileWanted
        self.salesforcePerformanceGroupFileName = csvFolder + "Salesforce_Performance_Group_members.csv"

    def showWindow(self):
        layout = [  [sg.Text('This is simple python programme used for creating CSV files for azuze and sending emails')],
             [sg.Text('Soubor se jmény', size=(15, 1), auto_size_text=False, justification='right'), sg.InputText('a.txt', key='-INPUT_FILE-'), sg.FileBrowse()],
             [sg.Radio('Pořadí jmen ve zdroji "Jméno Příjmení"', "PORADI", default=True, key='-JMENO_PRIJMENI-'), sg.Radio('Pořadí jmen ve zdroji "Příjmení Jméno"', "PORADI", key='-PRIJMENI_JMENO-')],
             [sg.T('Prosím zaškrtněte vše, co má program vykonat')],
             [sg.Text(size=(5, 1), auto_size_text=False), sg.Checkbox('Vygenerovat Azure_Bulk_User_Create.csv', key='-AZURE_USER-')],
             [sg.Text(size=(5, 1), auto_size_text=False), sg.Checkbox('Vygenerovat Azure_Bulk_Group_Add.csv', key='-AZURE_GROUP-')],
             [sg.Text(size=(5, 1), auto_size_text=False), sg.Checkbox('Vygenerovat Zeteo_User_Credentials.csv', key='-ZETEO_USER-')],
             [sg.Text(size=(5, 1), auto_size_text=False), sg.Checkbox('Vygenerovat Ustredna_User_Credentials.csv', key='-USTREDNA_USER-')],
             [sg.Text(size=(5, 1), auto_size_text=False), sg.Checkbox('Vygenerovat Zeteo_For_Jaachym.csv', key='-JAACHYM-')],
             [sg.Text(size=(5, 1), auto_size_text=False), sg.Checkbox('Rozeslat novým uživatelům maily', key='-MAIL-')],
             [sg.Button('Show'), sg.Button('Exit')]
         ]

        window = sg.Window('Window Title', layout)

        # event, values = window.read()
        
        # window.close()

        # print(event)
        # print(values)
        while True:  # Event Loop
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            if event == 'Show':
                print(values)

        window.close()

    def readUsersFromFile(self):
        newUsers = []
        with open(self.inputFileName, "r",  encoding="utf-8") as inputFile:
            middleName = ""
            for line in inputFile:
                words = line.split()
                words = list(filter(None, words))
                if len(words) < 2:
                    continue
                if len(words) > 2:
                    for x in range(1,len(words)-1):
                        middleName += " " + words[x]

                if self.firstName_secondName:
                    firstName = words[0]
                    secondName = words[len(words)-1]
                else:
                    secondName = words[0]
                    firstName = words[len(words)-1]

                newUsers.append(user(firstName, middleName, secondName, self.lastZeteoID))
                self.lastZeteoID += 1
        return newUsers

    def createCSVFiles(self):
        try:
                os.mkdir(csvFolder)
        except FileExistsError:
                pass
        if self.azureUserAddFileWanded:
            self.createAzureUserAddFile()
        if self.azureGroupAddFileWanded:
            self.createAzureGroupAddFile()
        if self.zeteoFileWanded:
            self.createZeteoCredentialsFile()
        if self.ustrednaFileWanded:
            self.createUstrednaCredentialsFile()
        if self.jaachymFileWanded:
            self.createJaachymFile()
        if self.nSureFileWanted:
            self.createnSureFile()
        if self.azureCredentialsWanted:
            self.createAzureCredentialsFile()
        if self.salesforceCredentialsFileWanted:
            self.createSalesforceFiles()
        if self.salesforcePerformanceGroupWanted:
            self.createPerformanceGroupFiles()

    def createAzureUserAddFile(self):
        try:
            with open(self.azureUserAddFileName, "r", encoding="utf-8") as file:
                pass
        except FileNotFoundError:
            with open(self.azureUserAddFileName, "w+", encoding="utf-8") as file:
                file.write("version:v1.0\n")
                file.write("Name [displayName] Required,User name [userPrincipalName] Required,Initial password [passwordProfile] Required,Block sign in (Yes/No) [accountEnabled] Required,First name [givenName],Last name [surname]\n")
                for person in self.newUsers:
                    file.write( person.firstName + person.middleName + " " + 
                                person.secondName + "," +
                                person.email + "," +
                                person.emailPass + "," + 
                                "No," + 
                                person.firstName + "," +
                                person.secondName + "\n")

    def createAzureGroupAddFile(self):
        try:
            with open(self.azureGroupAddFileName, "r", encoding="utf-8") as file:
                pass
        except FileNotFoundError:
            with open(self.azureGroupAddFileName, "w+",  encoding="utf-8") as file:
                file.write("version:v1.0\n")
                file.write("Member object ID or user principal name [memberObjectIdOrUpn] Required\n")
                for person in self.newUsers:
                    file.write(person.email + "\n")

    def createZeteoCredentialsFile(self):
        try:
            with open(self.zeteoFileName, "r", encoding="utf-8") as file:
                pass
        except FileNotFoundError:
            with open(self.zeteoFileName, "w+",  encoding="utf-8") as file:
                file.write("First name [givenName],Last name [surname],Zeteo universal email [zeteoEmailUniversal], Rixo telephone number [phoneNumber], Zeteo personal number [zeteoID], Zeteo role [zeteoRole], Zeteo user name [zeteoName] Required, Zeteo user password [zeteoPass] Required\n")
                for person in self.newUsers:
                    file.write( person.firstName + "," +
                                person.secondName + "," +
                                "pojisteni@rixo.cz" + "," +
                                "+420233089233" + "," + 
                                str(person.zeteoID) + ","
                                "Expert na pojištění" + "," +
                                person.zeteoName + "," +
                                person.zeteoPass + "\n")
    
    def createUstrednaCredentialsFile(self):
        try:
            with open(self.ustrednaFileName, "r", encoding="utf-8") as file:
                pass
        except FileNotFoundError:
            with open(self.ustrednaFileName, "w+",  encoding="utf-8") as file:
                file.write("First name [givenName],Last name [surname],Ustredna login name [ustrednaLogin], Ustredna password [ustrednaPass]\n")
                for person in self.newUsers:
                    file.write( person.firstName + "," +
                                person.secondName + "," + 
                                person.ustrednaName + "," +
                                person.ustrednaPass + "\n")

    def createJaachymFile(self):
        try:
            with open(self.jaachymFileName, "r", encoding="utf-8") as file:
                pass
        except FileNotFoundError:
            with open(self.jaachymFileName, "w+",  encoding="utf-8") as file:
                file.write("Member email [userEmail] Required, Zeteo ID [zeteoID] Required\n")
                for person in self.newUsers:
                    file.write( person.email + "," +
                                str(person.zeteoID) + "\n")

    def createnSureFile(self):
        try:
            with open(self.nSureFileName, "r", encoding="utf-8") as file:
                pass
        except FileNotFoundError:
            with open(self.nSureFileName, "w+",  encoding="utf-8") as file:
                file.write("First name [givenName],Last name [surname],Member email [userEmail] Required\n")
                for person in self.newUsers:
                    file.write( person.firstName + "," +
                                person.secondName + "," +
                                person.email + "\n")

    def createAzureCredentialsFile(self):
        try:
            with open(self.azureCredentialsFileName, "r", encoding="utf-8") as file:
                pass
        except FileNotFoundError:
            with open(self.azureCredentialsFileName, "w+",  encoding="utf-8") as file:
                file.write("Name [displayName] Required,Member email [userEmail] Required, Email password [emailPass]\n")
                for person in self.newUsers:
                    file.write( person.firstName + person.middleName + " " +
                                person.secondName + "," +
                                person.email + "," +
                                person.emailPass + "\n")

    def createSalesforceFiles(self):
        try:
            with open(self.salesforceCredentialsFileName, "r", encoding="utf-8") as file:
                pass
        except FileNotFoundError:
            with open(self.salesforceCredentialsFileName, "w+", encoding="utf-8") as file:
                file.write("FirstName,MiddleName,SecondName,Alis,UserName,Email,Phone,USERPERMISSIONSSUPPORTUSER,InsoftUserC,ProfileID,TimeZoneSidKey,LocaleSidKey,EmailEncodingKey,LanguageLocaleKey\n")
                for person in self.newUsers:
                    alias = person.firstName[0] + person.secondName[0:min(4,len(person.secondName))]
                    file.write( person.firstName + "," +
                                person.middleName + "," + 
                                person.secondName + "," +
                                alias + "," +
                                person.email + "," +
                                person.email + "," +
                                "+420 233 089 233" + "," +
                                "true" + "," +
                                "true" + "," + 
                                "00e2o0000013J6tAAE" + "," +
                                "Europe/Prague" + "," +
                                "cs_CZ" + "," +
                                "UTF-8" + "," +
                                "cs" + "\n"
                            )
    
    def createPublicGroupFiles(self):
        #USER ID + GROUP ID needed
        pass

    def createPermisionSetGroupFiles(self):
        #AssigneeID + ExpirationDate + PermissionSetGrouIP + PermissionSetID
        #exp date empty string
        pass

    def createPerformanceGroupFiles(self):
        #Assigned_Cases + User_C + Performance group ID
        pass

def blobcrement(number):
    if number < 20:
        number += 1
    print(number)

class printer (object):
    def __init__(self, users):
        self.users = users
        self.number = 4

    def incrementNumber(self):
        if self.number < len(self.users):
            self.number += 1
        print(self.number)

    def decrementNumber(self):
        if self.number > 0:
            self.number -= 1
        print(self.number)

    def printName(self):
        print(self.users[self.number].firstName)

    def printSurname(self):
        print(self.users[self.number].secondName)

if __name__ == '__main__':
    users = fileCreatorHandler("a.txt", 213)

    users.createCSVFiles()

    for user in users.newUsers:
        print(user)

    # print(len(users.newUsers))
    
    # i = 0
    # while True:
    #     while keyboard.is_pressed('ctrl'):
    #         if keyboard.is_pressed('p') and i < len(users.newUsers)-1:
    #             i += 1
    #             while keyboard.is_pressed('p'):
    #                 pass
    #         if keyboard.is_pressed('l') and i > 0:
    #             i -= 1
    #             print(i)
    #             while keyboard.is_pressed('l'):
    #                 pass
    #         if keyboard.is_pressed('m'):
    #             keyboard.write(users.newUsers[i].firstName)
    #             while keyboard.is_pressed('m'):
    #                 pass
    #         if keyboard.is_pressed(','):
    #             keyboard.write(users.newUsers[i].secondName)
    #             while keyboard.is_pressed(','):
    #                 pass
    #         if keyboard.is_pressed('.'):
    #             keyboard.write(users.newUsers[i].email)
    #             while keyboard.is_pressed('.'):
    #                 pass
    #         if keyboard.is_pressed('h'):
    #             keyboard.write(str(users.newUsers[i].zeteoID))
    #             while keyboard.is_pressed('h'):
    #                 pass
    #         if keyboard.is_pressed('j'):
    #             keyboard.write(users.newUsers[i].zeteoName)
    #             while keyboard.is_pressed('j'):
    #                 pass
    #         if keyboard.is_pressed('k'):
    #             keyboard.write(users.newUsers[i].ustrednaPass)
    #             while keyboard.is_pressed('k'):
    #                 pass
    #     if keyboard.is_pressed('g'):
    #         break
    


