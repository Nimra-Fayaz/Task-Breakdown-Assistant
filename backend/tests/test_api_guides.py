"""Unit tests for guides API endpoints."""

from unittest.mock import patch


class TestGetGuide:
    """Tests for GET /api/guides/{task_id} endpoint."""

    @patch("task_breakdown.api.tasks.generate_task_breakdown")
    def test_get_guide_success(self, mock_generate, client, setup_database, sample_breakdown_data):
        """Test successful guide retrieval."""
        mock_generate.return_value = sample_breakdown_data

        # Create a task
        task_response = client.post(
            "/api/tasks", json={"title": "Test Task", "description": "Test description"}
        )
        task_id = task_response.json()["id"]

        # Get guide steps
        response = client.get(f"/api/guides/{task_id}")

        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]["step_number"] == 1
        assert response.json()[0]["title"] == "Step 1"
        assert response.json()[1]["step_number"] == 2
        assert response.json()[1]["title"] == "Step 2"

    @patch("task_breakdown.api.tasks.generate_task_breakdown")
    def test_get_guide_empty_steps(self, mock_generate, client, setup_database):
        """Test getting guide for task with no steps."""
        mock_generate.return_value = {
            "title": "Test Task",
            "complexity_score": 5,
            "estimated_total_time": 60,
            "steps": [],
        }

        # Create a task
        task_response = client.post(
            "/api/tasks",
            json={"description": "Test task description that is long enough"},
        )
        task_id = task_response.json()["id"]

        # Get guide steps
        response = client.get(f"/api/guides/{task_id}")

        assert response.status_code == 200
        assert response.json() == []

    def test_get_guide_task_not_found(self, client, setup_database):
        """Test getting guide for non-existent task."""
        response = client.get("/api/guides/999")

        assert response.status_code == 404
        assert "Task not found" in response.json()["detail"]

    @patch("task_breakdown.api.tasks.generate_task_breakdown")
    def test_get_guide_steps_ordered(self, mock_generate, client, setup_database):
        """Test that guide steps are returned in correct order."""
        mock_generate.return_value = {
            "title": "Test Task",
            "complexity_score": 5,
            "estimated_total_time": 60,
            "steps": [
                {
                    "step_number": 3,
                    "title": "Step 3",
                    "description": "Third step",
                    "detailed_instructions": "Do this third",
                    "estimated_time": 30,
                    "dependencies": [],
                    "resources": [],
                    "code_snippets": [],
                    "tips": None,
                    "warnings": None,
                    "verification_steps": None,
                },
                {
                    "step_number": 1,
                    "title": "Step 1",
                    "description": "First step",
                    "detailed_instructions": "Do this first",
                    "estimated_time": 10,
                    "dependencies": [],
                    "resources": [],
                    "code_snippets": [],
                    "tips": None,
                    "warnings": None,
                    "verification_steps": None,
                },
                {
                    "step_number": 2,
                    "title": "Step 2",
                    "description": "Second step",
                    "detailed_instructions": "Do this second",
                    "estimated_time": 20,
                    "dependencies": [],
                    "resources": [],
                    "code_snippets": [],
                    "tips": None,
                    "warnings": None,
                    "verification_steps": None,
                },
            ],
        }

        # Create a task
        task_response = client.post(
            "/api/tasks",
            json={"description": "Test task description that is long enough"},
        )
        task_id = task_response.json()["id"]

        # Get guide steps
        response = client.get(f"/api/guides/{task_id}")

        assert response.status_code == 200
        steps = response.json()
        # Steps should be ordered by step_number
        assert steps[0]["step_number"] == 1
        assert steps[1]["step_number"] == 2
        assert steps[2]["step_number"] == 3
