def test_chat(client):
    response = client.post("/api/v1/chat", json={"message": "Test plan"})
    assert response.status_code == 200
    assert "response" in response.json()
