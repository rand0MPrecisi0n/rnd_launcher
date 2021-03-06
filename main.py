#!/usr/bin/python3
""" 
Twitch launcher for livestreamer
Includes database functions, quality selector and web-parsing 
"""

#a = tlfunc_classes.Db("a")
#print(a.dict)

import functions as functions
import sys, shelve, subprocess, webbrowser
from time import sleep

#User selection
shelf = shelve.open("default.shlf", writeback=True)
try:
    shelf["default"]
    user = shelf["default"]
except KeyError:
    user = input("Type the desired username: ")
    default = input("Would you like to make this the default user? y/n: ")
    if default == "y":
        shelf["default"] = user
        print("Default user changed to "+user)

#OAuth
try:
    shelf["oauth_rnd"]
    oauth_rnd = shelf["oauth_rnd"]
    shelf["oauth_ls"]
    oauth_ls = shelf["oauth_ls"]
except KeyError:
    subprocess.Popen("livestreamer --twitch-oauth-authenticate", shell=True)
    webbrowser.open(r"https://api.twitch.tv/kraken/oauth2/authorize?response_type=token&client_id=57escm9wy6fayv570mj99rx0147mn4q&redirect_uri=http://localhost&scope=user_read+user_follows_edit+user_subscriptions+chat_login")

    token_rnd = input("\n{0}\n\n".format("PLEASE PASTE TOKEN FOR RND_LAUNCHER (first page, after access_token=, before &scope=)"))
    token_ls = input("\n{0}\n\n".format("PLEASE PASTE TOKEN FOR LIVESTREAMER (second page, after access_token=, before &scope=)"))
    shelf["oauth_rnd"] = token_rnd
    shelf["oauth_ls"] = token_ls
    oauth_rnd = shelf["oauth_rnd"]; oauth_ls = shelf["oauth_ls"]
shelf.close()

#Create instance
instance = functions.Db(user, oauth_rnd, oauth_ls)

#options dispatch
options = {"h":instance.help, "help":instance.help, "list":instance.display_db, "clear":instance.clear_db, "chat":instance.chat_settings, "quit":sys.exit, "default":instance.default, "show oauth":instance.show_oauth, "live":instance.live, "browser":instance.browser_settings, "fl":instance.follow, "unf":instance.unfollow}
qualities = {"1":"source", "2":"high", "3":"medium", "4":"low", "5":"mobile"}

def launch_stream():
    instance.add_db(stream)
    instance.save_db()
    instance.launcher(stream, quality)

#Intro
print("{0:*^60}\n{1:*^60}\n{2:*^60}\n".format(" Hello "+user.upper()+" ", " Welcome to rnD Launcher ", " At any point, use option \"h\" for help "))

#Control Flow

while True:
    #print(streamlist)
    stream = input("Type the stream of choice or 'h' for help: ").lower().strip()
    var = stream.split()
    if len(var) == 1 and var[0] in options.keys():
        options[var[0]]()
    elif len(var) > 1 and var[0] in options.keys():
        options[var[0]](str(var[1:])[1:-1].replace("'",""))
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
