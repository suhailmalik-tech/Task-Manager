import pytest
from fastapi.testclient import TestClient
from main import app
from app.utils.db import Base, engine, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Use SQLite in-memory database for isolated, fast test execution
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_user_registration_and_login():
    # Register user
    reg_payload = {
        "name": "John Doe",
        "username": "johndoe",
        "password": "Password123!",
        "email": "john@example.com"
    }
    response = client.post("/user/register", json=reg_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "john@example.com"
    assert data["username"] == "johndoe"
    assert "id" in data
    assert "password" not in data

    # Duplicate email prevention
    response_dup = client.post("/user/register", json={
        "name": "Other John",
        "username": "otherjohn",
        "password": "Password123!",
        "email": "john@example.com"
    })
    assert response_dup.status_code == 400

    # Duplicate username prevention
    response_dup_user = client.post("/user/register", json={
        "name": "Other John",
        "username": "johndoe",
        "password": "Password123!",
        "email": "otherjohn@example.com"
    })
    assert response_dup_user.status_code == 400

    # Login with wrong password
    login_fail = client.post("/user/login", json={
        "email": "john@example.com",
        "password": "WrongPassword"
    })
    assert login_fail.status_code == 401

    # Login with correct password
    login_success = client.post("/user/login", json={
        "email": "john@example.com",
        "password": "Password123!"
    })
    assert login_success.status_code == 200
    token_data = login_success.json()
    assert "token" in token_data
    token = token_data["token"]

    # Verify is_auth endpoint with token
    auth_resp = client.get("/user/is_auth", headers={"Authorization": f"Bearer {token}"})
    assert auth_resp.status_code == 200
    assert auth_resp.json()["email"] == "john@example.com"

def test_tasks_crud_and_user_isolation():
    # Register User 1
    user1_reg = client.post("/user/register", json={
        "name": "User One",
        "username": "userone",
        "password": "pass123user1",
        "email": "user1@example.com"
    })
    assert user1_reg.status_code == 201
    login1 = client.post("/user/login", json={"email": "user1@example.com", "password": "pass123user1"})
    token1 = login1.json()["token"]
    headers1 = {"Authorization": f"Bearer {token1}"}

    # Register User 2
    user2_reg = client.post("/user/register", json={
        "name": "User Two",
        "username": "usertwo",
        "password": "pass123user2",
        "email": "user2@example.com"
    })
    assert user2_reg.status_code == 201
    login2 = client.post("/user/login", json={"email": "user2@example.com", "password": "pass123user2"})
    token2 = login2.json()["token"]
    headers2 = {"Authorization": f"Bearer {token2}"}

    # Unauthenticated task creation attempt
    no_auth_resp = client.post("/tasks/create", json={"title": "Test Task", "description": "Desc"})
    assert no_auth_resp.status_code == 401

    # User 1 creates a task
    create_resp = client.post("/tasks/create", json={
        "title": "User 1 Task",
        "description": "Buy groceries",
        "is_completed": False
    }, headers=headers1)
    assert create_resp.status_code == 201
    task1 = create_resp.json()
    task1_id = task1["id"]
    assert task1["title"] == "User 1 Task"
    assert task1["user_id"] == user1_reg.json()["id"]

    # User 1 gets all tasks
    get_tasks1 = client.get("/tasks/get_tasks", headers=headers1)
    assert get_tasks1.status_code == 200
    assert len(get_tasks1.json()) == 1

    # User 1 gets specific task
    get_one1 = client.get(f"/tasks/get_one/{task1_id}", headers=headers1)
    assert get_one1.status_code == 200
    assert get_one1.json()["id"] == task1_id

    # User 1 updates task
    update1 = client.put(f"/tasks/update_task/{task1_id}", json={
        "title": "User 1 Task Updated",
        "description": "Buy organic groceries",
        "is_completed": True
    }, headers=headers1)
    assert update1.status_code == 200
    assert update1.json()["title"] == "User 1 Task Updated"
    assert update1.json()["is_completed"] is True

    # User 2 attempts to read User 1's tasks
    get_tasks2 = client.get("/tasks/get_tasks", headers=headers2)
    assert get_tasks2.status_code == 200
    assert len(get_tasks2.json()) == 0  # Isolation check

    # User 2 attempts to read User 1's specific task -> 404
    get_one2 = client.get(f"/tasks/get_one/{task1_id}", headers=headers2)
    assert get_one2.status_code == 404

    # User 2 attempts to update User 1's task -> 404
    update2 = client.put(f"/tasks/update_task/{task1_id}", json={
        "title": "Hacked Title",
        "description": "Hacked",
        "is_completed": False
    }, headers=headers2)
    assert update2.status_code == 404

    # User 2 attempts to delete User 1's task -> 404
    delete2 = client.delete(f"/tasks/delete_task/{task1_id}", headers=headers2)
    assert delete2.status_code == 404

    # User 1 deletes their task -> 204
    delete1 = client.delete(f"/tasks/delete_task/{task1_id}", headers=headers1)
    assert delete1.status_code == 204

    # Verify task is deleted
    get_tasks_after = client.get("/tasks/get_tasks", headers=headers1)
    assert len(get_tasks_after.json()) == 0
