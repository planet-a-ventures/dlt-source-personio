# generated by datamodel-codegen:
#   filename:  auth.yaml

from __future__ import annotations

from enum import Enum

from pydantic_extra_types.pendulum_dt import Date, DateTime

from ..v2 import MyAuthBaseModel


class TokenType(str, Enum):
    BEARER = "Bearer"


class AuthenticationTokenResponse(MyAuthBaseModel):
    access_token: str
    expires_in: float
    scope: str
    token_type: TokenType
    refresh_token: str | None = None
