#!/usr/bin/python3
"""Defines the functions for use in Twitch Launcher using object-oriented programming"""

#colocar o display_name na shelf

import subprocess, shelve, requests
from os import name

class Db:
    
    def __init__(self, name, oauth_rnd, oauth_ls):
        self.dict = {}
        self.name = name
        self.oauth_rnd = oauth_rnd
        self.oauth_ls = oauth_ls
        self.shelf = str(self.name+"_settings.shlf")
        self.sup_browsers = ("chrome", "chromium-browser", "firefox", "iexplore")
        self.os = os.name
        try: 
            f = open(name, 'r')
            for line in f.readlines():
                try:
                    self.dict[line.split()[0]] = int(line.split()[1])
                except IndexError:
                    continue
            f.close()
        except FileNotFoundError:
            f = open(name, 'w')
            f.close()
        shelf = shelve.open(self.shelf, writeback=True)
        try:
            shelf["display_name"]
        except KeyError:
            fl = requests.get("https://api.twitch.tv/kraken/user?oauth_token="+self.oauth_rnd)
            shelf["display_name"] = fl.json()['display_name']
        try:
            shelf["chat"]
        except KeyError:
            shelf["chat"] = True
        try:
            shelf["browser"]
        except KeyError:
            while True:
                browser = input("Please enter your preferred browser (chrome, chromium-browser, firefox, iexplore): ")
                if browser == 'chrome' or 'chromium-browser' or 'firefox' or 'iexplore':
                    shelf["browser"] = browser
                    break
                else:
                    print("Entered browser is not supported")
        
    def launcher(self, stream, quality):
        """Launches the stream on livestreamer"""
        for i in range(3):
            print("*"*38)
        print("   LAUNCHING {0} ON {1} ".format(stream.upper(), quality.upper()))
        for i in range(3):
            print("*"*38)
            
        shelf = shelve.open(self.shelf)
        if self.os == 'nt':  
            if shelf["chat"]:
                if shelf["browser"] in self.sup_browsers[:2]:
                    os.system("start "+shelf["browser"]+" --app=https://www.twitch.tv/"+stream+"/chat?popout=")
                else:
                    os.system("start "+shelf["browser"]+" https://www.twitch.tv/"+stream+"/chat?popout=")
            os.system("livestreamer --twitch-oauth-token "+self.oauth_ls+r" https://www.twitch.tv/"+stream+" "+quality)

        else:
            if shelf["chat"]:
                if shelf["browser"] in self.sup_browsers[:2]:
                    subprocess.Popen(r"channel="+stream+r" ; quality="+quality+r"; "+shelf["browser"]+r" --app=https://www.twitch.tv/$channel/chat?popout=", shell=True)
                else:
                    subprocess.Popen(r"channel="+stream+r" ; quality="+quality+r"; "+shelf["browser"]+r" https://www.twitch.tv/$channel/chat?popout=", shell=True)
            subprocess.Popen("livestreamer --twitch-oauth-token "+self.oauth_ls+r" https://www.twitch.tv/"+stream+" "+quality, shell=True)
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
                        "list       : displays a list of all accessed streams \n", 
                        "h/help     : displays this help \n", 
                        "clear      : clears the stream database \n", 
                        "back       : goes back from quality selection to stream selection \n", 
                        "chat       : turns chat on/off \n",
                        "quit       : quits the program \n",
						"default    : makes the current user default \n",
                        "live       : displays live followed streams \n",
                        "fl stream  : follows given stream \n",
                        "unf stream : unfollows given stream \n",
                        "browser    : displays/changes currently selected browser \n",
						"oauth	    : changes the current user 'oauth' authentication \n",
                        "show oauth : displays user's oauth tokens \n"
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

    def open_chat(self, chat):
        """Opens chat for specified channel"""
        pass

    def browser_settings(self):
        """Changes the default browser"""
        shelf = shelve.open(self.shelf, writeback=True)
        print("The default browser is "+shelf["browser"])
        while True:
            browser = input("Please enter the new browser of choice, or enter to skip (chrome, chromium-browser, iexplore or firefox): ")
            if browser in self.sup_browsers:
                shelf["browser"] = browser
                break
            elif bool(browser) == False:
                break
            else:
                print("Selected browser is unsupported")
        shelf.close()

    def default(self):
        """Sets the current user to default"""
        shelf = shelve.open("default.shlf", writeback=True)
        shelf["default"] = self.name
        print("Default user changed successfully")

