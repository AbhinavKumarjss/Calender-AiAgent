
class Tools:

    Find_available_slots = {
        "name": "find_available_slots",
        "description": """
    Finds available time slots within a given date range.
    Args:
        start_date (str): Start date in ISO format (e.g., '2024-01-15T00:00:00Z')
        end_date (str): End date in ISO format (e.g., '2024-01-16T00:00:00Z')
        slot_duration_minutes (int): Duration of each slot in minutes (default: 60)
        business_hours (dict): Business hours configuration. If None, uses 9 AM to 5 PM.
                              Format: {'start': '09:00', 'end': '17:00', 'timezone': 'UTC'}
    Returns:
        list: List of available time slots as dictionaries with start and end times.
    """,
        "parameters": {
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "Start date in ISO format (e.g., '2024-01-15T00:00:00Z')"
                },
                "end_date": {
                    "type": "string", 
                    "description": "End date in ISO format (e.g., '2024-01-16T00:00:00Z')"
                },
                "slot_duration_minutes": {
                    "type": "integer",
                    "description": "Duration of each slot in minutes",
                    "default": 60
                },
                "business_hours": {
                    "type": "object",
                    "description": "Business hours configuration. If None, uses 9 AM to 5 PM UTC",
                    "properties": {
                        "start": {
                            "type": "string",
                            "description": "Start time in HH:MM format (e.g., '09:00')"
                        },
                        "end": {
                            "type": "string", 
                            "description": "End time in HH:MM format (e.g., '17:00')"
                        },
                        "timezone": {
                            "type": "string",
                            "description": "Timezone (e.g., 'UTC', 'America/New_York')"
                        }
                    },
                    "required": ["start", "end", "timezone"]
                }
            },
            "required": ["start_date", "end_date"]
        }
    }

