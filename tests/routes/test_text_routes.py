def test_generate_text_failure(client, auth_headers):
    res = client.post("/generate-text", json={"prompt": "dd"}, headers=auth_headers)
    assert res.status_code == 400
    assert res.get_json()["prompt"][0] == "Prompt must be at least 5 characters long."

def test_save_generated_text(client, auth_headers, mock_openai_create):
    res = client.post("/generate-text", json={"prompt": "Test prompt"}, headers=auth_headers)
    assert res.status_code == 201
    text_id = res.get_json()["data"]["id"]

    res = client.get(f"/generated-text/{text_id}", headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()["data"]["prompt"] == "Test prompt"

def test_update_generated_text(client, auth_headers, mock_openai_create):
    res = client.post("/generate-text", json={"prompt": "prompt"}, headers=auth_headers)
    text_id = res.get_json()["data"]["id"]

    res = client.put(f"/generated-text/{text_id}", json={}, headers=auth_headers)
    assert res.status_code == 200
    text = res.get_json()["data"]
    assert text["prompt"] == "prompt"
    assert text["id"] == text_id

    res = client.get(f"/generated-text/{text_id}", headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()["data"]["prompt"] == "prompt"
    assert res.get_json()["data"]["id"] == text_id
    assert res.get_json()["data"]["response"] == text["response"]


def test_delete_generated_text(client, auth_headers, mock_openai_create):
    res = client.post("/generate-text", json={"prompt": "To delete"}, headers=auth_headers)
    text_id = res.get_json()["data"]["id"]

    res = client.delete(f"/generated-text/{text_id}", headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()["message"] == "Text deleted successfully"

    res = client.get(f"/generated-text/{text_id}", headers=auth_headers)
    assert res.status_code == 404
