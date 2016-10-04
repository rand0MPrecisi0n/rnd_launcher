#!/usr/bin/python3
""" 
Twitch launcher for livestreamer
Includes database functions, quality selector and web-parsing 
"""

#a = tlfunc_classes.Db("a")
#print(a.dict)

import functions as functions
import sys, shelve

#User selection
shelf = shelve.open("default.shlf", writeback=True)
try:
    shelf["default"]
    user = shelf["default"]
except KeyError:
    user = input("Type the desired username: ")

#OAuth
try:
    shelf["oauth"]
    oauth = shelf["oauth"]
except KeyError:
    oauth = input("Please paste your OAUTH token:")
    shelf["oauth"] = oauth
shelf.close()

#Create instance
instance = functions.Db(user, oauth)

#options dispatch
options = {"h":instance.help, "help":instance.help, "list":instance.display_db, "clear":instance.clear_db, "chat":instance.chat_settings, "quit":sys.exit, "default":instance.default, "oauth":instance.oauth_token}
qualities = {"1":"source", "2":"high", "3":"medium", "4":"low", "5":"mobile"}

def launch_stream():
    instance.add_db(stream)
    instance.save_db()
    instance.launcher(stream, quality)

#Intro
print("{0:*^60}\n{1:*^60}\n{2:*^60}\n".format(" Hello "+user.upper()+" ", " Welcome to Twitch Launcher ", " At any point, use option \"h\" for help "))

#Control Flow

while True:
    #print(streamlist)
    stream = input("Type the stream of choice or 'h' for help: ").lower().strip()
    if stream in options.keys():
        options[stream]()
    else:
        while True: 
            quality = input("{0:*<60}\n{1}\n{2}\n{3}\n{4}\n{5}\n: ".format("Type the quality of choice or equivalent number ", "1 : source", "2 : high", "3 : medium", "4 : low", "5 : mobile")).lower().strip()
            if quality in options.keys():
                options[quality]()
            elif quality == "back":
                break
            elif quality in qualities.keys():
                quality = qualities[quality]
                launch_stream()
                break
            elif quality in qualities.values():
                launch_stream()
                break
            else:
                print("This is not a valid quality")
