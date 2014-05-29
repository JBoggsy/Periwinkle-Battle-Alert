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
print "Finished Imports"
#END IMPORTS#

#REDDIT LOGIN
r = praw.Reddit('Periwinkle Prime Recruitment')
tries = 0
while tries<11:
    try:
        r.login('Periwinkle_Prime','periwinklerules')
        print "Logged In"
        break
    except:
        print "Log in error, trying again"


def getUsers():
    signupThread = r.get_submission(submission_id='206qef')
    print signupThread
    signupThread.replace_more_comments()
    print 'Replaced more comments'
    signUps = signupThread.comments
    pprint(signUps)
    troopList = []
    for signUp in signUps:
        recruit = signUp.author.__str__()
        print recruit
        try:
            if not (recruit in troopList):
                troopList.append(recruit)
        except:
            print"ERROR:"
            print recruit
            pass
    print "Retrieved Majors"
    return troopList

def checkForGo(troopList):
    while True:
        PMs = r.get_unread(True, True)
        if PMs != None:
            print "New messages!"
            for PM in PMs:
                sLine = PM.subject.strip().upper()
                if sLine == "SEND MESSAGE":
                    for troops in troopList:
                        try:
                            r.send_message(troops,"Battle Reminder",PM.body)
                        except:
                            print ("Error with " + troops)
                            continue
                    break
        else:
            print "No new messages!"
        sleep(60)

troopList = getUsers()
checkForGo(troopList)