# User Data: Stores the data for one user

class UserData:
    def __init__(self, newUsername: str, newPassword: str, newPhone: str, newEmail: str):
        self.username = newUsername
        self.password = newPassword
        self.phone = newPhone
        self.email = newEmail
    
    # Get methods for data in object
    def getUsername(self) -> str:
        return self.username

    def getPassword(self) -> str:
        return self.password

    def getPhone(self) -> str:
        return self.phone

    def getEmail(self) -> str:
        return self.email
    
    # Returns True if given username matches the object's username
    def isUsername(self, otherUsername: str) -> bool:
        return otherUsername.lower() == self.username.lower()

    # Returns True if given password matches correct password
    def checkPassword(self, otherPassword: str) -> bool:
        return otherPassword == self.password
    
    # Printing for debugging
    def printAllData(self) -> None:
        print(f"User: {self.username}\n\tPass: {self.password}\n\tEmail: {self.email}\n\tPhone: {self.phone}")

# Returns True if given user matches the object's username
def isUser(self: UserData, otherUser: UserData) -> bool:
    return otherUser.getUsername().lower() == self.username.lower()

UserData.isUser = isUser