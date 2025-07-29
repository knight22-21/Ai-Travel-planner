def get_packing_list(request):
    # TODO: Connect to LangChain + Groq
    return f"Packing list for {request.destination} based on weather and interests in {request.interests}"
