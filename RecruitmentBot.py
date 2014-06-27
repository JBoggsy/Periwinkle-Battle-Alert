#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      James Boggs
#
# Created:     11/03/2014
# Copyright:   (c) James Boggs 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#IMPORTS:#
import praw
import string
from pprint import pprint
from time import sleep
log = open("RecruitmentRunLog.txt","w")
log.write("Finished Imports\n")
#END IMPORTS#

#REDDIT LOGIN
r = praw.Reddit('Periwinkle Prime Recruitment')
tries = 0
while tries<11:
    try:
        r.login('Periwinkle_Prime','periwinklerules')
        log.write("Logged In\n")
        break
    except:
        log.write("Log in error, trying again\n")


def getUsers():
    signupThread = r.get_submission(submission_id='206qef')
    log.write(str(signupThread)+"\n")
    signupThread.replace_more_comments()
    log.write('Replaced more comments'+"\n")
    signUps = signupThread.comments
    log.write(str(signUps)+"\n")
    troopList = []
    for signUp in signUps:
        if detect_ORed(signUp.author):
            print("Orangered "+str(signUp.author)+" ignored!")
            continue
        recruit = signUp.author.__str__()
        log.write(str(signUp)+"\n")
        try:
            if not (recruit in troopList):
                troopList.append(recruit)
        except:
            log.write("ERROR:"+"\n")
            log.write(str(recruit)+"\n")
            pass
    log.write("Retrieved Majors"+"\n")
    log.write(str(troopList)+"\n")
    return troopList

def checkForGo(troopList):
    while True:
        PMs = r.get_unread(True, True)
        if PMs != None:
            log.write("New messages!"+"\n")
            for PM in PMs:
                PM.mark_as_read()
                sLine = PM.subject.strip().upper()
                if (sLine == "SEND MESSAGE") and (PM.author.__str__() in ['RockdaleRooster','Tiercel','Sahdee']):
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
    for subName in ['orangered','Oraistedearg','Aegis_Imperial','AreusAntris','GreatAurantiaco','NovumPersarum','MetropolisDaja','OrangeLondo','Pasto_Range','Tentorahogo']:
        subReddit = r.get_subreddit(subName)
        mods = subReddit.get_moderators()
        for mod in mods:
            if mod == user:
                return True
        return False

#troopList = getUsers()
checkForGo(['Eliminioa'])