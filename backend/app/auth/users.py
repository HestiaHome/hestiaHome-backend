from typing import Optional, Dict, Any
from log_settings import logger

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase

from .db import User, get_user_db

SECRET = "SECRET"


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        # print(f"User {user.id} has registered.")
        logger.debug(f"User {user.id} has registered.")

    async def on_after_login(self, user: User, request: Optional[Request] = None):
        logger.debug(f"User {user.id} has login.")

    async def on_after_delete(self, user: User, request: Optional[Request] = None) -> None:
        logger.debug(f"User {user.id} deleted.")

    async def on_after_update(self, user: User, update_dict: Dict[str, Any], request: Optional[Request] = None,) -> None:
        logger.debug(f"User {user.id} update his profile.")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
super_user = fastapi_users.current_user(superuser=True)
