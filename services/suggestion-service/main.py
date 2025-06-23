from fastapi import FastAPI, Query
from pydantic import BaseModel
import random
from typing import List, Optional

app = FastAPI(title="Suggestion Service")

# --- Pydantic Models ---
class Suggestion(BaseModel):
    id: int
    title: str
    recommendation_reason: str

# --- Simulated Data & Logic ---
# In a real scenario, this would come from a database, an ML model, or an external API.
simulated_content_items = [
    {"id": 1, "title": "Learn Python Programming", "category": "education"},
    {"id": 2, "title": "Introduction to FastAPI", "category": "technology"},
    {"id": 3, "title": "Healthy Cooking Recipes", "category": "lifestyle"},
    {"id": 4, "title": "Understanding Microservices", "category": "technology"},
    {"id": 5, "title": "Travel Guide: Paris", "category": "travel"},
    {"id": 6, "title": "Advanced JavaScript Techniques", "category": "technology"},
    {"id": 7, "title": "Home Workout Routines", "category": "health"},
    {"id": 8, "title": "The Art of Digital Painting", "category": "art"},
]

def get_simulated_suggestions(category: Optional[str] = None, limit: int = 3) -> List[Suggestion]:

    source_items = simulated_content_items
    if category:
        source_items = [item for item in simulated_content_items if item.get("category") == category]
        if not source_items: # Fallback if category yields no results
            source_items = simulated_content_items

    # Ensure we don't try to sample more items than available
    num_to_sample = min(limit, len(source_items))
    if num_to_sample == 0:
        return []

    suggested_items = random.sample(source_items, num_to_sample)

    suggestions = []
    for i, item in enumerate(suggested_items):
        reasons = [
            "Based on popular trends.",
            "You might also like this.",
            "Recommended for you.",
            "Others also viewed this.",
            f"A top pick in '{item.get('category', 'general')}'."
        ]
        suggestions.append(
            Suggestion(
                id=item["id"], # Using item's original ID
                title=item["title"],
                recommendation_reason=random.choice(reasons)
            )
        )
    return suggestions

# --- API Endpoints ---
@app.get("/suggestions/", response_model=List[Suggestion])
async def get_recommendations(
    category: Optional[str] = Query(None, description="Optional category to filter suggestions"),
    limit: int = Query(3, ge=1, le=10, description="Number of suggestions to return")
):
    """
    Provides a list of content suggestions.
    This is a simulated endpoint. In a real system, it would use an AI/ML model.
    """
    suggestions = get_simulated_suggestions(category=category, limit=limit)
    return suggestions

@app.get("/")
def read_root():
    return {"message": "Suggestion Service is running. Try /suggestions/ endpoint."}

# To run this service (for development):
# uvicorn services.suggestion-service.main:app --reload --port 8003
# No .env needed for this simple version unless you add external API keys (e.g., OpenAI).
