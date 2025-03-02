import pytest
from unittest.mock import patch
from app.services.ai import ai_service

def test_generate_text(mock_openai_create):
    prompt = "Hello, AI!"
    response = ai_service.generate_text(prompt)

    assert response == "This is a test response."
    mock_openai_create.assert_called_once_with(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

