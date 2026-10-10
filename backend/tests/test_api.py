from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_python_vs_python():
    response = client.post(
        "/api/v1/analyze",
        json={
            "code_a": "import os\nos.system('calc')",
            "language_a": "python",
            "code_b": "import os\nos.system('whoami')",
            "language_b": "python"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["similarity"]["similarity_percentage"] == 100.0

def test_api_js_vs_js():
    response = client.post(
        "/api/v1/analyze",
        json={
            "code_a": "child_process.exec('calc');",
            "language_a": "javascript",
            "code_b": "child_process.exec('whoami');",
            "language_b": "javascript"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["similarity"]["similarity_percentage"] == 100.0

def test_api_python_vs_js():
    response = client.post(
        "/api/v1/analyze",
        json={
            "code_a": "import os\nos.system('calc')",
            "language_a": "python",
            "code_b": "child_process.exec('whoami');",
            "language_b": "javascript"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["similarity"]["similarity_percentage"] == 100.0
    assert data["tags_a"] == ["EXEC_SYS_CMD"]
    assert data["tags_b"] == ["EXEC_SYS_CMD"]

def test_api_different_behavior():
    response = client.post(
        "/api/v1/analyze",
        json={
            "code_a": "open('test.txt', 'w')",
            "language_a": "python",
            "code_b": "child_process.exec('whoami');",
            "language_b": "javascript"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["similarity"]["similarity_percentage"] == 0.0

def test_api_empty_input():
    response = client.post(
        "/api/v1/analyze",
        json={
            "code_a": "",
            "language_a": "python",
            "code_b": "open('test.txt', 'w')",
            "language_b": "python"
        }
    )
    assert response.status_code == 400
    assert "cannot be empty" in response.json()["detail"]

def test_api_unsupported_language():
    response = client.post(
        "/api/v1/analyze",
        json={
            "code_a": "print('hello')",
            "language_a": "ruby",
            "code_b": "open('test.txt', 'w')",
            "language_b": "python"
        }
    )
    assert response.status_code == 400
    assert "Unsupported language: ruby" in response.json()["detail"]

def test_api_malformed_code():
    response = client.post(
        "/api/v1/analyze",
        json={
            "code_a": "this is not python",
            "language_a": "python",
            "code_b": "this is not javascript => {",
            "language_b": "javascript"
        }
    )
    assert response.status_code == 400
    assert "Syntax error" in response.json()["detail"]
