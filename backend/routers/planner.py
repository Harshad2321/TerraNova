from fastapi import APIRouter, HTTPException
from backend.schemas.city import DetailedCityRequest, DetailedCityResponse
from backend.services.planner import generate_city_layout

router = APIRouter()

@router.post("/plan", response_model=DetailedCityResponse)
async def plan_city(request: DetailedCityRequest):
    """
    Plan a city based on detailed parameters
    
    Args:
        request: DetailedCityRequest containing city parameters
        
    Returns:
        DetailedCityResponse with recommendations and analysis
    
    Raises:
        HTTPException: If request parameters are invalid
    """
    # Input validation
    if request.population <= 0:
        raise HTTPException(status_code=400, detail="Population must be positive")
    
    if request.area <= 0:
        raise HTTPException(status_code=400, detail="Area must be positive")
    
    # Validate soil_type
    valid_soil_types = ["sandy", "clay", "rocky", "loamy"]
    if request.soil_type.lower() not in valid_soil_types:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid soil type. Must be one of: {', '.join(valid_soil_types)}"
        )
    
    # Validate surroundings
    valid_surroundings = ["coastal", "hilly", "plain", "forest"]
    if request.surroundings.lower() not in valid_surroundings:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid surroundings. Must be one of: {', '.join(valid_surroundings)}"
        )
        
    # Generate the city plan
    return generate_city_layout(request)
# End of file
