# Insait AI Text Generation API

This is an AI-based text generation API built with Flask, PostgreSQL, and OpenAI API integration. The API allows users to generate and manage AI-generated text using prompts. It supports CRUD operations on generated text.

## Table of Contents

- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Testing](#testing)
- [Running The API](#running-the-api)
- [Endpoints](#endpoints)
  - [Register](#register)
  - [Login](#login)
  - [Generate Text](#generate-text)
  - [Get Generated Text](#get-generated-text)
  - [Update Generated Text](#update-generated-text)
  - [Delete Generated Text](#delete-generated-text)
- [Error Codes](#error-codes)
- [License](#license)

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/insait.git
   cd insait
   ```
2. Build the Docker containers:
    ```
    docker-compose up --build
    ```
3. The API will be running at http://localhost:4012 once the containers are started.

## Environment Variables
```bash
SECRET_KEY=
DATABASE_URL=
SQLALCHEMY_TRACK_MODIFICATIONS=
JWT_SECRET_KEY=
PORT=
OPENAI_API_KEY=
FLASK_ENV=
USE_AI_MOCK=
TEST_DATABASE_URL=
```

If you set a value for USE_AI_MOCK and the call to OpenAI fails this will return a dummy data. This is useful if you want to quickly test the API implementation without worrying about responses from OpenAI.

## Testing
To test the API with both unit and integration tests, you need to have a running database
If you have a running database, you can run the command below after setting the `TEST_DATABASE_URL`
```bash
    pytest tests
```

Alternatively, you can use the command below to run the test in a container
```bash
docker-compose run -e FLASK_ENV=testing app pytest tests/
```

### Running The API
To run the Api, you can run it with `python run.py` if you already have your database setup and set in the environment variable (`DATABASE_URL`). Alternatively, you can run the API with the command below, this persists the DB so if you restart the container you still have access to your existing data
```bash
docker-compose up
```

## Endpoints
1. ### Register
    URL: `/register`
    Method: POST
    Description: Creates a new user.
    Request Body:

    ```json
    {
        "username": "string|required|min=5",
        "password": "string|required|min=6",
    }
    ```

    Response Body

    ```json
    {
        "message": "User registered successfully",
        "data": {}
    }
    ```

    #### Account already exists
    ```json
    {
        "error": "User already exists"
    }
    ```

2. ### Login
    URL: `/login`
    Method: POST
    Description: Login a user
    Request Body:

    ```json
    {
        "username": "string|required|min=5",
        "password": "string|required|min=6",
    }
    ```

    Response Body

    ```json
    {
        "message": "User authenticated successfully",
        "data": {
            "access_token": "<token>"
        }
    }
    ```

    #### Account does not exist/invalid password
    ```json
    {
        "error": "Invalid credentials"
    }
    ```

3. ### Generate Text
    URL: `/generate-text`
    Method: POST
    Description: Generates text based on the provided prompt.
    Request Body:

    ```json
    {
        "prompt": "string|required"
    }
    ```

    Response Body

    ```json
    {
        "message": "Text generated successfully",
        "data": {
            "id": 1,
            "user_id": 123,
            "prompt": "string",
            "response": "string",
            "timestamp": "string",
            "created_at": "string",
            "updated_at": "string"
        }
    }
    ```

4. ### Get Generated Text
URL: `/generated-text/{text_id}`
Method: GET
Description: Fetches the generated text by ID.
Request Parameters:
text_id (integer, required): The ID of the generated text.
Response:

```json
{
    "message": "Text retrieved successfully",
    "data": {
        "id": 1,
        "user_id": 123,
        "prompt": "string",
        "response": "string",
        "timestamp": "string",
        "created_at": "string",
        "updated_at": "string"
    }
}
```

Error Response(404)

```json
{
    "error": "Text not found"
}
```

5. ### Update Generated Text
URL: `/generated-text/{text_id}`
Method: PUT
Description: Updates an existing generated text record with a new response by recalling open AI with the saved prompt.
Request Parameters:
text_id (integer, required): The ID of the generated text.
Request Body:
Response:

```json
{
    "message": "Text updated successfully",
    "data": {
        "id": 1,
        "user_id": 123,
        "prompt": "string",
        "response": "string",
        "timestamp": "string",
        "created_at": "string",
        "updated_at": "string"
    }
}
```


Error Response(404)

```json
{
    "error": "Text not found"
}
```

6. ### Delete Generated Text
URL: `/generated-text/{text_id}`
Method: DELETE
Description: Deletes the generated text by ID.
Request Parameters:
text_id (integer, required): The ID of the generated text.
Response:

```json
{
    "message": "Text deleted successfully",
    "data": {}
}
```

message: A message indicating success.
Error Response(404):

```json
{
    "error": "Text not found"
}
```

## Error Codes
The API will return the following common error codes and messages:

Status Code	Error Message	Description
400	Validation error	Input validation failed, such as missing or invalid fields.
401	Invalid token	Authentication failed. Invalid or expired JWT token.
404	Text not found	The requested generated text ID does not exist.
500	Internal server error	Something went wrong on the server side.
