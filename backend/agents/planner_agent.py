from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config.settings import GROQ_API_KEY

def get_itinerary(request):
    llm = ChatGroq(
        model="mixtral-8x7b-32768",  # or "llama3-70b-8192"
        api_key=GROQ_API_KEY
    )

    prompt_template = PromptTemplate(
        input_variables=["destination", "start_date", "end_date", "interests"],
        template=(
            "You are a professional travel planner. Create a detailed day-by-day itinerary for a person traveling to {destination} "
            "from {start_date} to {end_date}. Their interests include: {interests}. Include places to visit, local foods to try, and time of day."
        )
    )

    chain = LLMChain(llm=llm, prompt=prompt_template)

    response = chain.run({
        "destination": request.destination,
        "start_date": request.start_date,
        "end_date": request.end_date,
        "interests": request.interests
    })

    return response