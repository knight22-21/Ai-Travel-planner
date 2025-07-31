from langchain_groq import ChatGroq
from langchain.agents import initialize_agent, Tool
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from config.settings import GROQ_API_KEY

# 🔧 Core LLM
llm = ChatGroq(
    model="deepseek-r1-distill-llama-70b",
    api_key=GROQ_API_KEY,
    temperature=0.7
)

# 🌍 Tool 1: Travel Itinerary
def get_itinerary(place: str) -> str:
    prompt = PromptTemplate(
        input_variables=["place"],
        template="Generate a 7-day travel itinerary for visiting {place} with varied activities."
    )
    chain: RunnableSequence = prompt | llm
    return chain.invoke({"place": place})

# 🎒 Tool 2: Smart Packing
def get_packing_list(destination: str) -> str:
    prompt = PromptTemplate(
        input_variables=["destination"],
        template="Generate a smart packing list for a trip to {destination}, considering climate and activities."
    )
    chain: RunnableSequence = prompt | llm
    return chain.invoke({"destination": destination})

# 🍜 Tool 3: Local Foods
def get_local_foods(destination: str) -> str:
    prompt = PromptTemplate(
        input_variables=["destination"],
        template="List the top 5 must-try local dishes and street foods in {destination}."
    )
    chain: RunnableSequence = prompt | llm
    return chain.invoke({"destination": destination})

# 🎉 Tool 4: Local Events
def get_local_events(destination: str) -> str:
    prompt = PromptTemplate(
        input_variables=["destination"],
        template="List famous festivals or events in {destination} happening throughout the year."
    )
    chain: RunnableSequence = prompt | llm
    return chain.invoke({"destination": destination})

# 🧰 Define tools
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
    Tool(
        name="LocalFoodAdvisor",
        func=get_local_foods,
        description="Use this tool when the user wants to know about local dishes or street food to try in a destination."
    ),
    Tool(
        name="LocalEventsFinder",
        func=get_local_events,
        description="Use this tool when the user wants to know about cultural festivals or major events in a place."
    ),
]

# 🧠 Agent with tools
agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

# 💬 Main function for chat
def get_chat_response(message: str) -> str:
    return agent_executor.run(message)
