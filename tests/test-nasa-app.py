from unittest.mock import patch

from app import app


def test_home_page():
    mock_response = [
        {
            "date": "2026-10-01",
            "title": "Test NASA Image",
            "media_type": "image",
            "hdurl": "https://example.com/image.jpg",
            "alt": "Test image",
            "explanation": "Test explanation",
            "credit": "Test credit",
            "permalink": "https://example.com",
            "url": "https://example.com",
        }
    ]

    with patch("app.requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.raise_for_status.return_value = None

        client = app.test_client()

        response = client.get("/")

        assert response.status_code == 200
        assert b"Test NASA Image" in response.data