from fastapi import FastAPI, HTTPException, BackgroundTasks
import requests
import sqlite3
from pydantic import BaseModel
app = FastAPI()

SERPAPI_KEY = "f59ac241e5c46866961f558a5ed7a3213f4973293fe5f28de9a72cd86b718173"
API_URL = "https://serpapi.com/search.json"

# Database setup
def init_db():
    conn = sqlite3.connect("recommendations.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS recommendations (
                        id INTEGER PRIMARY KEY,
                        user_id TEXT,
                        title TEXT,
                        url TEXT,
                        description TEXT,
                        tags TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Fetch data from SerpAPI
def fetch_serpapi_results(query):
    params = {"q": query, "api_key": SERPAPI_KEY}
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    return {}

# Store recommendations in the database
def store_recommendations(user_id, results):
    conn = sqlite3.connect("recommendations.db")
    cursor = conn.cursor()
    for result in results.get("organic_results", []):
        cursor.execute("INSERT INTO recommendations (user_id, title, url, description, tags) VALUES (?, ?, ?, ?, ?)",
                       (user_id, result.get("title", "Unknown"), result.get("link", ""), result.get("snippet", ""), ""))
    conn.commit()
    conn.close()

@app.post("/update_recommendations/{user_id}")
def update_recommendations(user_id: str, background_tasks: BackgroundTasks):
    interests = ["AI/ML courses", "Web development projects", "Data Science internships"]  # Fetch from user profile
    for interest in interests:
        results = fetch_serpapi_results(interest)
        store_recommendations(user_id, results)
    return {"message": "Recommendations are being updated."}

@app.get("/recommendations/{user_id}")
def get_recommendations(user_id: str):
    conn = sqlite3.connect("recommendations.db")
    cursor = conn.cursor()
    cursor.execute("SELECT title, url, description, tags FROM recommendations WHERE user_id = ?", (user_id,))
    data = cursor.fetchall()
    conn.close()
    return [{"title": row[0], "url": row[1], "description": row[2], "tags": row[3].split(",")} for row in data]

@app.get("/user/{user_id}")
def get_user(user_id: str):
    # Mock user data for display
    user_data = {
        "name": "Sarah Johnson",
        "major": "Computer Science Major",
        "interests": ["AI/ML", "Web Development", "Data Science", "UX Design"],
        "skills": {"JavaScript": "Advanced", "Python": "Intermediate", "React": "Advanced", "Machine Learning": "Beginner"},
        "performance": {"GPA": "4.0", "honors": "Dean's List - Fall 2023", "strengths": "Strong in Mathematics"}
    }
    return user_data

@app.put("/user/{user_id}/interests")
def update_interests(user_id: str, interests: dict):
    return {"message": "User interests updated successfully.", "interests": interests}

class SearchRequest(BaseModel):
    interests: list[str]

@app.post("/get_courses")
def get_courses(request: SearchRequest):
    courses = []
    for interest in request.interests:
        params = {
            "q": f"{interest} online courses",
            "api_key": SERPAPI_KEY,
            "engine": "google"
        }
        response = requests.get(API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            for result in data.get("organic_results", []):
                courses.append({
                    "title": result.get("title"),
                    "link": result.get("link"),
                    "snippet": result.get("snippet")
                })
        else:
            raise HTTPException(status_code=500, detail="Error fetching data from SERP API")
    return {"courses": courses}
