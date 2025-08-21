# utils/suggestion.py

from utils.wardrobe import get_uploaded_clothes

def suggest_outfit(weather, occasion):
    temperature = weather.get("temperature", 25)
    condition = weather.get("condition", "Clear")
    wardrobe = get_uploaded_clothes()
    
    suggestions = []

    # Basic logic based on temperature and occasion
    for item in wardrobe:
        name = item.lower()

        if "jacket" in name or "hoodie" in name or "sweater" in name:
            if temperature < 20:
                suggestions.append(item)
        elif "rain" in name or "umbrella" in name:
            if "rain" in condition.lower():
                suggestions.append(item)
        elif "formal" in name or "shirt" in name:
            if occasion.lower() == "formal":
                suggestions.append(item)
        elif "party" in name or "dress" in name:
            if occasion.lower() == "party":
                suggestions.append(item)
        elif "casual" in name or "tshirt" in name:
            if occasion.lower() == "casual":
                suggestions.append(item)
        else:
            # Default: lightweight for warm days
            if temperature > 22 and ("jean" in name or "top" in name or "kurti" in name):
                suggestions.append(item)

    # Fallback: If no items matched, show the first 3
    if not suggestions:
        suggestions = wardrobe[:3]

    return suggestions
