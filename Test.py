from Client import Client
from ThreadedServer import ThreadedServer
from threading import Thread
import unittest
import builtins


class Testing(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        self.client.cleanup()

    '''
    Override the input() function to return my own input data
    '''
    @staticmethod
    def __set_input(input_text):
        builtins.input = lambda prompt: input_text

    '''
    Help Menu
    '''
    def test_help_menu(self):
        self.__set_input('h')

        assert self.client.listen() == "Help Menu\n" + \
            "Add a value to the dictionary:\n" \
            "    set <key>:<value>\n" \
            "Retrieve a value from the dictionary:\n" \
            "    get <key>\n" \
            "Delete a value from the dictionary:\n" \
            "     delete <key>\n" + \
            "See all values in the dictionary:\n" \
            "    showall\n" \
            "Please note that values stored by one user can by accessed by any other user."

    '''
    Set
    '''
    def test_00_bad_set_1(self):
        self.__set_input('set')
        self.assertEqual(self.client.listen(), 'Must have key and value in set command')

    def test_01_bad_set_2(self):
        self.__set_input('set key')
        self.assertEqual(self.client.listen(), 'Must have key and value in set command')

    def test_02_set_1(self):
        self.__set_input('set stevie:ray vaughn')
        self.assertEqual(self.client.listen(), 'Set new entry\n    key: stevie, value: ray vaughn')

    def test_03_set_2(self):
        self.__set_input('set steve:miller')
        self.assertEqual(self.client.listen(), 'Set new entry\n    key: steve, value: miller')

    '''
    Get
    '''
    def test_04_bad_get(self):
        self.__set_input('get foo')
        self.assertEqual(self.client.listen(), 'Could not find an entry for that key')

    def test_05_get_1(self):
        self.__set_input('get stevie')
        self.assertEqual(self.client.listen(), 'ray vaughn')

    def test_06_get_2(self):
        self.__set_input('get steve')
        self.assertEqual(self.client.listen(), 'miller')

    '''
    Showall
    '''
    def test_07_showall(self):
        self.__set_input('showall')
        self.assertEqual(self.client.listen(), "{'stevie': 'ray vaughn', 'steve': 'miller'}")

    '''
    Delete
    '''
    def test_08_bad_delete(self):
        self.__set_input('delete bar')
        self.assertEqual(self.client.listen(), 'Could not find an entry for that key')

    def test_09_delete(self):
        self.__set_input('delete stevie')
        self.assertEqual(self.client.listen(), 'Deleted stevie')

    '''
    Exit
    '''
    def test_exit(self):
        self.__set_input('exit')
        self.assertEqual(self.client.listen(), 'Goodbye :-)')


if __name__ == "__main__":
    # Start server
    server_thread = Thread(target=ThreadedServer('', 12345).listen)
    server_thread.daemon = True
    server_thread.start()
    unittest.main()
