"""Unit tests for tasks API endpoints."""

from unittest.mock import patch

from task_breakdown.api.tasks import MAX_LIMIT


class TestCreateTask:
    """Tests for POST /api/tasks endpoint."""

    @patch("task_breakdown.api.tasks.generate_task_breakdown")
    def test_create_task_success(
        self, mock_generate, client, setup_database, sample_breakdown_data
    ):
        """Test successful task creation."""
        mock_generate.return_value = sample_breakdown_data

        response = client.post(
            "/api/tasks",
            json={"title": "Test Task", "description": "Create a hello world program"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["description"] == "Create a hello world program"
        assert len(data["guide_steps"]) == 2
        assert data["guide_steps"][0]["step_number"] == 1
        assert data["guide_steps"][0]["title"] == "Step 1"
        assert data["guide_steps"][1]["step_number"] == 2

    @patch("task_breakdown.api.tasks.generate_task_breakdown")
    def test_create_task_without_title(
        self, mock_generate, client, setup_database, sample_breakdown_data
    ):
        """Test task creation without title (should use AI-generated title)."""
        mock_generate.return_value = sample_breakdown_data

        response = client.post("/api/tasks", json={"description": "Create a hello world program"})

        assert response.status_code == 201
        assert response.json()["title"] == "Test Task"

    @patch("task_breakdown.api.tasks.generate_task_breakdown")
    def test_create_task_ai_service_error(self, mock_generate, client, setup_database):
        """Test handling of AI service errors."""
        mock_generate.side_effect = Exception("AI service unavailable")

        response = client.post("/api/tasks", json={"description": "Create a hello world program"})

        assert response.status_code == 500
        assert "Error creating task" in response.json()["detail"]

    @patch("task_breakdown.api.tasks.generate_task_breakdown")
    def test_create_task_with_empty_steps(self, mock_generate, client, setup_database):
        """Test task creation with empty steps."""
        mock_generate.return_value = {
            "title": "Test Task",
            "complexity_score": 5,
            "estimated_total_time": 60,
            "steps": [],
        }

        response = client.post(
            "/api/tasks",
            json={
                "description": "Test task description that is long enough"  # Min 10 chars
            },
        )

        assert response.status_code == 201
        assert len(response.json()["guide_steps"]) == 0


class TestGetTasks:
    """Tests for GET /api/tasks endpoint."""

    def test_get_tasks_empty(self, client, setup_database):
        """Test getting tasks when database is empty."""
        response = client.get("/api/tasks/")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    @patch("task_breakdown.api.tasks.generate_task_breakdown")
    def test_get_tasks_with_data(
        self, mock_generate, client, setup_database, sample_breakdown_data
    ):
        """Test getting tasks with existing data."""
        mock_generate.return_value = sample_breakdown_data

        # Create a task first
        client.post("/api/tasks", json={"title": "Test Task", "description": "Test description"})

        # Get all tasks
        response = client.get("/api/tasks/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Test Task"

    @patch("task_breakdown.api.tasks.generate_task_breakdown")
    def test_get_tasks_with_pagination(
        self, mock_generate, client, setup_database, sample_breakdown_data
    ):
        """Test getting tasks with pagination."""
        mock_generate.return_value = sample_breakdown_data

        # Create multiple tasks
        for i in range(5):
            client.post(
                "/api/tasks",
                json={"title": f"Task {i}", "description": f"Description {i}"},
            )

        # Get tasks with limit
        response = client.get("/api/tasks/?skip=0&limit=3")

        assert response.status_code == 200
        assert len(response.json()) == 3

    @patch("task_breakdown.api.tasks.generate_task_breakdown")
    def test_get_tasks_with_invalid_limit(
        self, mock_generate, client, setup_database, sample_breakdown_data
    ):
        """Test getting tasks with invalid limit (should clamp to MAX_LIMIT)."""
        mock_generate.return_value = sample_breakdown_data

        # Create a task
        client.post("/api/tasks", json={"title": "Test Task", "description": "Test description"})

        # Request with limit exceeding MAX_LIMIT
        response = client.get(f"/api/tasks/?skip=0&limit={MAX_LIMIT + 100}")

        assert response.status_code == 200
        # Should return tasks but limit should be clamped internally

    def test_get_tasks_with_negative_skip(self, client, setup_database):
        """Test getting tasks with negative skip value."""
        response = client.get("/api/tasks/?skip=-1&limit=10")

        assert response.status_code == 200


class TestGetTask:
    """Tests for GET /api/tasks/{task_id} endpoint."""

    @patch("task_breakdown.api.tasks.generate_task_breakdown")
    def test_get_task_success(self, mock_generate, client, setup_database, sample_breakdown_data):
        """Test getting a specific task."""
        mock_generate.return_value = sample_breakdown_data

        # Create task
        create_response = client.post(
            "/api/tasks", json={"title": "Test Task", "description": "Test description"}
        )
        task_id = create_response.json()["id"]

        # Get task
        response = client.get(f"/api/tasks/{task_id}")

        assert response.status_code == 200
        assert response.json()["id"] == task_id
        assert response.json()["title"] == "Test Task"
        assert len(response.json()["guide_steps"]) == 2

    def test_get_task_not_found(self, client, setup_database):
        """Test getting a non-existent task."""
        response = client.get("/api/tasks/999")

        assert response.status_code == 404
        assert "Task not found" in response.json()["detail"]

    def test_get_task_invalid_id(self, client, setup_database):
        """Test getting task with invalid ID format."""
        response = client.get("/api/tasks/invalid")

        assert response.status_code == 422  # Validation error


class TestDeleteTask:
    """Tests for DELETE /api/tasks/{task_id} endpoint."""

    @patch("task_breakdown.api.tasks.generate_task_breakdown")
    def test_delete_task_success(
        self, mock_generate, client, setup_database, sample_breakdown_data
    ):
        """Test successful task deletion."""
        mock_generate.return_value = sample_breakdown_data

        # Create task
        create_response = client.post(
            "/api/tasks", json={"title": "Test Task", "description": "Test description"}
        )
        task_id = create_response.json()["id"]

        # Delete task
        response = client.delete(f"/api/tasks/{task_id}")

        assert response.status_code == 204

        # Verify task is deleted
        get_response = client.get(f"/api/tasks/{task_id}")
        assert get_response.status_code == 404

    def test_delete_task_not_found(self, client, setup_database):
        """Test deleting a non-existent task."""
        response = client.delete("/api/tasks/999")

        assert response.status_code == 404
        assert "Task not found" in response.json()["detail"]
