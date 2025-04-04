import requests
import json
from datetime import datetime

API_URL = "http://localhost:8000"

def create_test_notes():
    """Create a set of test notes with different categories."""
    test_notes = [
        {
            "title": "Investment Portfolio Update",
            "content": "Stock market showing positive trends. Need to rebalance portfolio with 60% stocks, 30% bonds, and 10% cash. Consider adding more tech stocks."
        },
        {
            "title": "Weekly Workout Plan",
            "content": "Monday: Cardio and strength training. Tuesday: Yoga and flexibility. Wednesday: Rest day. Thursday: HIIT workout. Friday: Swimming. Weekend: Light walking."
        },
        {
            "title": "Project Timeline",
            "content": "Q1: Complete MVP development. Q2: User testing and feedback. Q3: Feature enhancements. Q4: Production deployment. Need to schedule weekly team meetings."
        },
        {
            "title": "Vacation Planning",
            "content": "Planning trip to Bali. Need to book flights, hotel, and activities. Research local attractions and restaurants. Check visa requirements."
        },
        {
            "title": "System Architecture Design",
            "content": "Designing microservices architecture. Need to implement API gateway, service discovery, and load balancing. Consider using Kubernetes for orchestration."
        },
        {
            "title": "Family Reunion",
            "content": "Organizing annual family reunion. Need to coordinate with relatives, book venue, and plan activities. Create shopping list for supplies."
        },
        {
            "title": "Machine Learning Course",
            "content": "Enrolled in advanced ML course. Topics include neural networks, deep learning, and reinforcement learning. Need to complete weekly assignments."
        },
        {
            "title": "Garden Maintenance",
            "content": "Spring cleaning needed in the garden. Tasks: trim hedges, plant new flowers, fertilize lawn, and clean garden tools."
        }
    ]

    print("Creating test notes...")
    for note in test_notes:
        response = requests.post(f"{API_URL}/notes", json=note)
        if response.status_code == 200:
            print(f"Created note: {note['title']}")
        else:
            print(f"Failed to create note: {note['title']}")
            print(f"Error: {response.text}")

def test_search_functionality():
    """Test different search scenarios."""
    search_tests = [
        {"keyword": "investment", "category": "Finance"},
        {"keyword": "workout", "category": "Health"},
        {"keyword": "project", "category": "Work"},
        {"keyword": "vacation", "category": "Travel"},
        {"keyword": "system", "category": "Technology"},
        {"keyword": "family", "category": "Personal"},
        {"keyword": "learning", "category": "Education"}
    ]

    print("\nTesting search functionality...")
    for test in search_tests:
        print(f"\nSearching for: {test['keyword']} in category: {test['category']}")
        response = requests.get(
            f"{API_URL}/search",
            params=test
        )
        if response.status_code == 200:
            results = response.json()
            print(f"Found {results['total']} results")
            for note in results['results']:
                print(f"- {note['title']} (Category: {note['category']})")
        else:
            print(f"Search failed: {response.text}")

def test_health_check():
    """Test the health check endpoint."""
    print("\nTesting health check...")
    response = requests.get(f"{API_URL}/health")
    if response.status_code == 200:
        health_status = response.json()
        print("Health Check Results:")
        print(json.dumps(health_status, indent=2))
    else:
        print(f"Health check failed: {response.text}")

def main():
    print("Starting API tests...")
    
    # Wait for API to be ready
    print("Waiting for API to be ready...")
    import time
    time.sleep(5)
    
    # Run tests
    create_test_notes()
    test_search_functionality()
    test_health_check()
    
    print("\nTest completed!")

if __name__ == "__main__":
    main() 