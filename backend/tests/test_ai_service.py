"""Unit tests for AI service."""


class TestCheckOllamaAvailable:
    """Tests for Ollama availability checking."""

    def test_ollama_function_exists(self):
        """Test that check_ollama_available function exists and is callable."""
        from task_breakdown.services.ai_service import check_ollama_available

        assert callable(check_ollama_available)

        # Function should return a tuple
        # Note: Actual result depends on Ollama installation status
        result = check_ollama_available()
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], bool)
        # Module can be None or the actual module

    def test_ollama_function_signature(self):
        """Test function signature and return type."""
        from task_breakdown.services.ai_service import check_ollama_available

        # Function should be callable without arguments
        result = check_ollama_available()

        # Should return tuple of (bool, module_or_none)
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], bool)

    def test_ollama_function_handles_errors(self):
        """Test that function handles errors gracefully."""
        from task_breakdown.services.ai_service import check_ollama_available

        # Function should not raise exceptions
        # It should handle ImportError and RequestException internally
        result = check_ollama_available()

        # Should always return a tuple
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], bool)
