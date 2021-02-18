# TODO

# DONE Generate random string
# DONE to lovercase
# DONE remove diacritic 
# DONE opening files

#doubory potrebne k vygenerovani
#Azure bulk add user csv
#Azire bulk add users to groups
#salesforce?
#Zeteo .csv? s nebo bez generování ID?

#CSV string version:v1.0
#Name [displayName] Required,User name [userPrincipalName] Required,Initial password [passwordProfile] Required,Block sign in (Yes/No) [accountEnabled] Required,First name [givenName],Last name [surname]

import unidecode
import random
import sys

vowels = "aeiouy"

consonants = "bcdfghjklmnpqrsvwxz"

def func():
	#i = 10;
	print("Hello")

	name = "Rozárka Ďublik"

	nameWithoutCarkyHacky = unidecode.unidecode(name)

	print(nameWithoutCarkyHacky.lower())

	blob = nameWithoutCarkyHacky.lower().split(" ");
	firstName = blob[0]
	lastName = blob[1]
	print(firstName)
	#print(lastName)

	#Váňová Kateřina,katerina.vanova@rixo.cz,NoveHeslo1,No,Kateřina,Váňová

	newLine = lastName+" "+firstName+","

	#print(newLine)
def createCSVFiles(inputFileName, lastZeteoID = -1):
	newUserNames = readUserNamesFromFile(inputFileName)
	createAzureFiles(newUserNames)
	if lastZeteoID != -1:
		createZeteoFiles(newUserNames, lastZeteoID)

def createZeteoFiles(newUserNames, lastZeteoID):
	with open("Zeteo_For_Jaachym.csv", "w+") as file:
		file.write("Member email [userEmail] Required, Zeteo ID [zeteoID] Required\n")
		for person in newUserNames:
			file.write(createZeteoForJaachymLine(person[0], person[1], lastZeteoID))
			lastZeteoID += 1

	with open("Zeteo_Bulk_User_Credentials.csv", "w+") as file:
		file.write("Zeteo ID [zeteoID] Required, User name [zeteoUserID], Zeteo password [zeteoPassword]\n")
		for person in newUserNames:
			file.write(createZeteoUserCreateLine(person[0], person[1], lastZeteoID))
			lastZeteoID += 1

def createZeteoUserCreateLine(firstName, secondName, zeteoID):
	line = ""
	line += str(zeteoID)+","
	line += unidecode.unidecode(firstName.lower())+"."+unidecode.unidecode(secondName.lower())
	line += generagePassword()

	return line

def createZeteoForJaachymLine(firstName, secondName, zeteoID):
	line = ""
	line += createEmail(firstName, secondName)+","
	line += str(zeteoID)+"\n"

	return line



def createAzureFiles(newUserNames):
	with open("Azure_Bulk_User_Create.csv", "w+") as file:
		file.write("Name [displayName] Required,User name [userPrincipalName] Required,Initial password [passwordProfile] Required,Block sign in (Yes/No) [accountEnabled] Required,First name [givenName],Last name [surname]\n")
		for person in newUserNames:
			file.write(createUserAzureLine(person[0], person[1]))

	with open("Azure_Bulk_Group_Add.csv", "w+") as file:
		file.write("Member email [userEmail] Required\n")
		for person in newUserNames:
			file.write(addGroupAzureLine(person[0], person[1]))
	
		
def readUserNamesFromFile(inputFileName):
	newUserNames = []
	with open(inputFileName, "r") as inputFile:
		for line in inputFile:
			line = line.strip('\n')
			words = line.split(" ")
			if len(words) < 2:
				continue
			if len(words) > 2:
				for x in range(1,len(words)-1):
					words[0] += " " + words[x]
			firstName = words[0]
			secondName = words[len(words)-1]
			newUserNames.append((firstName, secondName))
	return newUserNames


def generagePassword():
	passwordLength = random.randint(8, 10)
	x = 0;

	password = ""

	while x < 3*passwordLength/5:
		if x%2 == 0:
			password += random.choice(consonants)
		else:
			password += random.choice(vowels)
		x += 1

	while x < passwordLength:
		password += str(random.randint(0,9))
		x += 1
	return password


def createUserAzureLine(firstName, secondName):
	line = ""

	line += secondName+" "+firstName+","
	line += createEmail(firstName,secondName)+","
	line += generagePassword()+","
	line += "No,"
	line += firstName+","
	line += secondName+"\n"

	return line

def addGroupAzureLine(firstName, secondName):
	line = createEmail(firstName, secondName)+"\n"

	return line

def createEmail(firstName, secondName):
	if len(firstName.split(" ")) > 1:
		firstName = firstName[0]
	firstName = unidecode.unidecode(firstName.lower())
	secondName = unidecode.unidecode(secondName.lower())
	email = firstName+"."+secondName+"@rixo.cz"

	return email

if __name__ == '__main__':
	if len(sys.argv) > 1:
		createCSVFiles("a.txt", int(sys.argv[1]))
	else:
		createCSVFiles("a.txt")