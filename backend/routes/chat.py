from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from fastapi.responses import JSONResponse
from ..controller.controller import agent

AGENT_MEMORY = 10

class ChatRequest(BaseModel):
    message:List[str]


router  = APIRouter(tags=["Chat Assistant"])

@router.post('/chat')
def Chat(req:ChatRequest):
    messages = req.message;
    if(len(req.message) > AGENT_MEMORY):
        messages = req.message[-AGENT_MEMORY:]
    response = agent.invoke({"chat_history":messages})
    return JSONResponse(content={"response": response['final_response']})



