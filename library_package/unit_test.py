import unittest
from library import Library, Crypto, DateTime

class TestLibrary(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # this method is only run once for the entire class rather than being run for each test which is done for setUp()
        self.library = Library("/library_package/", 1000)

    ''' test Create function'''
    def testCreate(self):
        # get current datetime
        timestamp = DateTime.get_datetime()
        # encrypt timestamp
        encrypt_timestamp = Crypto.encrypt(timestamp)
        # return message
        message = self.library.create(encrypt_timestamp)
        # pop out Assertion Error if failure condition happens
        self.assertEqual(message, 'success: timestamp file created !')

    ''' test CheckExpiry function '''
    def testCheckExpiry(self):
        # get sign of check
        check = self.library.check_expiry()
        # pop out Assertion Error if failure condition happens
        self.assertTrue(check)

    ''' test Inspect function '''
    def testInspect(self):
        # get timestamp
        encrypted_timestamp = self.library.inspect()
        # pop out Assertion Error if Inspect returns ""
        self.assertNotEqual(encrypted_timestamp, "")

if __name__ == "__main__":

    unittest.main()


        

