#!venv./bin/python
# Google Calendar API needs to be activated


from datetime import datetime, timedelta
import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dotenv import load_dotenv

load_dotenv() 

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

CREDENTIALS_FILE = '../google-creds/creds-google-calendar-python.json' # get creds file from google project
CALENDAR_ID = os.getenv('GOOGLE_CALENDAR_ID') # Use the method list_calendars() to list all avaible calendars 
EVENT_FILE = 'events.txt'
EVENT_LIST = []

def get_calendar_service():
   creds = None
   # The file token.pickle stores the user's access and refresh tokens, and is
   # created automatically when the authorization flow completes for the first
   # time.
   if os.path.exists('token.pickle'):
       with open('token.pickle', 'rb') as token:
           creds = pickle.load(token)
   # If there are no (valid) credentials available, let the user log in.
   if not creds or not creds.valid:
       if creds and creds.expired and creds.refresh_token:
           creds.refresh(Request())
       else:
           flow = InstalledAppFlow.from_client_secrets_file(
               CREDENTIALS_FILE, SCOPES)
           creds = flow.run_local_server(port=0)

       # Save the credentials for the next run
       with open('token.pickle', 'wb') as token:
           pickle.dump(creds, token)

   service = build('calendar', 'v3', credentials=creds)
   return service

# Use the method to list all available calendars 
def list_calendars():
   service = get_calendar_service()
   # Call the Calendar API
   print('Getting list of calendars')
   calendars_result = service.calendarList().list().execute()

   calendars = calendars_result.get('items', [])

   if not calendars:
       print('No calendars found.')
   for calendar in calendars:
       summary = calendar['summary']
       id = calendar['id']
       primary = "Primary" if calendar.get('primary') else ""
       print("%s\t%s\t%s" % (summary, id, primary))


def insert_event(event):
   # creates 15 minute event one day before
   service = get_calendar_service()

   day_before = datetime(event.year, event.month, event.day, 17) - timedelta(days=1)
   start = day_before.isoformat()
   end = (day_before + timedelta(minutes=15)).isoformat()

   event_result = service.events().insert(calendarId=CALENDAR_ID,
       body={
           "summary": 'Taking out trashcan',
           "start": {"dateTime": start, "timeZone": 'Europe/Berlin'},
           "end": {"dateTime": end, "timeZone": 'Europe/Berlin'},
           'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 10},
                ],
            },
           "colorId": 5, #https://lukeboyle.com/blog/posts/google-calendar-api-color-id
       }
   ).execute()

   print("created event")
   print("id: ", event_result['id'])
   print("starts at: ", event_result['start']['dateTime'])
   print("ends at: ", event_result['end']['dateTime'])

def read_events():
    print("Reading events from file: ", EVENT_FILE)
    file = open(EVENT_FILE, 'r')
    Lines = file.readlines()
    
    for line in Lines:
        line_dt = datetime.strptime(line.strip(), '%d.%m.%Y').date()
        EVENT_LIST.append(line_dt)


if __name__ == '__main__':
   # list_calendars()
   read_events()
   for event in EVENT_LIST:
       insert_event(event)