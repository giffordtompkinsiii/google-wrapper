from __future__ import print_function
# import pandas as pd
import datetime as dt
import pickle
import os
import calendar
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class GoogleClient(object):
    """
    Class for configuring Google API access. For a complete list of scopes and 
    services go to https://developers.google.com/identity/protocols/oauth2/scopes#gmailv1.
    """

    SERVICES=[
        ('calendar','v3'),
        ('tasks','v1')
                ]

    SCOPES = ['https://www.googleapis.com/auth/' + service for service, version in SERVICES]

    def __init__(self, client_name):
        """
        Creates a token.pickle from the credential file.
        The file token.pickle stores the user's access and refresh tokens, and is
        created automatically when the authorization flow completes for the first
        time.
        """
        self.client_name = client_name
        creds = None
        client_path = f"{os.path.curdir}/clients/{client_name.replace(' ','_').lower()}"
        creds_path = os.path.join(client_path, 'credentials.json')
        token_path = os.path.join(client_path, 'token.pickle')

        if not os.path.exists(client_path):
            os.mkdir(client_path)

        if os.path.exists(token_path):
            if os.path.getsize(token_path) > 0:
                creds = pickle.load(open(token_path, 'rb'))

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(creds_path, self.SCOPES)
                    creds = flow.run_local_server(port=0)
                except FileNotFoundError as e:
                    print(f'Follow the following link to acquire credential files: https://developers.google.com/docs/api/quickstart/python')
            # Save the credentials for the next run
                with open(token_path, 'wb') as token:
                    pickle.dump(creds, token)
        self.creds = creds

    def build_calendar(self):
        self.calendar_service = CalendarService(service=build('calendar', 'v3', credentials=self.creds))

class CalendarService(object):
    def __init__(self, service):
        self.service = service
        self.calendars = []
        for cal in self.service.calendarList().list().execute()['items']:
            self.calendars.append(Calendar(self.service, cal))


class Calendar(CalendarService):
    def __init__(self, service, calendar):
        self.service = service
        for k, v in calendar.items():
            self.__setattr__(k, v)

    def __repr__(self):
        d = {'summary': self.summary, 'id': self.id}
        return str(d).replace(',',',\n\t')+'\n'

    # def get_events(self):
        

# class Event(Calendar):
#     def __init__(self, event_dict):
#         for k, v in calendar.items():
#             self.__setattr__(k, v)


user = GoogleClient('Gifford Tompkins')
user.build_calendar()
cals = user.calendar_service.calendars
cal = cals[0]
