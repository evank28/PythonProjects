#CITATION: The following block of code comes from Google Sheet's API's Quickstart.py, with some modifications to suit our needs
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

#The following code is written by the AP Submitting Students
from difflib import SequenceMatcher #function for similarity
from datetime import date, datetime, timedelta, time

def findDay(full):	#Written by: WZ 
    list=full.split("/")
    return (int(list[1]))

def findMonth(full): #Written by: WZ
    list=full.split("/")
    MonthNumber=int(list[0])
    Months=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    return Months[MonthNumber-1]

def nxtMonth(full): #Written by: both EK & WZ
    list=full.split("/")
    MonthNumber=int(list[0])
    Months=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    return Months[MonthNumber]    

def newRowFinder(file): #Written by: EK
    """This function returns the row to read to see if it exists. Give the path to the filename as parameter 'file'. """
    in_file = open(file)
    line = int(in_file.readline())
    return line+1

def saveLastRow(file, lastRow): #Written by:EK
    in_file = open(file, "w")
    in_file.write(str(lastRow))


def isSimilar(a, b): #Written by: EK
    similarity= SequenceMatcher(None, a, b).ratio() # This funcion (SequenceMatcher) Came from the built in difflib library. https://d.python.org/2/library/difflib.html#sequencematcher-objects
    if similarity >=0.55:
        return True
    else:
        return False

def getTime(inTime): #Written by: Both WZ & EK
    """Takes a Google Sheets formatted time and returns a datetime.time formatted time"""
    list = inTime.split(":")
    list[2] = list[2][3:]
    hours=int(list[0])
    minutes=int(list[1])
    if str(list[2]) =='PM': 
        hours+=12
    return time(hours, minutes)

def formatTime(inTime): #Written by: EK
    """inTime must be a datetime.time() object"""
    t=str(time.strftime(inTime, "%I:%M %p"))
    if t[0]=="0":
        return str(time.strftime(inTime, "%I:%M %p"))[1:]
    return str(time.strftime(inTime, "%I:%M %p"))


def timeSubtraction(inTime, minutesToSubtract): #Written by: EK
    """takes a time in datetime.time() format and an integer for the number of minutes to subtract from the time"""
    dt = datetime.combine(date.today(), inTime)
    return (dt - timedelta(minutes=minutesToSubtract)).time()


def callTime(HouseOpen, EventType): #Written by: WZ
    """return(CallTime,seniorCrew,juniorCrew)"""
    CallTime = 0
    juniorCrew = 0
    seniorCrew = 0
    if EventType == "Lecture":
        CallTime = timeSubtraction(getTime(HouseOpen), 30)
        juniorCrew = 3
        seniorCrew = 1
    if EventType == "Panel Discussion":
        CallTime = timeSubtraction(getTime(HouseOpen), 90)
        juniorCrew = 3
        seniorCrew = 2
    if EventType == "Dance or Drama Performance":
        CallTime =  timeSubtraction(getTime(HouseOpen), 120)
        juniorCrew = 3
        seniorCrew = 3
    if EventType == "Musical Concert":
        CallTime = timeSubtraction(getTime(HouseOpen), 120)
        juniorCrew = "All Crew"
        seniorCrew = "All Crew"
    if EventType == "Ceremony":
        CallTime = timeSubtraction(getTime(HouseOpen), 90)
        juniorCrew = 3
        seniorCrew = 3
    if EventType == "Competition or Conference":
        CallTime = timeSubtraction(getTime(HouseOpen), 120)
        juniorCrew = 3
        seniorCrew = 1
    return [CallTime, seniorCrew, juniorCrew]

