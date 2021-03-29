#                                           Summary:
# This class manages data flow by storing and returning user data from our
# "database" file.
#
#
#
#                                          Data Members:
#
# userName, password, phone, email.
#
#
#
#                                           Methods:
#
# "loadData": Loads the data of the user from a file to an object stored in the memory.
#
# "saveData": Saves the data of the user from an object stored in the memory to a file.




# User IO: Store and retrieve user data from file
# Child of DataIO class

from DataIO import DataIO
from dataClasses.UserData import UserData

# Data is stored as a list of UserData objects
class UserIO(DataIO):
    filePath = DataIO.databasePath + DataIO.userdataFilename
    # Load User data from file to memory in object
    def loadData(self) -> None:
        with open(self.filePath, 'r') as inFile:
            for line in inFile:
                line = line.strip().split()

                # Separate the line into relevant categories
                username = line.pop(0)
                password = line.pop(0)
                phone = line.pop(0)
                email = line.pop(0)

                # Add new UserData object to this object's data list
                self.data.append(UserData(username, password, phone, email))
        
    # Save User data to file from memory in object
    def saveData(self) -> None:
        with open(self.filePath, 'w') as outFile:
            for user in self.data:
                # Create a list with username, password, email, and phone
                line = []
                line.append(user.getUsername())
                line.append(user.getPassword())
                line.append(user.getPhone())
                line.append(user.getEmail())

                # Convert to single line string
                line = ' '.join(line)

                # Print line to file
                print(line, file=outFile)

if __name__=="__main__":
    users = UserIO()
    users.loadData()
    for user in users.getData():
        user.printAllData()
    users.saveData()