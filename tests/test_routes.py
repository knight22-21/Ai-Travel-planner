def test_chat(client):
    response = client.post("/api/v1/chat", json={"message": "Test plan"})
    assert response.status_code == 200
    assert "response" in response.json()

def test_generate_pdf(client):
    chat_history = [
        {"role": "user", "content": "Hi"},
        {"role": "guide", "content": "Hello! How can I help you plan your trip?"}
    ]
    response = client.post("/api/v1/pdf", json={"history": chat_history})
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
