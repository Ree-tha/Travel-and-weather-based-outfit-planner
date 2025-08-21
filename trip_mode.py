
# utils/trip_mode.py

from utils.weather import get_weather_by_location
from utils.suggestion import suggest_outfit

def plan_trip_outfits(locations, days, occasion):
    locations_list = [loc.strip() for loc in locations.split(",") if loc.strip()]
    outfit_plan = []

    if not locations_list:
        return [], "No valid locations provided."

    for day in range(days):
        # Rotate through locations if fewer than days
        location = locations_list[day % len(locations_list)]
        weather, error = get_weather_by_location(location)

        if error:
            outfit_plan.append({
                "day": day + 1,
                "location": location,
                "error": error
            })
        else:
            suggestions = suggest_outfit(weather, occasion)
            outfit_plan.append({
                "day": day + 1,
                "location": location,
                "weather": weather,
                "suggestions": suggestions
            })

    return outfit_plan, None
