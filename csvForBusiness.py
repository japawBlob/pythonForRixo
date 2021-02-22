import unidecode
import random
import sys

vowels = "aeiouy"

consonants = "bcdfghjklmnpqrsvwxz"

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

	upperChar = random.randint(0, x-1)
	password = password[:upperChar] + password[upperChar].upper() + password[(upperChar+1):]

	while x < passwordLength:
		password += str(random.randint(0,9))
		x += 1
	return password


class user(object):
	def __init__(self, firstName, secondName, zeteoID = -1):
		self.firstName = firstName
		self.secondName = secondName
		self.email = self.createEmail()
		self.emailPass = generagePassword()
		self.zeteoName = self.createZeteoName()
		self.zeteoPass = generagePassword()
		self.zeteoID = zeteoID
		self.ustrednaName = self.email
		self.ustrednaPass = generagePassword()

	def createEmail(self):
		firstName = unidecode.unidecode(self.firstName).lower();
		secondName = unidecode.unidecode(self.secondName).lower();
		email = firstName+"."+secondName+"@rixo.cz"
		return email

	def createZeteoName(self):
		firstName = unidecode.unidecode(self.firstName).lower();
		secondName = unidecode.unidecode(self.secondName).lower();
		zeteoName = firstName+"."+secondName
		return zeteoName

	def __str__(self):
		return self.firstName + " " + self.secondName + " " + self.email 

class fileCreatorHandler(object):
	def __init__(self, inputFileName, lastZeteoID = -1, azureUserAddFileWanded = True, azureGroupAddFileWanded = True, zeteoFileWanded = True, ustrednaFileWanded = True, jaachymFileWanded = True):
		self.inputFileName = inputFileName
		self.newUsers = self.readUsersFromFile()
		self.azureUserAddFileWanded = azureUserAddFileWanded
		self.azureUserAddFileName = "Azure_Bulk_User_Create.csv"
		self.azureGroupAddFileWanded = azureGroupAddFileWanded
		self.azureGroupAddFileName = "Azure_Bulk_Group_Add.csv"
		self.zeteoFileWanded = zeteoFileWanded
		self.zeteoFileName = "Zeteo_User_Credentials.csv"
		self.ustrednaFileWanded = ustrednaFileWanded
		self.ustrednaFileName = "Ustredna_User_Credentials.csv"
		self.jaachymFileWanded = jaachymFileWanded
		self.jaachymFileName = "Zeteo_For_Jaachym.csv"

	def readUsersFromFile(self):
		newUsers = []
		with open(self.inputFileName, "r") as inputFile:
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
				newUsers.append(user(firstName, secondName))
		return newUsers

	def createCSVFiles(self):
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

	def createAzureUserAddFile(self):
		with open("Azure_Bulk_User_Create.csv", "w+") as file:
			file.write("version:v1.0\n")
			file.write("Name [displayName] Required,User name [userPrincipalName] Required,Initial password [passwordProfile] Required,Block sign in (Yes/No) [accountEnabled] Required,First name [givenName],Last name [surname]\n")
			for person in self.newUsers:
				file.write(	person.secondName + " " + 
							person.firstName + "," +
							person.email + "," +
							person.emailPass + "," + 
							"No," + 
							person.firstName + "," +
							person.secondName + "\n")

	def createAzureGroupAddFile(self):
		with open(self.azureGroupAddFileName, "w+") as file:
			file.write("version:v1.0\n")
			file.write("Member object ID or user principal name [memberObjectIdOrUpn] Required\n")
			for person in self.newUsers:
				file.write(person.email + "\n")

	def createZeteoCredentialsFile(self):
		with open(self.zeteoFileName, "w+") as file:
			file.write("version:v1.0\n")
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
		with open(self.ustrednaFileName, "w+") as file:
			file.write("version:v1.0\n")
			file.write("First name [givenName],Last name [surname],Ustredna login name [ustrednaLogin], Ustredna password [ustrednaPass]\n")
			for person in self.newUsers:
				file.write( person.firstName + "," +
							person.secondName + "," + 
							person.ustrednaName + "," +
							person.ustrednaPass + "\n")

	def createJaachymFile(self):
		with open(self.jaachymFileName, "w+") as file:
			file.write("version:v1.0\n")
			file.write("Member email [userEmail] Required, Zeteo ID [zeteoID] Required\n")
			for person in self.newUsers:
				file.write( person.email + "," +
							str(person.zeteoID) + "\n")

if __name__ == '__main__':
	users = fileCreatorHandler("a.txt")

	users.createCSVFiles();
