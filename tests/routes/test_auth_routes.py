def test_invalid_request_body(client):
    res = client.post("/register", json={"username": "us", "password": "testpass"})
    assert res.status_code == 400
    assert "password" in res.get_json()
    assert "username" in res.get_json()

    assert "Username must be at least 3 characters long." in res.get_json()["username"]
    assert "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number." in res.get_json()["password"]

def test_register_user(client):
    res = client.post("/register", json={"username": "newuser", "password": "Pasword@13"})
    assert res.status_code == 201
    assert "User registered successfully" in res.get_json()["message"]

def test_register_duplicate_user(client):
    client.post("/register", json={"username": "testuser", "password": "Pasword@13"})
    res = client.post("/register", json={"username": "testuser", "password": "Pasword@13"})
    assert res.status_code == 400
    assert "User already exists" in res.get_json()["error"]

def test_login_user(client, test_user):
    res = client.post("/login", json={"username": test_user.username, "password": test_user.password})
    assert res.status_code == 200
    assert "access_token" in res.get_json()["data"]

def test_login_invalid_credentials(client):
    res = client.post("/login", json={"username": "testuser", "password": "Pasword@1334"})
    assert res.status_code == 401
    assert "Invalid credentials" in res.get_json()["error"]
