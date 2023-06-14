# import pytest
#
# from conftest import client
# from database.database import SessionLocal
# 
# session = SessionLocal()

# TODO: Написать тест для websocket

# @pytest.fixture()
# def register_and_auth_user():
#     client.post("/auth/register",
#                            json={
#                                "email": "user@example.com",
#                                "password": "example_password",
#                                "is_active": True,
#                                "is_superuser": False,
#                                "is_verified": False,
#                                "username": "user_example1"
#                            })
#
#     response = client.post("/auth/jwt/login",
#                            data={"username": "user@example.com",
#                                  "password": "example_password"})
#     data = response.json()
#     token = data["access_token"]
#     return token
#
#
# def test_websocket(register_and_auth_user):
#     pass
