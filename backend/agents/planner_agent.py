def get_itinerary(request):
    # TODO: Connect to LangChain + Groq
    return f"Mock itinerary for {request.destination} from {request.start_date} to {request.end_date} focusing on {request.interests}"
