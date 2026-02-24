print("THIS IS THE API FILE BEING EXECUTED")
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Zodiac Persona API", version="1.0.0")

# 🔥 Put CORS immediately after app creation
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=False,  # 👈 VERY IMPORTANT
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/cors-test")
def cors_test():
    return {"message": "cors middleware active"}
# THEN import other heavy modules
from fastapi import HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from zodiac_persona.main import calculate_birth_chart
class BirthData(BaseModel):
    name: str = "User"
    dob: str  # ISO format string e.g., 2000-01-01T12:00:00
    latitude: float
    longitude: float
    timezone_offset: float = 0.0

@app.post("/api/astrology/calculate")
def calculate_astrology(data: BirthData):
    try:
        birth_date = datetime.fromisoformat(data.dob)
        
        # Call the existing calculation module
        chart = calculate_birth_chart(
            birth_date=birth_date,
            latitude=data.latitude,
            longitude=data.longitude,
            timezone_offset=data.timezone_offset,
            name=data.name
        )
        
        # Extract meaningful data for "Zodiac Persona: Your nature, your sign"
        # Let's get ascendant and its details from the d1_chart (House 1)
        ascendant_house = chart.d1_chart.houses[0]
        ascendant_sign = ascendant_house.sign
        
        # Sun sign (which planet in d1_chart is Sun)
        sun_planet = next((p for p in chart.d1_chart.planets if p.celestial_body == "Sun"), None)
        moon_planet = next((p for p in chart.d1_chart.planets if p.celestial_body == "Moon"), None)
        
        # Provide basic personality mapping based on signs
        personality_traits = {
            "Aries": "Courageous, energetic, and pioneering.",
            "Taurus": "Patient, reliable, and deeply grounded.",
            "Gemini": "Adaptable, outgoing, and highly communicative.",
            "Cancer": "Nurturing, sensitive, and fiercely protective.",
            "Leo": "Charismatic, confident, and natural leaders.",
            "Virgo": "Detail-oriented, practical, and analytical.",
            "Libra": "Diplomatic, fair-minded, and social.",
            "Scorpio": "Passionate, resourceful, and intuitive.",
            "Sagittarius": "Optimistic, freedom-loving, and adventurous.",
            "Capricorn": "Disciplined, responsible, and tenacious.",
            "Aquarius": "Innovative, independent, and humanitarian.",
            "Pisces": "Compassionate, artistic, and deeply empathetic."
        }
        sun_sign_name = sun_planet.sign if sun_planet else "Unknown"
        moon_sign_name = moon_planet.sign if moon_planet else "Unknown"
        
        return {
            "status": "success",
            "data": {
                "name": data.name,
                "ascendant": ascendant_sign,
                "sun_sign": sun_sign_name,
                "moon_sign": moon_sign_name,
                "personality": personality_traits.get(sun_sign_name, "Unique and mysterious individual."),
                "full_chart": chart.to_dict()  # Raw detailed chart for future expansion
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}
