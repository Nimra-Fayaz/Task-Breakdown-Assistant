"""Unit tests for ratings API endpoints."""

from unittest.mock import patch

import pytest

from task_breakdown.api.ratings import MAX_RATING, MIN_RATING


class TestCreateRating:
    """Tests for POST /api/ratings endpoint."""

    @patch("task_breakdown.api.tasks.generate_task_breakdown")
    def test_create_rating_success(
        self, mock_generate, client, setup_database, sample_breakdown_data
    ):
        """Test successful rating creation."""
        mock_generate.return_value = sample_breakdown_data

        # First create a task
        task_response = client.post(
            "/api/tasks",
            json={"description": "Test task description that is long enough"},
        )
        task_id = task_response.json()["id"]

        # Create rating
        response = client.post(
            "/api/ratings/",
            json={"task_id": task_id, "rating": 5, "comment": "Great guide!"},
        )

        assert response.status_code == 201
        assert response.json()["rating"] == 5
        assert response.json()["task_id"] == task_id
        assert response.json()["comment"] == "Great guide!"

    @patch("task_breakdown.api.tasks.generate_task_breakdown")
    def test_create_rating_without_comment(
        self, mock_generate, client, setup_database, sample_breakdown_data
    ):
        """Test rating creation without comment."""
        mock_generate.return_value = sample_breakdown_data

        # Create a task
        task_response = client.post(
            "/api/tasks",
            json={"description": "Test task description that is long enough"},
        )
        task_id = task_response.json()["id"]

        # Create rating without comment
        response = client.post("/api/ratings/", json={"task_id": task_id, "rating": 4})

        assert response.status_code == 201
        assert response.json()["rating"] == 4

    @patch("task_breakdown.api.tasks.generate_task_breakdown")
    def test_create_rating_invalid_value_too_high(
        self, mock_generate, client, setup_database, sample_breakdown_data
    ):
        """Test rating creation with rating value too high."""
        mock_generate.return_value = sample_breakdown_data

        # Create a task
        task_response = client.post(
            "/api/tasks",
            json={"description": "Test task description that is long enough"},
        )
        task_id = task_response.json()["id"]

        # Create rating with invalid value
        # Pydantic validates at schema level, so returns 422 (validation error)
        response = client.post(
            "/api/ratings/",
            json={
                "task_id": task_id,
                "rating": MAX_RATING + 1,  # Invalid: should be 1-5
                "comment": "Test",
            },
        )

        assert response.status_code == 422  # Pydantic validation error
        # Check that validation error mentions rating constraint
        error_detail = str(response.json())
        assert "rating" in error_detail.lower() or "greater than" in error_detail.lower()

    @patch("task_breakdown.api.tasks.generate_task_breakdown")
    def test_create_rating_invalid_value_too_low(
        self, mock_generate, client, setup_database, sample_breakdown_data
    ):
        """Test rating creation with rating value too low."""
        mock_generate.return_value = sample_breakdown_data

        # Create a task
        task_response = client.post(
            "/api/tasks",
            json={"description": "Test task description that is long enough"},
        )
        task_id = task_response.json()["id"]

        # Create rating with invalid value
        # Pydantic validates at schema level, so returns 422 (validation error)
        response = client.post(
            "/api/ratings/",
            json={
                "task_id": task_id,
                "rating": MIN_RATING - 1,  # Invalid: should be 1-5
                "comment": "Test",
            },
        )

        assert response.status_code == 422  # Pydantic validation error
        # Check that validation error mentions rating constraint
        error_detail = str(response.json())
        assert "rating" in error_detail.lower() or "less than" in error_detail.lower()

    def test_create_rating_task_not_found(self, client, setup_database):
        """Test rating creation for non-existent task."""
        response = client.post(
            "/api/ratings/", json={"task_id": 999, "rating": 5, "comment": "Test"}
        )

        assert response.status_code == 404
        assert "Task not found" in response.json()["detail"]


class TestGetRatings:
    """Tests for GET /api/ratings/{task_id} endpoint."""

    @patch("task_breakdown.api.tasks.generate_task_breakdown")
    def test_get_ratings_empty(self, mock_generate, client, setup_database, sample_breakdown_data):
        """Test getting ratings when task has no ratings."""
        mock_generate.return_value = sample_breakdown_data

        # Create a task
        task_response = client.post(
            "/api/tasks",
            json={"description": "Test task description that is long enough"},
        )
        task_id = task_response.json()["id"]

        # Get ratings (should be empty)
        response = client.get(f"/api/ratings/{task_id}")

        assert response.status_code == 200
        assert response.json()["total_ratings"] == 0
        assert response.json()["average_rating"] == 0.0
        assert response.json()["ratings"] == []

    @patch("task_breakdown.api.tasks.generate_task_breakdown")
    def test_get_ratings_with_data(
        self, mock_generate, client, setup_database, sample_breakdown_data
    ):
        """Test getting ratings with existing ratings."""
        mock_generate.return_value = sample_breakdown_data

        # Create a task
        task_response = client.post(
            "/api/tasks",
            json={"description": "Test task description that is long enough"},
        )
        task_id = task_response.json()["id"]

        # Create multiple ratings
        client.post("/api/ratings", json={"task_id": task_id, "rating": 5})
        client.post("/api/ratings", json={"task_id": task_id, "rating": 4})
        client.post("/api/ratings", json={"task_id": task_id, "rating": 3})

        # Get ratings
        response = client.get(f"/api/ratings/{task_id}")

        assert response.status_code == 200
        assert response.json()["total_ratings"] == 3
        assert response.json()["average_rating"] == 4.0  # (5+4+3)/3 = 4.0
        assert len(response.json()["ratings"]) == 3

    @patch("task_breakdown.api.tasks.generate_task_breakdown")
    def test_get_ratings_average_calculation(
        self, mock_generate, client, setup_database, sample_breakdown_data
    ):
        """Test average rating calculation."""
        mock_generate.return_value = sample_breakdown_data

        # Create a task
        task_response = client.post(
            "/api/tasks",
            json={"description": "Test task description that is long enough"},
        )
        task_id = task_response.json()["id"]

        # Create ratings: 5, 5, 1
        client.post("/api/ratings", json={"task_id": task_id, "rating": 5})
        client.post("/api/ratings", json={"task_id": task_id, "rating": 5})
        client.post("/api/ratings", json={"task_id": task_id, "rating": 1})

        # Get ratings
        response = client.get(f"/api/ratings/{task_id}")

        assert response.status_code == 200
        assert response.json()["average_rating"] == pytest.approx(
            3.67, abs=0.01
        )  # (5+5+1)/3 = 3.67

    def test_get_ratings_task_not_found(self, client, setup_database):
        """Test getting ratings for non-existent task."""
        response = client.get("/api/ratings/999")

        assert response.status_code == 404
        assert "Task not found" in response.json()["detail"]
