from typing import TypedDict,List,Optional,Dict
import google.generativeai as genai
from backend.config import config
from controller.prompt import Prompt
from controller.utils import extract_json
from controller.calender import book_appointment,analyze_slots_status
#########################
#     CONFIGURATIONS    #
#########################

genai.configure(api_key=config.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash",)

#########################
#      AGENT STATE      #
#########################

class AgentState(TypedDict):
    chat_history:Optional[List[str]]
    final_response:Optional[str]
    intent:Optional[str]
    appointment_info:Optional[Dict]
    slot_available:Optional[bool]

#########################
#         STATE         #
#########################
class state:
    def gemini_reasoner(state : AgentState) -> AgentState:
        response = model.generate_content(Prompt.GeminiResponserPrompt(state['chat_history']))
        JsonResponse = extract_json(response.text)
        # print("Raw response:", response.text)
        # print("Extracted JSON:", JsonResponse)
        if "Intent"  in JsonResponse:
            # print("Intent detected")
            state['intent'] = JsonResponse['Intent']
            state['appointment_info'] = JsonResponse
        else:
            print("No intent detected, setting final response")
            state['final_response'] = response.text
        return state
    
    def check_availability(state : AgentState) -> AgentState:
        print("CHECKING APPOINTMENT")
        slots_data = analyze_slots_status(state['appointment_info']['event'])
        response = model.generate_content(Prompt.CheckAvailabilityPrompt(slots_data,state['chat_history']))
        JsonResponse = extract_json(response.text)
        # print("JsonResponse:",JsonResponse)
        if JsonResponse['occupied']:
            state['intent'] = 'Check'
            state['final_response'] = JsonResponse['response']
        else:
            state['final_response'] = JsonResponse['response']
        return state
    
    def book_appointment(state : AgentState) -> AgentState:
        print("BOOK APPOINTMENT")
        event_link = book_appointment(state['appointment_info']['event'])
        state['final_response'] = f"Appointment booked! Here is your event link: {event_link}"
        return state






