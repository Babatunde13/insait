import pytest
from marshmallow.exceptions import ValidationError
from app.validation.validator import RegisterSchema, LoginSchema, GenerateTextSchema, UpdateTextSchema

def test_register_schema_valid():
    schema = RegisterSchema()
    data = {"username": "testuser", "password": "TestPassword1"}

    result = schema.load(data)
    assert result == data

def test_register_schema_invalid_username_too_short():
    schema = RegisterSchema()
    data = {"username": "tu", "password": "TestPassword1"}
    
    with pytest.raises(ValidationError) as excinfo:
        schema.load(data)
    assert "Username must be at least 3 characters long." in str(excinfo.value)

def test_register_schema_invalid_username_with_spaces():
    schema = RegisterSchema()
    data = {"username": "test user", "password": "TestPassword1"}
    
    with pytest.raises(ValidationError) as excinfo:
        schema.load(data)
    assert "Username cannot contain spaces." in str(excinfo.value)

def test_register_schema_invalid_password_too_short():
    schema = RegisterSchema()
    data = {"username": "testuser", "password": "short"}
    
    with pytest.raises(ValidationError) as excinfo:
        schema.load(data)
    assert "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number." in str(excinfo.value)

def test_register_schema_invalid_password_missing_required_chars():
    schema = RegisterSchema()
    data = {"username": "testuser", "password": "password123"}
    
    with pytest.raises(ValidationError) as excinfo:
        schema.load(data)
    assert "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number." in str(excinfo.value)

def test_login_schema_valid():
    schema = LoginSchema()
    data = {"username": "testuser", "password": "TestPassword1"}
    
    result = schema.load(data)
    assert result == data

def test_generate_text_schema_valid():
    schema = GenerateTextSchema()
    data = {"prompt": "This is a valid prompt."}

    result = schema.load(data)
    assert result == data

def test_generate_text_schema_invalid_prompt_too_short():
    schema = GenerateTextSchema()
    data = {"prompt": "123"}

    with pytest.raises(ValidationError) as excinfo:
        schema.load(data)
    assert "Prompt must be at least 5 characters long." in str(excinfo.value)

def test_update_text_schema_valid():
    schema = UpdateTextSchema()
    data = {"prompt": "This is an updated valid prompt."}

    result = schema.load(data)
    assert result == data

def test_update_text_schema_invalid_prompt_too_short():
    schema = UpdateTextSchema()
    data = {"prompt": "123"}

    with pytest.raises(ValidationError) as excinfo:
        schema.load(data)
    assert "Prompt must be at least 5 characters long." in str(excinfo.value)
