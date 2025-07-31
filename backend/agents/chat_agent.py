from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, Tool
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from config.settings import GROQ_API_KEY

# Core LLM
llm = ChatGroq(
    model="meta-llama/llama-4-maverick-17b-128e-instruct",
    api_key=GROQ_API_KEY,
    temperature=0.7
)

# Tool 1: Travel Planning
def get_itinerary(place: str) -> str:
    prompt = PromptTemplate(
        input_variables=["place"],
        template="Generate a 7-day travel itinerary for visiting {place} with varied activities."
    )
    chain: RunnableSequence = prompt | llm
    return chain.invoke({"place": place})

# Tool 2: Smart Packing
def get_packing_list(destination: str) -> str:
    prompt = PromptTemplate(
        input_variables=["destination"],
        template="Generate a smart packing list for a trip to {destination}, considering climate and activities."
    )
    chain: RunnableSequence = prompt | llm
    return chain.invoke({"destination": destination})

# Define tools
tools = [
    Tool(
        name="TravelPlanner",
        func=get_itinerary,
        description="Use this tool when the user asks for a travel itinerary or trip plan."
    ),
    Tool(
        name="PackingAssistant",
        func=get_packing_list,
        description="Use this tool when the user asks what to pack OR when they're planning a trip and might need packing advice for the destination."
    ),
]

# Create agent
agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

# Main function for chat message
def get_chat_response(message: str) -> str:
    return agent_executor.run(message)
