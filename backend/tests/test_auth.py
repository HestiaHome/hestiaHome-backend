"""
Тестирование endpoint'ов для аунтентификации пользователя.
"""

from conftest import client
from database.database import SessionLocal

session = SessionLocal()


class TestUserAuthentication:
    def test_register_client(self):
        response = client.post("/auth/register",
                               json={
                                   "email": "user@example.com",
                                   "password": "example_password",
                                   "is_active": True,
                                   "is_superuser": False,
                                   "is_verified": False,
                                   "username": "user_example1"
                               })

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "user@example.com"
        assert data["is_active"] is True
        assert data["is_superuser"] is False
        assert data["is_verified"] is False
        assert data["username"] == "user_example1"
        assert "password" not in data
        assert "hashed_password" not in data

    def test_login_client(self):
        response = client.post("/auth/jwt/login", data={"username": "user@example.com", "password": "example_password"})
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data and data["token_type"] == "bearer"

    def test_authenticated_authorized_client(self):
        response = client.post("/auth/jwt/login", data={"username": "user@example.com", "password": "example_password"})
        data = response.json()
        access_token = data["access_token"]
        response = client.get("/authenticated-route", headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200

    def test_authenticated_not_authorized_client(self):
        response = client.get("/authenticated-route")
        assert response.status_code == 401
        assert response.json().get("detail") == "Unauthorized"

    def test_logout_client(self):
        response = client.post("/auth/jwt/login", data={"username": "user@example.com", "password": "example_password"})
        data = response.json()
        access_token = data["access_token"]
        response = client.post("/auth/jwt/logout", headers={"Authorization": f"Bearer {access_token}"})
        assert response.status_code == 200
        response = client.get("/authenticated-route")
        assert response.status_code == 401
        data = response.json()
        assert data.get("detail") == "Unauthorized"

    def test_bad_login(self):
        response = client.post("/auth/jwt/login",
                               data={"username": "user123@example.com", "password": "example_password"})
        assert response.status_code == 400
        data = response.json()
        assert data.get("detail") == "LOGIN_BAD_CREDENTIALS"

    def test_user_get_himself(self):
        client.post("/auth/register",
                    json={
                        "email": "user1@example.com",
                        "password": "user_example2",
                        "is_active": True,
                        "is_superuser": False,
                        "is_verified": False,
                        "username": "user_example2"
                    })

        response = client.post("/auth/jwt/login", data={"username": "user1@example.com", "password": "user_example2"})
        data = response.json()
        access_token = data["access_token"]

        response = client.get("/users/me", headers={"Authorization": f"Bearer {access_token}"})
        data = response.json()
        assert response.status_code == 200
        assert "id" in data
        assert data.get("email") == "user1@example.com"
        assert data.get("username") == "user_example2"

        assert "password" not in data or "hashed_password" not in data

        assert "password" not in data or "hashed_password" not in data

# class TestDevices:
#
#     def test_send_data(self):
#         client.post("/devices/send_data/")
