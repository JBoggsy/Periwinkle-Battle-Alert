#-------------------------------------------------------------------------------
# Name:        Alert Module
# Purpose:      Allows Prime to send out pre-battle alert messages
#
# Author:      James Boggs
#
# Created:     11/03/2014
# Copyright:   (c) James Boggs 2014
# Licence:     GNU shit
#-------------------------------------------------------------------------------

# IMPORTS:
import praw
import string
from pprint import pprint
from time import sleep
import webbrowser
import json
# END IMPORTS

# CONFIG INFO
with open('config.cfg') as f:
    config = f.read()
    config = config.split(',')
    client_ID = config[0]
    client_secret = config[1]
    redirect_uri = config[2]
    enemy_sub = config[3]
    rec_threads = config[4].strip("(").strip(")").split("|")
    generals = config[4:]
# GET BlACKLIST INFO
with open('blacklist.cfg','r') as bl_file:
    raw_list = bl_file.read()
    blacklist = raw_list.split(',')
    for item in blacklist:
        item.strip()
# GET USER DATABASE
with open('userlist.cfg','r') as ul_file:
    user_list = json.load(ul_file)
log = open("RecruitmentRunLog.txt","w")
log.write("Finished Imports\n")
from requests.exceptions import HTTPError


#REDDIT LOGIN
r = praw.Reddit('Chroma Assistance Suite')
#r.set_oauth_app_info(client_id=client_ID, client_secret=client_secret, redirect_uri='http://127.0.0.1:65010/code')
#url = r.get_authorize_url('identity','privatemessages',True)
#webbrowser.open(url)
#code = raw_input()
#print code
#access_info = r.get_access_information(code)
#r.set_access_credentials(**access_information)

tries = 0
while tries<11:
    try:
        r.login("Periwinkle_Prime_3","CodeOmega")
        log.write("Logged In\n")
        break
    except:
        log.write("Log in error, trying again\n")
        tries += 1

def getUsersFromList(thread_id, troopList=[]):
    """
    Underlying method of getting users from a sign up thread.
    """
    signupThread = r.get_submission(submission_id=thread_id,comment_limit=None,comment_sort='random')
    log.write(str(signupThread)+"\n")
    signupThread.replace_more_comments()
    log.write('Replaced more comments'+"\n")
    signUps = signupThread.comments
    log.write(str(signUps)+"\n")
    for signUp in signUps:
       # if detect_ORed(signUp.author):
       #     print("Orangered "+str(signUp.author)+" ignored!")
       #     log.write("Orangered "+str(signUp.author)+" ignored!")
       #     continue
        recruit = signUp.author.__str__()
        try:
            log.write(str(signUp)+"\n")
            if (not (recruit in troopList)) and (not (recruit in blacklist)):
                troopList.append(recruit)
                print(recruit)
                log.write("Added user "+recruit+"to troopList.\n")
                log.flush()
                replied = already_replied(signUp)
                print(replied)
                if not replied:
                    signUp.reply("ADDED TO DATABASE")
                    print("replied!")
        except:
            log.write("ERROR:"+"\n")
            log.write(str(recruit)+"\n")
            pass
    log.write("Retrieved Majors"+"\n")
    log.write(str(troopList)+"\n")
    #print troopList
    return troopList

def checkForGo(troopList):
    """
    Check PMs for a SEND MESSAGE command and then execute once found.
    """
    while True:
        PMs = r.get_unread(True, True)
        if PMs != None:
            log.write("New messages!"+"\n")
            print("New messages!")
            for PM in PMs:
                PM.mark_as_read()
                sLine = PM.subject.strip().upper()
                print(sLine)
                print(str(generals)+"|"+str(PM.author.__str__()))
                print(PM.author.__str__() in generals)
                if (sLine == "SEND MESSAGE") and (PM.author.__str__() in generals):
                    print("Beginning to send message!")
                    sent_to = ''
                    for troops in troopList:
                        try:
                            r.send_message(troops,"Battle Reminder",PM.body)
                            log.write("Message: "+PM.body+" sent to "+troops+"\n")
                            print("Message sent to "+troops)
                        except:
                            log.write("Error with " + troops+"\n")
                            print("Error with "+troops)
                    PM.reply("Message sent to "+str(troops)+"!")
        else:
            log.write("No new messages!"+"\n")
        log.flush()
        sleep(60)

# def detect_ORed(user):
#     subReddit = r.get_subreddit(enemy_sub)
#     mods = subReddit.get_moderators()
#     for mod in mods:
#         try:
#             if mod == user:
#                 return True
#         except HTTPError:
#             print ("User no longer exists?")
#             log.write("HTTPError again, with user "+str(user)+"\n")
#             continue
#     return False

def get_troops_most(thread_id):
    """
    Ensure we get as many unique people as possible from threads with 
    more comments than PRAW can retrieve.
    """
    trooplist = getUsersFromList(thread_id,[])
    hold_list = []
    while trooplist != hold_list:
        hold_list = trooplist
        trooplist = getUsersFromList(thread_id,trooplist)
    return trooplist

def get_all_troops(trooplist=[]):
    """
    Method to get troops from every sign-up thread on the list.
    """
    for thread in rec_threads:
        print(thread)
        new_troops = get_troops_most(thread)
        temp_list = set(trooplist).union(set(new_troops))
        trooplist=list(temp_list)
    return trooplist

def already_replied(PM):
    print("CHECKING FOR REPLY")
    replies = PM.replies
    for reply in replies:
        if str(reply.author) == "Periwinkle_Prime_3":
            return True
    return False

trooplist = get_all_troops(user_list)
print("Done getting troops: " + str(len(trooplist)))
with open('userlist.cfg','w') as ul_list:
    json.dump(trooplist,ul_list)
checkForGo(trooplist)
