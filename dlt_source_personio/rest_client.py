from typing import Any
import logging
from pydantic import ValidationError

import dlt
from dlt.sources.helpers.rest_client.client import RESTClient, Response
from dlt.sources.helpers.rest_client.paginators import JSONLinkPaginator

from .personio_oauth2_client_credentials import PersonioOAuth2ClientCredentials
from .settings import x_personio_app_id

from .settings import API_BASE
from dlt.sources.helpers.requests.session import Session

# Share a session (and thus pool) between all rest clients
session: Session = Session(raise_for_status=False)

auth: PersonioOAuth2ClientCredentials = None


def get_rest_client(
    api_base: str = API_BASE,
):
    global session
    global auth

    if auth is None:
        auth = PersonioOAuth2ClientCredentials(
            api_base=api_base,
            client_id=dlt.secrets["personio_client_id"],
            client_secret=dlt.secrets["personio_client_secret"],
            default_token_expiration=86400,
            session=session,
        )

    client = RESTClient(
        base_url=api_base,
        headers={
            "Accept": "application/json",
            "X-Personio-App-ID": x_personio_app_id,
        },
        auth=auth,
        data_selector="_data",
        paginator=JSONLinkPaginator(next_url_path="_meta.links.next.href"),
        session=session,
    )
    return client, auth


def debug_response(response: Response, *args: Any, **kwargs: Any) -> None:
    if logging.getLogger().isEnabledFor(logging.DEBUG):
        logging.debug(
            f"Response: {response.status_code} {response.reason} {response.url} {response.text}"
        )


def raise_for_status(response: Response, *args: Any, **kwargs: Any) -> None:
    response.raise_for_status()


hooks = {
    "response": [
        debug_response,
        raise_for_status,
    ]
}
V2_MAX_PAGE_LIMIT = 1
V1_BASE_PAGE = 0
