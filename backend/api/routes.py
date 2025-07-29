from fastapi import APIRouter, Request
from pydantic import BaseModel
from agents.planner_agent import get_itinerary
from agents.packing_agent import get_packing_list

router = APIRouter()

class TripRequest(BaseModel):
    destination: str
    start_date: str
    end_date: str
    interests: str

@router.post("/itinerary")
async def itinerary(request: TripRequest):
    return {"itinerary": get_itinerary(request)}

@router.post("/packing")
async def packing(request: TripRequest):
    return {"packing_list": get_packing_list(request)}
