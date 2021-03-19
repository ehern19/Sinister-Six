# User Data: Stores the data for one user

class UserData:
    def __init__(self, newUsername, newPassword, newEmail, newPhone):
        self.username = newUsername
        self.password = newPassword
        self.email = newEmail
        self.phone = newPhone
    
    # Get methods for data in object
    def getUsername(self):
        return self.username

    def getPassword(self):
        return self.password

    def getEmail(self):
        return self.email
    
    def getPhone(self):
        return self.phone

    # Returns True if given username matches the object's username
    def isUser(self, otherUsername):
        return otherUsername == self.username

    # Returns True if given password matches correct password
    def checkPassword(self, otherPassword):
        return otherPassword == self.password
    
    # Printing for debugging
    def printAllData(self):
        print(f"User: {self.username}\n\tPass: {self.password}\n\tEmail: {self.email}\n\tPhone: {self.phone}")