###############
######## API ##
###############

# BROKEN corrigir    def oauth_token(self):
        #"""Changes the current user oauth authentication"""
        #shelf = shelve.open('default.shlf', writeback=True)
        #self.newoauth = input("Please type the new OAUTH token: ")
        #if self.newoauth:
        #    shelf["oauth"] = self.newoauth
        #    print("OAUTH changed successfully")
        #else: 
        #    print("Nothing was changed")
        #shelf.close()

    def show_oauth(self):
        """Shows the current user oauth tokens"""
        shelf = shelve.open('default.shlf', writeback=True)
        print("rnd_launcher token = "+shelf["oauth_rnd"])
        print("livestreamer token = "+shelf["oauth_ls"])
        shelf.close()

    def live(self):
        """Displays online followed channels"""
        games = []
        streams = []
        fl = requests.get("https://api.twitch.tv/kraken/streams/followed?oauth_token="+self.oauth_rnd)
        if self.os == 'nt': #Windows implementation (utf-8 encoding)
            for i in range(len(fl.json()['streams'])):
                if fl.json()['streams'][i]['game'] not in games:
                    games.append(fl.json()['streams'][i]['game'])
                streams.append((fl.json()['streams'][i]['channel']['name'], fl.json()['streams'][i]['channel']['status'].encode('utf-8'), fl.json()['streams'][i]['game']))
            games.sort()
            print("\n{0:*^60}".format(""))
            print("{0:*^60}".format("LIST OF ONLINE STREAMS"))
            ("{0:*^60}".format(""))
            for i in range(len(games)):
                print(u"\n{0}{1}".format("*"*10, games[i]))
                for c in range(len(streams)):
                    if streams[c][2] == games[i]:
                        print(streams[c][0], ":", streams[c][1])
            print("\n")

        else: #Linux implementation (no encoding)
            for i in range(len(fl.json()['streams'])):
                if fl.json()['streams'][i]['game'] not in games:
                    games.append(fl.json()['streams'][i]['game'])
                streams.append((fl.json()['streams'][i]['channel']['name'], fl.json()['streams'][i]['channel']['status'], fl.json()['streams'][i]['game']))
            games.sort()
            print("\n{0:*^60}".format(""))
            print("{0:*^60}".format("LIST OF ONLINE STREAMS"))
            ("{0:*^60}".format(""))
            for i in range(len(games)):
                print(u"\n{0}{1}".format("*"*10, games[i]))
                for c in range(len(streams)):
                    if streams[c][2] == games[i]:
                        print(streams[c][0], ":", streams[c][1])
            print("\n")
#        for i in range(len(fl.json()['streams'])):               
#                print("{0:<10} | game: {1}\n{2}".format(fl.json()['streams'][i]['channel']['name'], fl.json()['streams'][i]['game'], fl.json()['streams'][i]['channel']['status']))
      
    def follow(self, stream):
        """Follows given stream"""
        shelf = shelve.open(self.shelf, writeback=True)
        fl  = requests.put(r"https://api.twitch.tv/kraken/users/"+shelf["display_name"]+r"/follows/channels/"+stream+"?oauth_token="+self.oauth_rnd)
        print("Channel "+stream+" followed successfully")
        shelf.close()

    def unfollow(self, stream):
        """Follows given stream"""
        shelf = shelve.open(self.shelf, writeback=True)
        fl  = requests.delete(r"https://api.twitch.tv/kraken/users/"+shelf["display_name"]+r"/follows/channels/"+stream+"?oauth_token="+self.oauth_rnd)
        print("Channel "+stream+" unfollowed successfully")
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
