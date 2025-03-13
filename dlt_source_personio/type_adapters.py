from typing import List

from .model.v2.auth import AuthenticationTokenResponse
from .model.v2.person import Person


from pydantic import TypeAdapter


person_adapter = TypeAdapter(List[Person])
auth_adapter = TypeAdapter(AuthenticationTokenResponse)
