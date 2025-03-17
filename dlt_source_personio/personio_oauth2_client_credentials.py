from urllib.parse import urljoin
from .settings import X_PERSONIO_APP_ID
from .settings import V2_AUTH_REVOKE, V2_AUTH_TOKEN
from .type_adapters import auth_adapter


from dlt.sources.helpers.rest_client.auth import OAuth2ClientCredentials


from typing import Any


class PersonioOAuth2ClientCredentials(OAuth2ClientCredentials):
    """
    OAuth2 client credentials for Personio API
    """

    api_base: str
    """
    The base URL of the Personio API
    """

    def __init__(self, api_base: str, *args, **kwargs):
        self.api_base = api_base
        super().__init__(
            access_token_url=urljoin(self.api_base, V2_AUTH_TOKEN), *args, **kwargs
        )

    def revoke_token(self) -> None:
        """
        Revoke the current access token
        """

        if self.access_token is None:
            return

        response = self.session.post(
            urljoin(self.api_base, V2_AUTH_REVOKE),
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
                "Authorization": f"Bearer {self.access_token}",
                "X-Personio-App-ID": X_PERSONIO_APP_ID,
            },
            data={
                "token": self.access_token,
            },
        )
        response.raise_for_status()
        self.access_token = None

    def parse_expiration_in_seconds(self, response_json: Any) -> int:
        token_response = auth_adapter.validate_python(response_json)
        return int(token_response.expires_in) | self.default_token_expiration

    def parse_access_token(self, response_json: Any) -> str:
        token_response = auth_adapter.validate_python(response_json)
        return token_response.access_token
