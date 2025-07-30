from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config.settings import GROQ_API_KEY

def get_packing_list(request):
    llm = ChatGroq(
        model="meta-llama/llama-4-maverick-17b-128e-instruct",  # or "llama3-70b-8192"
        api_key=GROQ_API_KEY
    )

    prompt_template = PromptTemplate(
        input_variables=["destination", "start_date", "end_date", "interests"],
        template=(
            "You are an expert travel assistant. Create a detailed packing list for a person traveling to {destination} from "
            "{start_date} to {end_date}. Their interests include {interests}. Include weather-appropriate clothes, accessories, tech, documents, etc."
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