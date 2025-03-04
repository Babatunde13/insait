import re
from marshmallow import Schema, fields, validates, ValidationError

class RegisterSchema(Schema):
    """Schema for user registration validation."""
    username = fields.Str(required=True)
    password = fields.Str(required=True)

    @validates("username")
    def validate_username(self, value):
        value = value.strip().lower()
        if len(value) < 3:
            raise ValidationError("Username must be at least 3 characters long.")
        if " " in value:
            raise ValidationError("Username cannot contain spaces.")
        
    @validates("password")
    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number.")

        regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$"
        if not re.match(regex, value):
            raise ValidationError("Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number.")

class LoginSchema(Schema):
    """Schema for user login validation."""
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class GenerateTextSchema(Schema):
    """Schema for validating AI text generation request."""
    prompt = fields.Str(required=True)

    @validates("prompt")
    def validate_prompt(self, value):
        if len(value) < 5:
            raise ValidationError("Prompt must be at least 5 characters long.")
