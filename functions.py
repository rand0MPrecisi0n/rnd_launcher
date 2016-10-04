#!/usr/bin/python3
"""Defines the functions for use in Twitch Launcher using object-oriented programming"""

########### Colocar autenticador
########### 
###########




import subprocess, shelve

class Db:
    
    def __init__(self, name, oauth):
        self.dict = {}
        self.name = name
        self.oauth = oauth
        self.shelf = str(self.name+"_settings.shlf")
        try: 
            f = open(name, 'r')
            for line in f.readlines():
                self.dict[line.split()[0]] = int(line.split()[1])
            f.close()
        except FileNotFoundError:
            f = open(name, 'w')
            f.close()
        shelf = shelve.open(self.shelf, writeback=True)
        try:
            shelf["chat"]
            shelf.close()
        except KeyError:
            shelf["chat"] = True
            shelf.close()
        
    def launcher(self, stream, quality):
        """Launches the stream on livestreamer"""
        for i in range(3):
            print("*"*38)
        print("   LAUNCHING {0} ON {1} ".format(stream.upper(), quality.upper()))
        for i in range(3):
            print("*"*38)
            
        shelf = shelve.open(self.shelf)
        if shelf["chat"]:
            subprocess.Popen(r"channel="+stream+r" ; quality="+quality+r"; chromium-browser --app=https://www.twitch.tv/$channel/chat?popout= ; livestreamer --twitch-oauth-token "+self.oauth+r" https://www.twitch.tv/$channel $quality", shell=True)
        else:
            subprocess.Popen(r"channel="+stream+r" ; quality="+quality+r"; livestreamer --twitch-oauth-token "+self.oauth+r" https://www.twitch.tv/$channel $quality", shell=True)
        shelf.close()


    def add_db(self, stream):
        """Adds selected stream to the database and counts the number of times it's been launched"""
        if stream in self.dict:
            self.dict[stream] += 1
        else:
            self.dict[stream] = 1
    
    def save_db(self):
        """Saves current database to file"""
        f = open(self.name, "w")
        for k, v in self.dict.items():
            f.writelines("{0} {1}\n".format(k, v))
        f.close()
        print("Database saved successfully")
    
    def display_db(self):
        """Displays database ordered by number of times watched"""
        self.list = sorted((zip(self.dict.values(), self.dict.keys())))
#        self.list = sorted(self.dict.items(), key=lambda kv: kv[1], reverse=True)
        self.list.reverse()
        print()
        print("{0:*^60}\n".format(" STREAM LIST "))
        for rank, stream in enumerate(self.list):
            print("{0:<4}{1:<15.15} watched {2} times".format(rank+1, stream[1], stream[0]))
        print()
        
    def clear_db(self):
        """Clears entire database"""
        while True:
            confirmation = input("Are you sure? y/n: ")
            if confirmation == "y":
                f = open(self.name, 'w')
                f.close()
                self.dict = {}
                print("\nDatabase successfully cleared\n")
                break
            elif confirmation == "n":
                break
            else:
                print("\nPlease select a valid option\n")
        
    def help(self):
        """Displays the help text"""
        print("\n{0:*^60}".format(" HELP "))
#        print("{0}\n{1}\n{2}\n{3}\n{4}\n: ".format
        print(
                        "Available commands: \n", 
                        "list   : displays a list of all accessed streams \n", 
                        "h/help : displays this help \n", 
                        "clear  : clears the stream database \n", 
                        "back   : goes back from quality selection to stream selection \n", 
                        "chat   : turns chat on/off \n",
                        "quit   : quits the program \n",
						"default: defaults to the selected user next time you launch the application \n",
						"oauth	: changes the current user 'oauth' authentication \n",
                        )

    def chat_settings(self):
        """Turns the chat on/off"""
        shelf = shelve.open(self.shelf, writeback=True)
        while True:
            option = input("Do you want chat? y/n: ")
            if option == "y":
                shelf["chat"] = True
                shelf.close()
                print("Chat has been enabled")
                break
            elif option == "n":
                shelf["chat"] = False
                shelf.close()
                print("Chat has been disabled")
                break
            else:
                print("Please select a valid option")

    def default(self):
        """Sets the current user to default"""
        shelf = shelve.open("default.shlf", writeback=True)
        shelf["default"] = self.name
        print("Default user changed successfully")

    def oauth_token(self):
        """Changes the current user oauth authentication"""
        shelf = shelve.open('default.shlf', writeback=True)
        self.newoauth = input("Please type the new OAUTH token: ")
        if self.newoauth:
            shelf["oauth"] = self.newoauth
            print("OAUTH changed successfully")
        else: 
            print("Nothing was changed")
        shelf.close()

##############
#############		Tests
###########		   
import unittest, tempfile, shutil, glob, os

class FileTest(unittest.TestCase):

    def setUp(self):
        """Sets Up the test environment"""
        self.test = Db("test")
        self.test.add_db("summit1g")
        self.test.add_db("summit1g")
        self.test.add_db("lirik")
    
    def test_display(self):
        """Tests if the database is being displayed properly by 'list' command"""
        self.test.display_db()
        self.assertEqual(self.test.list, [(2, 'summit1g'), (1, 'lirik')], "Lists don't match")
    
    def test_adddb(self):
        """Tests if the add_db() function is working properly"""
        self.test.add_db("overzero")
        self.test.add_db("summit1g")
        self.assertEqual(self.test.dict, {"summit1g": 3, "lirik": 1, "overzero": 1}, "Streams not being added to the database, or being counted wrong")
    
    def test_save(self):
        """Tests if database is being saved properly"""
        self.test.save_db()
        self.dict = {}
        f = open(self.test.name, 'r')
        for line in f.readlines():
            self.dict[line.split()[0]] = int(line.split()[1])
        self.assertEqual(self.dict, self.test.dict, "Dicts don't match")
        f.close()
    
    def test_clear(self):
        """Tests if database is being cleared properly"""
        self.test.clear_db()
        f = open(self.test.name, 'r')
        self.assertEqual(f.read(), '', "Database not empty")
        f.close()
    
#    def test_settings(self):
        """Tests if settings are being changed properly"""
        pass 
    
    def tearDown(self):
        os.remove(self.test.name)
        
if __name__ == "__main__":
    unittest.main()
