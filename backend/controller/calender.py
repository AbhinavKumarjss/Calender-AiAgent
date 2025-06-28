from __future__ import print_function
import datetime
import os.path
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

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

    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

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

def check_slots(event_json):
    """
    Checks for available time slots in Google Calendar.
    Args:
        event_json (dict): Dictionary with event details. Should contain keys like 'start_datetime', 'end_datetime', 'timezone'.
    Returns:
        dict: Dictionary with availability information including conflicts and available slots.
    """
    start_datetime = event_json.get('start')['dateTime']
    end_datetime = event_json.get('end')['dateTime']
    timezone = event_json.get('timeZone', 'UTC')
    
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    
    # Convert datetime strings to datetime objects for comparison
    start_dt = datetime.datetime.fromisoformat(start_datetime.replace('Z', '+00:00'))
    end_dt = datetime.datetime.fromisoformat(end_datetime.replace('Z', '+00:00'))
    
    # Get events that overlap with the requested time slot
    events_result = service.events().list(
        calendarId='primary',
        timeMin=start_datetime,
        timeMax=end_datetime,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    
    # Check for conflicts
    conflicts = []
    for event in events:
        event_start = event['start'].get('dateTime', event['start'].get('date'))
        event_end = event['end'].get('dateTime', event['end'].get('date'))
        
        # Convert to datetime objects for comparison
        event_start_dt = datetime.datetime.fromisoformat(event_start.replace('Z', '+00:00'))
        event_end_dt = datetime.datetime.fromisoformat(event_end.replace('Z', '+00:00'))
        
        # Check if there's an overlap
        if (start_dt < event_end_dt and end_dt > event_start_dt):
            conflicts.append({
                'summary': event.get('summary', 'No title'),
                'start': event_start,
                'end': event_end,
                'description': event.get('description', '')
            })
    
    # Determine availability
    is_available = len(conflicts) == 0
    
    return {
        'is_available': is_available,
        'requested_start': start_datetime,
        'requested_end': end_datetime,
        'conflicts': conflicts,
        'conflict_count': len(conflicts)
    }

def find_available_slots(event_json, slot_duration_minutes=60, business_hours=None):
    """
    Finds available time slots within a given date range.
    Args:
        start_date (str): Start date in ISO format (e.g., '2024-01-15T00:00:00Z')
        end_date (str): End date in ISO format (e.g., '2024-01-16T00:00:00Z')
        slot_duration_minutes (int): Duration of each slot in minutes (default: 60)
        business_hours (dict): Business hours configuration. If None, uses 9 AM to 5 PM.
                              Format: {'start': '09:00', 'end': '17:00', 'timezone': 'UTC'}
    Returns:
        list: List of available time slots as dictionaries with start and end times.
    """
    start_date = event_json.get('start')['dateTime']
    end_date = event_json.get('end')['dateTime']
    timezone = event_json.get('timeZone', 'UTC')

    if business_hours is None:
        business_hours = {'start': '09:00', 'end': '17:00', 'timezone': 'UTC'}
    
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    
    # Get all events in the date range
    events_result = service.events().list(
        calendarId='primary',
        timeMin=start_date,
        timeMax=end_date,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    
    # Convert dates to datetime objects
    start_dt = datetime.datetime.fromisoformat(start_date.replace('Z', '+00:00'))
    end_dt = datetime.datetime.fromisoformat(end_date.replace('Z', '+00:00'))
    
    # Generate all possible slots
    available_slots = []
    current_dt = start_dt
    
    while current_dt < end_dt:
        # Check if current time is within business hours
        current_time = current_dt.strftime('%H:%M')
        if business_hours['start'] <= current_time <= business_hours['end']:
            slot_end = current_dt + datetime.timedelta(minutes=slot_duration_minutes)
            
            # Check if this slot conflicts with any existing events
            slot_available = True
            for event in events:
                event_start = event['start'].get('dateTime', event['start'].get('date'))
                event_end = event['end'].get('dateTime', event['end'].get('date'))
                
                # Convert to datetime objects
                event_start_dt = datetime.datetime.fromisoformat(event_start.replace('Z', '+00:00'))
                event_end_dt = datetime.datetime.fromisoformat(event_end.replace('Z', '+00:00'))
                
                # Check for overlap
                if (current_dt < event_end_dt and slot_end > event_start_dt):
                    slot_available = False
                    break
            
            if slot_available:
                available_slots.append({
                    'start': current_dt.isoformat(),
                    'end': slot_end.isoformat(),
                    'duration_minutes': slot_duration_minutes
                })
        
        # Move to next slot
        current_dt += datetime.timedelta(minutes=slot_duration_minutes)
    
    return available_slots

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

    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    
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