from typing import List

from .model.v2.auth import AuthenticationTokenResponse
from .model.v2.person import Person
from .model.v2.employment import Employment


from pydantic import TypeAdapter


persons_adapter = TypeAdapter(List[Person])
employments_adapter = TypeAdapter(List[Employment])
auth_adapter = TypeAdapter(AuthenticationTokenResponse)
