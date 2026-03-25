"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.  
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Team basketball practice, drills, and friendly matches",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Swimming Team": {
        "description": "Swim training for endurance, technique, and competition",
        "schedule": "Tuesdays and Fridays, 6:30 AM - 7:30 AM",
        "max_participants": 18,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Drama Club": {
        "description": "Acting workshops and stage performance preparation",
        "schedule": "Thursdays, 3:30 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["isabella@mergington.edu", "charlotte@mergington.edu"]
    },
    "Painting Studio": {
        "description": "Explore watercolor, acrylic, and mixed media techniques",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["amelia@mergington.edu", "evelyn@mergington.edu"]
    },
    "Math Olympiad": {
        "description": "Advanced problem-solving and competition math training",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["elijah@mergington.edu", "james@mergington.edu"]
    },
    "Debate Society": {
        "description": "Develop argumentation, rhetoric, and public speaking skills",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["lucas@mergington.edu", "harper@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Field training, teamwork drills, and interschool matches",
        "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["henry@mergington.edu", "jack@mergington.edu"]
    },
    "Volleyball Club": {
        "description": "Volleyball fundamentals, rotations, and team scrimmages",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["zoe@mergington.edu", "nora@mergington.edu"]
    },
    "Photography Club": {
        "description": "Learn composition, lighting, and photo storytelling",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["lily@mergington.edu", "grace@mergington.edu"]
    },
    "School Band": {
        "description": "Practice ensemble performance with modern and classical pieces",
        "schedule": "Thursdays, 3:30 PM - 5:30 PM",
        "max_participants": 24,
        "participants": ["leo@mergington.edu", "scarlett@mergington.edu"]
    },
    "Robotics Club": {
        "description": "Design, build, and program robots for team challenges",
        "schedule": "Fridays, 3:30 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["aiden@mergington.edu", "chloe@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Hands-on science events and competition preparation",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["ethan@mergington.edu", "aria@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    normalized_email = email.strip().lower()

    # Validate student is not already signed up
    existing_participants = {participant.lower() for participant in activity["participants"]}
    if normalized_email in existing_participants:
        raise HTTPException(status_code=409, detail="Student is already signed up for this activity")

    # Add student
    activity["participants"].append(normalized_email)
    return {"message": f"Signed up {normalized_email} for {activity_name}"}
