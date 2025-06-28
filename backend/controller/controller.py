from langgraph.graph import StateGraph,START,END
from controller.states import AgentState, state
graph = StateGraph(AgentState)

graph.add_node("GeminiResponder" ,state.gemini_reasoner)
graph.add_node("BookAppointment" , state.book_appointment)
graph.add_node("CheckAvailability",state.check_availability)

graph.add_edge(START, "GeminiResponder")
graph.add_edge("BookAppointment", END)

graph.add_conditional_edges(
    "CheckAvailability",
    lambda state: (print(f"CheckAvailability edge - intent: {state.get('intent')}"), state.get('intent'))[1],
    {
        'Book': "BookAppointment",
        'Check': END
    }
)
graph.add_conditional_edges(
    "GeminiResponder",
    lambda state: (print(f"GeminiResponder edge - intent: {state.get('intent')}"), state.get('intent'))[1],
    {
        'Book': "CheckAvailability",
        'Check': "CheckAvailability",
        None: END
    }
)
agent = graph.compile()
