# User Data: Stores the data for one user

class UserData:
    def __init__(self, newUsername, newPassword, newPhone, newEmail):
        self.username = newUsername
        self.password = newPassword
        self.phone = newPhone
        self.email = newEmail
    
    # Get methods for data in object
    def getUsername(self):
        return self.username

    def getPassword(self):
        return self.password

    def getPhone(self):
        return self.phone

    def getEmail(self):
        return self.email
    
    # Returns True if given user matches the object's username
    def isUser(self, otherUser):
        return otherUser.getUsername().lower() == self.username.lower()

    # Returns True if given username matches the object's username
    def isUsername(self, otherUsername):
        return otherUsername.lower() == self.username.lower()

    # Returns True if given password matches correct password
    def checkPassword(self, otherPassword):
        return otherPassword == self.password
    
    # Printing for debugging
    def printAllData(self):
        print(f"User: {self.username}\n\tPass: {self.password}\n\tEmail: {self.email}\n\tPhone: {self.phone}")