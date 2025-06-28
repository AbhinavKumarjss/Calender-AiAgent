from __future__ import print_function
import datetime
import os.path
import pickle
import json

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from config import config

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_creds():
    """
    Get Google Calendar credentials using environment variables.
    Returns:
        Credentials: Google OAuth2 credentials
    """
    creds = None
    
    # Check if we have a stored token
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    return creds

def book_appointment(event_json):
    """
    Books an appointment on Google Calendar using an event JSON/dict.
    Args:
        event_json (dict): Dictionary with event details. Should contain keys like 'summary', 'location', 'description', 'start_datetime', 'end_datetime', 'timezone', 'attendees', 'reminders'.
    Returns:
        str: Link to the created event.
    """
    print(event_json)
    summary = event_json.get('summary', '')
    location = event_json.get('location', '')
    description = event_json.get('description', '')
    start_datetime = event_json.get('start')['dateTime']
    end_datetime = event_json.get('end')['dateTime']
    timezone = event_json.get('timeZone', 'UTC')
    attendees = event_json.get('attendees', [])
    reminders = event_json.get('reminders', None)



    service = build('calendar', 'v3', credentials=get_creds())

    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_datetime,
            'timeZone': timezone,
        },
        'end': {
            'dateTime': end_datetime,
            'timeZone': timezone,
        },
        'attendees': attendees,
        'reminders': reminders if reminders else {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))
    return event.get('htmlLink')

def analyze_slots_status(event_json):
    """
    Analyzes the status of every slot within a given time range.
    Args:
        event_json (dict): Dictionary with start and end times.
                          Should contain keys like 'start', 'end', 'timeZone'.
        slot_duration_minutes (int): Duration of each slot in minutes (default: 60)
    Returns:
        dict: Dictionary with analysis results including slot statuses and summary.
    """
    slot_duration_minutes=30;
    start_date = event_json.get('start')['dateTime']
    end_date = event_json.get('end')['dateTime']
    timezone = event_json.get('timeZone', 'UTC')
    slot_duration_minutes = event_json.get('duration')

    service = build('calendar', 'v3', credentials=get_creds())
    
    # Get all events in the date range
    events_result = service.events().list(
        calendarId='primary',
        timeMin=start_date,
        timeMax=end_date,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    print(f"Found {len(events)} events in the time range")
    
    # Convert dates to datetime objects with proper timezone handling
    def parse_datetime(dt_string):
        if dt_string.endswith('Z'):
            dt_string = dt_string[:-1] + '+00:00'
        return datetime.datetime.fromisoformat(dt_string)
    
    start_dt = parse_datetime(start_date)
    end_dt = parse_datetime(end_date)
    
    print(f"Analyzing slots from {start_dt} to {end_dt}")
    
    # Generate all slots and analyze their status
    slots_analysis = []
    current_dt = start_dt
    slot_number = 1
    
    while current_dt < end_dt:
        slot_end = current_dt + datetime.timedelta(minutes=slot_duration_minutes)
        
        # Don't exceed the requested end time
        if slot_end > end_dt:
            slot_end = end_dt
        
        # Check if this slot conflicts with any existing events
        slot_status = 'available'
        conflicting_events = []
        
        for event in events:
            event_start = event['start'].get('dateTime', event['start'].get('date'))
            event_end = event['end'].get('dateTime', event['end'].get('date'))
            
            # Handle all-day events
            if 'date' in event['start']:
                # All-day event - skip for now as we're dealing with time slots
                continue
            
            # Convert to datetime objects
            event_start_dt = parse_datetime(event_start)
            event_end_dt = parse_datetime(event_end)
            
            # Check for overlap - more precise overlap detection
            overlap_start = max(current_dt, event_start_dt)
            overlap_end = min(slot_end, event_end_dt)
            
            if overlap_start < overlap_end:
                slot_status = 'occupied'
                conflicting_events.append({
                    'summary': event.get('summary', 'No title'),
                    'start': event_start,
                    'end': event_end,
                    'description': event.get('description', ''),
                    'overlap_start': overlap_start.isoformat(),
                    'overlap_end': overlap_end.isoformat()
                })
                print(f"Slot {slot_number} conflicts with: {event.get('summary', 'No title')}")
        
        # Calculate actual duration for this slot
        actual_duration = int((slot_end - current_dt).total_seconds() / 60)
        
        slots_analysis.append({
            'slot_number': slot_number,
            'start': current_dt.isoformat(),
            'end': slot_end.isoformat(),
            'duration_minutes': actual_duration,
            'status': slot_status,
            'conflicting_events': conflicting_events
        })
        
        slot_number += 1
        current_dt = slot_end
    
    # Calculate summary statistics
    total_slots = len(slots_analysis)
    available_slots = len([slot for slot in slots_analysis if slot['status'] == 'available'])
    occupied_slots = len([slot for slot in slots_analysis if slot['status'] == 'occupied'])
    
    # Calculate total available and occupied time
    total_available_minutes = sum(slot['duration_minutes'] for slot in slots_analysis if slot['status'] == 'available')
    total_occupied_minutes = sum(slot['duration_minutes'] for slot in slots_analysis if slot['status'] == 'occupied')
    
    print(f"Analysis complete: {total_slots} total slots, {available_slots} available, {occupied_slots} occupied")
    
    return {
        'time_range': {
            'start': start_date,
            'end': end_date,
            'timezone': timezone
        },
        'slot_duration_minutes': slot_duration_minutes,
        'summary': {
            'total_slots': total_slots,
            'available_slots': available_slots,
            'occupied_slots': occupied_slots,
            'total_available_minutes': total_available_minutes,
            'total_occupied_minutes': total_occupied_minutes,
            'availability_percentage': round((available_slots / total_slots * 100), 2) if total_slots > 0 else 0
        },
        'slots': slots_analysis,
        'debug_info': {
            'events_found': len(events),
            'event_details': [{'summary': e.get('summary', 'No title'), 'start': e['start'], 'end': e['end']} for e in events]
        }
    }