def main(values): #Written by: EK, Debugged by both WZ and EK
    lastIndex=len(values)-1
    #2. Loop through the necessary rows and write the relevant data to a dictionary - newEvents
    newEvents={}
    for event in values[newRowFinder('lastrow.txt'):len(values)]:#Only updates rows that have not been updated previously. See newRowFinder() . 
        newEvents.setdefault(event[2], {'dateOfEvent': event[3],
                                        'eventCoordinator': event[4],
                                        'staffSupervisor': event[5],
                                                'eventType': event[6],
                                                'eventStart': event[7],
                                                'houseOpen':event[10],
                                                'curtains':event[13],
                                        'podium':event[14],
                                        'additionalFurniture': event[15],
                                        'audienceQs':event[16],
                                        'AvMedia':event[22],
                                        'Lighting':event[24]
                                        }
                             )
    #3. Write values to correct location in other file                          
    #First, read the Event List File
    rangeName = 'Event List'
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    #Create a dictionary called 'months' with all the indexes of where months begin
    months={'July':len(values)}
    for rows in values[1:]:
        if rows[0] !='':
            months.setdefault(rows[0])
            months[rows[0]]=values.index(rows)

    #Begin the copy
    for event in newEvents:
        #Find where to insert
        eventMonth=findMonth(newEvents[event]['dateOfEvent'])
        nextMonth=nxtMonth(newEvents[event]['dateOfEvent'])

        for rows in values[months[eventMonth]:months[nextMonth]]:
            #print(rows[1], "compared with", findDay(newEvents[event]['dateOfEvent']))
            if int(rows[1])==findDay(newEvents[event]['dateOfEvent']): #Checks to see if an event on the day of the event exists - if yes, it knows the event row to insert
                rowToInsert=values.index(rows)+1
                indextoInsert=values.index(rows)
                break
            elif int(rows[1])>findDay(newEvents[event]['dateOfEvent']): #Checks to see if an event after the day of the event exists, setting the index to insert as 1 row above
                rowToInsert=values.index(rows)
                indextoInsert=values.index(rows)-1
                break
            else:
                rowToInsert=months[nextMonth]
                indextoInsert=months[nextMonth]-1                

        if not isSimilar(values[indextoInsert][2],event): #Checks to see if an event with the same name exists on that date
            #If yes, be prepared to overwrite it
            #Othwerwise, create a new row below the existing row, to add this new event
            rowToInsert+=1
            indextoInsert+=1
            #InsertNewRow using InsertDimensionRequest
            requests=[]
            requests.append({"insertRange": { "range":{
                "sheetId": 1034566956,
                "startRowIndex": rowToInsert-1,
                            "endRowIndex": rowToInsert,
                                                            "startColumnIndex": 0,
                                                            "endColumnIndex": 12, },
                                              "shiftDimension": "ROWS",
                                              }})	
            body = {"requests": requests}
            response = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId,body=body).execute()	


        """Perform the copy using the spreadsheet.values collection's BatchUpdate request"""
        ct=callTime(newEvents[event]['houseOpen'], newEvents[event]['eventType'])	
        batch_update_values_request_body = {
            # How the input data should be interpreted.
            'value_input_option': 'USER_ENTERED', 

                    # The new values to apply to the spreadsheet.
                            'data': [
                                {"range": str(rangeName)+'!B'+str(rowToInsert), "majorDimension": "ROWS", "values": [[findDay(newEvents[event]['dateOfEvent'])]]},
                                {"range": str(rangeName)+'!C'+str(rowToInsert),"values": [[event]]},
                                {"range": str(rangeName)+'!D'+str(rowToInsert),"values": [["Event Coordinator: " + str(newEvents[event]['eventCoordinator']) +"\n" +"Staff Supervisor: " + str(newEvents[event]['staffSupervisor'])]]},
                                    {"range": str(rangeName)+'!E'+str(rowToInsert),"values": [[ct[1]]]},
                                    {"range": str(rangeName)+'!G'+str(rowToInsert),"values": [[ct[2]]]},
                                    {"range": str(rangeName)+'!J'+str(rowToInsert),"values": [[formatTime(ct[0])]]},
                                    {"range": str(rangeName)+'!K'+str(rowToInsert),"values": [["Type: "+str(newEvents[event]['eventType'])
                                                                                               +"\n Event Starts: "+ str(newEvents[event]['eventStart'])
                                                                                               +"\n House Opens: "+str(newEvents[event]['houseOpen'])
                                                                                               +"\n Curtains: "+str(newEvents[event]['curtains'])
                                                                                +"\n Podium: "+str(newEvents[event]['podium'])
                                                                                +"\n Audience Questions: "+str(newEvents[event]['audienceQs'])
                                                                                +"\n Lights On: "+str(newEvents[event]['Lighting'])
                                                                                +"\n Additional AV Media: "+str(newEvents[event]['AvMedia'])
                                                                                +"\n Additional Furniture: "+str(newEvents[event]['additionalFurniture'])
                                                                                ]]}
                                    ],  

        }

        request = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body=batch_update_values_request_body)
        response = request.execute()	
        print('Updated Row ' +str(rowToInsert) +' for '+event)

#Mission Accomplished
        print ('All Updates Complete!!')
        
        saveLastRow('lastrow.txt', lastIndex) #Saves the last row to the file
import easygui as eg
import webbrowser
default='Exit'
def checkStatus(values): #Written by: EK
    global default
    if len(values) > newRowFinder("lastrow.txt"):
        default='Exit'
        return "New Events have been requested. \n\n                           Please update the Event List."
    else:
        default='Update Spreadsheet Now'
        return "The Event List is up to date." 

#1. Read all rows in the spreadsheet and set it to a list within a list, called 'values'    
if __name__ == '__main__': #Written by: EK
        credentials = get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)
        
        spreadsheetId = '1z2QzPf9Kc02roOwTJUYab4k2dwYu1n-nIbJ5yzWF3YE'
        rangeName = 'Event Requests'
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheetId, range=rangeName).execute()
        values = result.get('values', [])
else:  
    choice=eg.msgbox(msg='Credentials are incorrect - cannot run. Please Run the program again, after installing credentials.', title='Incorrect Credentials - Try Again.', ok_button='Exit', image=None, root=None)
    if choice == 1:
                exit()
#Written by: WZ
choice = eg.ynbox(msg="Spreadsheet Status:   "+ checkStatus(values), title='Event List Updater', choices=['Update Spreadsheet Now', 'Exit'], default_choice=default, cancel_choice='Cancel')
if (choice == 1):
    if __name__ == '__main__':
        main(values)
    option = eg.ynbox("The Event List was updated succesfully. Do you wish to view it?", "Event List Updater - Update Complete", ("View Updated Event List", "Exit"))
    if option == 1:
        webbrowser.open("https://docs.google.com/spreadsheets/d/1z2QzPf9Kc02roOwTJUYab4k2dwYu1n-nIbJ5yzWF3YE/edit?ts=58ecf7bf#gid=1034566956", new=0, autoraise=True)
        exit()
    else:
        exit()
    
else: exit()