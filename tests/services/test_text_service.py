import pytest
from app.services.text import TextService
from app.extensions import db

@pytest.fixture
def test_text(test_user):
    text = TextService.save_generated_text(test_user.id, "prompt", "response")
    return text

def test_save_generated_text(test_user):
    result = TextService.save_generated_text(test_user.id, "prompt", "response")
    assert result.user_id == test_user.id
    assert result.prompt == "prompt"
    assert result.response == "response"
    assert result.id is not None
    assert result.created_at is not None
    assert result.updated_at is not None

def test_get_text_by_id_success(test_text):
    text = TextService.get_text_by_id(test_text.id, test_text.user_id)
    assert text == test_text

def test_get_text_by_id_not_found(test_text):
    text = TextService.get_text_by_id(test_text.id, test_text.user_id + 1)
    assert text is None

def test_update_text_success(test_text):
    result = TextService.update_text(test_text,  "updated prompt", "new response")
    assert result.response == "new response"
    assert result.prompt == "updated prompt"


def test_delete_text_success(test_text):
    result = TextService.delete_text(test_text.id, test_text.user_id)
    assert result is True


def test_delete_text_not_found(test_text):
    result = TextService.delete_text(test_text.id, test_text.user_id + 1)
    assert result is False
