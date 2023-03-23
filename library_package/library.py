import os
import sys
import time
from datetime import datetime

class Library:
    def __new__(cls, *args, **kwargs):
        return super(Library, cls).__new__(cls)
    
    def __init__(self, path: str, trialPeriod: float):

        # create the file path
        self.filePath = path + "timestamp_file.txt"
        # set trial period
        self.trialPeriod = trialPeriod
        # decrypted timestamp: protected attribute, accessing from class outside is NOT ALLOWED
        self._decrypted_timestamp = float("inf")

    ''' 1.  A function to create a start timestamp when the software product is installed '''
    def create(self, encrypted_timestamp: str):

        # timestamp file already exists
        if self.exit():
            # return failure condition message directly to the screen console
            error_message = 'failure condition: timestamp file already exists !'
            return error_message
        
        # set decrypted timestamp
        self.set_decrypted_timestamp(encrypted_timestamp)
        
        # open a file in write mode
        file = open(self.filePath, 'w')
        # write timestamp to the file
        file.write(encrypted_timestamp)
        # close the file
        file.close()

        success_message = 'success: timestamp file created !'
        return success_message

    ''' 2.  A function to check the expiry '''
    def check_expiry(self):
        
        # the timestamp file does not exist
        if not self.exit():
            sys.stdout.write('failure condition: timestamp file does not exist !')
            return False
        
        # open the file in read mode
        file = open(self.filePath, 'r')
        # read the encrypted timestamp from file
        encrypted_timestamp = file.read()
        # decrypt the encrypted timestamp
        decrypted_timestamp_A = Crypto.decrypt(encrypted_timestamp)
        # get previously decrypted timestamp inside class
        decrypted_timestamp_B = self.get_decrypted_timestamp()
        # close the file
        file.close()

        # the timestamp cannot be decrypted back to its original form (tampered)
        if decrypted_timestamp_A != decrypted_timestamp_B:
            sys.stdout.write('failure condition: the timestamp cannot be decrypted back to its original form (tampered) !')
            return False
        
        # get current datetime
        decrypted_timestamp_C = DateTime.get_datetime()

        # the duration between current time and the decrypted timestamp is longer than the trial period (expired).
        if decrypted_timestamp_C - decrypted_timestamp_A > self.trialPeriod:
            sys.stdout.write('failure condition: the duration between current time and the decrypted timestamp is longer than the trial period (expired) !')
            return False

        sys.stdout.write('Success !')
        return True
    
    ''' 3.	A function to inspect the timestamp '''
    def inspect(self):

        # current timestamp file path exists
        if self.exit():
            # open a file in read mode
            file = open(self.filePath, 'r')
            # read the encrypted_timestamp from file
            encrypted_timestamp = file.read()
            # close the file
            file.close()
            # return the encrypted_timestamp
            return encrypted_timestamp

        # current timestamp file path does not exist
        return ""
    
    ''' check whether file exists '''
    def exit(self):

        # return True if the file exists
        # return False if the file does not exist
        return os.path.exists(self.filePath)
    
    ''' get decrypted timestamp '''
    def get_decrypted_timestamp(self):
        return self._decrypted_timestamp

    ''' set decrypted timestamp '''
    def set_decrypted_timestamp(self, encrypted_timestamp: str):
        self._decrypted_timestamp = Crypto.decrypt(encrypted_timestamp)

class Crypto:
    def __new__(cls, *args, **kwargs):
        return super(Crypto, cls).__new__(cls) 
    
    @staticmethod
    def encrypt(decrypt_timestamp: float):

        # hashtable used to convert numeric to alpha
        encrypt_hashtable = {".": "A", "0": "B", "1": "C", "2": "D", "3": "E", "4": "F", "5": "G", "6": "H", "7": "I", "8": "J", "9": "K"}

        # covert float datatype to string datatype
        string_decrypt_timestamp = str(decrypt_timestamp)

        # initilize encrypted_timestamp
        encrypted_timestamp = ""

        # ex. 2528.733159 -> DGDJAEECGK
        # iterate over every single character in string_decrypt_timestamp
        for char in string_decrypt_timestamp:
            encrypted_timestamp += encrypt_hashtable.get(char)

        return encrypted_timestamp
        
    @staticmethod
    def decrypt(encrypt_timestamp: str):

        # hashtable used to convert alpha to numeric
        decrypt_hashtable = {"A": ".", "B": "0", "C": "1", "D": "2", "E": "3", "F": "4", "G": "5", "H": "6", "I": "7", "J": "8", "K": "9"}

        # initilize decrypted_timestamp
        decrypted_timestamp = ""

        # ex. DGDJAEECGK -> 2528.733159
        # iterate over every single character in encrypt_timestamp
        for char in encrypt_timestamp:
            decrypted_timestamp += decrypt_hashtable.get(char)

        # convert string datatype to float datatype
        float_decrypted_timestamp = float(decrypted_timestamp)

        return float_decrypted_timestamp
    
class DateTime:
    def __new__(cls, *args, **kwargs):
        return super(DateTime, cls).__new__(cls) 
    
    @staticmethod
    def get_datetime():

        # get current date and time
        dt = datetime.now()
        # get the timestamp
        timestamp = datetime.timestamp(dt)

        return timestamp

if __name__ == "__main__":

    ''' /library_package/ '''
    ''' trialPeriod = 1000 '''
    ''' checkPeriod = 4 '''

    ''' console application used to receive input from the keyboard'''
    # get the file path from command line
    file_path = sys.argv[1]
    # get the trialPeriod from command line
    trialPeriod = float(sys.argv[2])
    # get the check time from command line
    checkPeriod = int(sys.argv[3])

    # declare library object
    LibraryAPI = Library(file_path, trialPeriod)

    # get current datetime
    timestamp = DateTime.get_datetime()
    # encrypt timestamp
    encrypt_timestamp = Crypto.encrypt(timestamp)

    # create a start timestamp
    LibraryAPI.create(encrypt_timestamp)

    while LibraryAPI.check_expiry():

        # create a start timestamp
        LibraryAPI.create(encrypt_timestamp)
        # inspect timestamp
        print("current timestamp: ", LibraryAPI.inspect())
        # check periodically
        time.sleep(checkPeriod)

