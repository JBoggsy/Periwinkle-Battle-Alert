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

#IMPORTS:#
import praw
import string
from pprint import pprint
from time import sleep
config = open('prime_cnfg.txt')
config = config.read()
config = config.split(',')
userID = config[0]
userPass = config[1]
enemy_sub = config[2]
rec_thread = config[3]
generals = config[3:]
log = open("RecruitmentRunLog.txt","w")
log.write("Finished Imports\n")
from requests.exceptions import HTTPError
#END IMPORTS#


#REDDIT LOGIN
r = praw.Reddit('Chroma Recruitment Bot')
tries = 0
while tries<11:
    try:
        r.login(userID,userPass)
        log.write("Logged In\n")
        break
    except:
        log.write("Log in error, trying again\n")
        tries += 1

def getUsers():
    signupThread = r.get_submission(submission_id=rec_thread)
    log.write(str(signupThread)+"\n")
    signupThread.replace_more_comments()
    log.write('Replaced more comments'+"\n")
    signUps = signupThread.comments
    log.write(str(signUps)+"\n")
    troopList = []
    for signUp in signUps:
        if detect_ORed(signUp.author):
            print("Orangered "+str(signUp.author)+" ignored!")
            log.write("Orangered "+str(signUp.author)+" ignored!")
            continue
        recruit = signUp.author.__str__()
        log.write(str(signUp)+"\n")
        try:
            if not (recruit in troopList):
                troopList.append(recruit)
                log.write("Added user "+recruit+"to troopList.\n")
                log.flush()
        except:
            log.write("ERROR:"+"\n")
            log.write(str(recruit)+"\n")
            pass
    log.write("Retrieved Majors"+"\n")
    log.write(str(troopList)+"\n")
    print troopList
    return troopList

def checkForGo(troopList):
    while True:
        PMs = r.get_unread(True, True)
        if PMs != None:
            log.write("New messages!"+"\n")
            for PM in PMs:
                PM.mark_as_read()
                sLine = PM.subject.strip().upper()
                if (sLine == "SEND MESSAGE") and (PM.author.__str__() in generals):
                    sent_to = ''
                    for troops in troopList:
                        try:
                            r.send_message(troops,"Battle Reminder",PM.body)
                            log.write("Message: "+PM.body+" sent to "+troops+"\n")
                        except:
                            log.write("Error with " + troops+"\n")
                    PM.reply("Message sent to "+str(troops)+"!")
        else:
            log.write("No new messages!"+"\n")
        log.flush()
        sleep(60)

def detect_ORed(user):
    subReddit = r.get_subreddit(enemy_sub)
    mods = subReddit.get_moderators()
    for mod in mods:
        try:
            if mod == user:
                return True
        except HTTPError:
            print ("User no longer exists?")
            log.write("HTTPError again, with user "+str(user)+"\n")
            continue
    return False

troopList = getUsers()
checkForGo(troopList)