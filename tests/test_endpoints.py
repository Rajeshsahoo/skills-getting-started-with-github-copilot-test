"""Tests for API endpoints using AAA (Arrange-Act-Assert) pattern"""

import pytest


class TestRootEndpoint:
    """Tests for the root endpoint"""

    def test_root_redirects_to_static_index(self, client):
        """Test that root endpoint redirects to /static/index.html"""
        # Arrange
        expected_redirect_url = "/static/index.html"

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == expected_redirect_url


class TestGetActivities:
    """Tests for the get activities endpoint"""

    def test_get_activities_returns_all_activities(self, client):
        """Test that GET /activities returns all activities"""
        # Arrange
        expected_activity_count = 9

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200
        assert len(activities) == expected_activity_count
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Basketball Team" in activities

    def test_get_activities_returns_correct_structure(self, client):
        """Test that activity objects have required fields"""
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str)
            assert set(activity_data.keys()) == required_fields
            assert isinstance(activity_data["participants"], list)


class TestSignupForActivity:
    """Tests for the signup endpoint"""

    def test_signup_new_student_succeeds(self, client):
        """Test successful signup for an activity"""
        # Arrange
        activity_name = "Basketball Team"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "Signed up" in data["message"]
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_duplicate_student_fails(self, client):
        """Test signup fails when student is already signed up"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]

    def test_signup_nonexistent_activity_fails(self, client):
        """Test signup fails when activity does not exist"""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]


class TestRemoveSignup:
    """Tests for the remove signup endpoint"""

    def test_remove_existing_signup_succeeds(self, client):
        """Test successful removal of student from activity"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "Removed" in data["message"]
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_remove_nonexistent_signup_fails(self, client):
        """Test removal fails when student is not signed up for activity"""
        # Arrange
        activity_name = "Chess Club"
        email = "notstudent@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "not signed up" in data["detail"]

    def test_remove_from_nonexistent_activity_fails(self, client):
        """Test removal fails when activity does not exist"""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]