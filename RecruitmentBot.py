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
#END IMPORTS#

#REDDIT LOGIN
r = praw.Reddit('Periwinkle Prime Recruitment')
r.login('Periwinkle_Prime','periwinklerules')

def getUsers():
    signupThread = r.get_submission(submission_id='206qef')
    signupThread.replace_more_comments()
    signUps = signupThread.comments
    troopList = []
    for signUp in signUps:
        recruit = signUp.author.__str__()
        try:
            if not (recruit in troopList):
                troopList.append(recruit)
        except:
            print"ERROR:"
            print recruit
            pass
    return troopList

def checkForGo(troopList):
    while True:
        PMs = r.get_unread(True)
        if PMs != None:
            for PM in PMs:
                if PM.subject == "SEND MESSAGE":
                    for troops in troopList:
                        try:
                            r.send_message(troops,"Battle Reminder",PM.body)
                        except:
                            print ("Error with " + troops)
                            continue

checkForGo(getUsers)