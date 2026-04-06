"""Pytest configuration and shared fixtures"""

import pytest
import copy
from fastapi.testclient import TestClient
from src.app import app

# Initial activities data for resetting between tests
INITIAL_ACTIVITIES = {
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
    "Basketball Team": {
        "description": "Practice and compete in basketball games",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 15,
        "participants": []
    },
    "Soccer Club": {
        "description": "Train and play soccer matches",
        "schedule": "Wednesdays and Saturdays, 3:00 PM - 5:00 PM",
        "max_participants": 22,
        "participants": []
    },
    "Art Club": {
        "description": "Explore painting, drawing, and other visual arts",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": []
    },
    "Music Club": {
        "description": "Learn to play instruments and sing in a choir",
        "schedule": "Tuesdays, 3:00 PM - 4:30 PM",
        "max_participants": 25,
        "participants": []
    },
    "Debate Club": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": []
    },
    "Science Club": {
        "description": "Conduct experiments and learn about scientific concepts",
        "schedule": "Fridays, 2:00 PM - 3:30 PM",
        "max_participants": 20,
        "participants": []
    }
}

@pytest.fixture
def client():
    """Test client with reset activities data"""
    from src.app import activities
    
    # Reset activities to initial state
    activities.clear()
    activities.update(copy.deepcopy(INITIAL_ACTIVITIES))
    
    return TestClient(app)