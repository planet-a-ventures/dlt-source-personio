"""A source loading entities and lists from personio  (personio.com)"""

from enum import StrEnum
from typing import Any, Iterable, List, Sequence
import dlt
import logging
from dlt.common.logger import is_logging
from dlt.common.typing import TDataItem
from dlt.sources import DltResource
from dlt.sources.helpers.rest_client.client import RESTClient
import jmespath
from pydantic import AnyUrl
import re

from dlt.common import json
from dlt.common.json import JsonSerializable

from .model.v2.person import Person

from .settings import V2_PERSONS
from pydantic import BaseModel
from .rest_client import get_rest_client, V2_MAX_PAGE_LIMIT, hooks
from .type_adapters import persons_adapter, employments_adapter


# logging.basicConfig(level=logging.DEBUG)

if is_logging():
    logger = logging.getLogger("dlt")

    class HideSinglePagingNonsense(logging.Filter):
        def filter(self, record):
            msg = record.getMessage()
            if (
                "Extracted data of type list from path _data with length 1" in msg
                or re.match(
                    r"Paginator JSONLinkPaginator at [a-fA-F0-9]+: next_url_path: _meta\.links\.next\.href does not have more pages",
                    msg,
                )
            ):
                return False
            return True

    logger.addFilter(HideSinglePagingNonsense())


def anyurl_encoder(obj: Any) -> JsonSerializable:
    if isinstance(obj, AnyUrl):
        return obj.unicode_string()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


json.set_custom_encoder(anyurl_encoder)


def pydantic_model_dump(model: BaseModel, **kwargs):
    """
    Dumps a Pydantic model to a dictionary, using the model's field names as keys and NOT observing the field aliases,
    which is important for DLT to correctly map the data to the destination.
    """
    return model.model_dump(by_alias=True, **kwargs)


class Table(StrEnum):
    CUSTOM_ATTRIBUTES = "persons_custom_attributes"
    EMPLOYMENTS = "employments"
    PERSONS = "persons"
    PERSONS_PROFILE_PICTURES = "persons_profile_pictures"


def use_id(entity: Person, **kwargs) -> dict:
    return pydantic_model_dump(entity, **kwargs) | {"_dlt_id": __get_id(entity)}


@dlt.resource(
    selected=True,
    parallelized=True,
    primary_key="id",
)
def persons(rest_client: RESTClient) -> Iterable[TDataItem]:
    for persons_raw in rest_client.paginate(
        V2_PERSONS, params={"limit": V2_MAX_PAGE_LIMIT}, hooks=hooks
    ):
        yield persons_adapter.validate_python(persons_raw)


async def person_employments(
    person: Person,
    rest_client: RESTClient,
):
    href = jmespath.search("links.employments.href", person.field_meta)
    if not href:
        return
    for employments_raw in rest_client.paginate(
        href, params={"limit": V2_MAX_PAGE_LIMIT}, hooks=hooks
    ):
        employments = employments_adapter.validate_python(employments_raw)
        for employment in employments:
            yield dlt.mark.with_hints(
                item=use_id(employment, exclude=["field_meta", "org_units"]),
                hints=dlt.mark.make_hints(
                    table_name=Table.EMPLOYMENTS.value,
                ),
                # needs to be a variant due to https://github.com/dlt-hub/dlt/pull/2109
                create_table_variant=True,
            )


# TODO: Workaround for the fact that when `add_limit` is used, the yielded entities
# become dicts instead of first-class entities
def __get_id(obj):
    if isinstance(obj, dict):
        return obj.get("id")
    return getattr(obj, "id", None)


@dlt.transformer(
    max_table_nesting=1,
    parallelized=True,
    table_name=Table.PERSONS.value,
)
async def person_details(persons: List[Person], rest_client: RESTClient):
    yield [
        use_id(
            person,
            exclude=[
                "field_meta",
                "custom_attributes",
                "employments",
                "profile_picture",
            ],
        )
        for person in persons
    ]
    for person in persons:
        yield person_employments(person, rest_client)

        if person.profile_picture.url:
            # TODO: Pass `headers={"Accept": "image/*"}` to the REST client once
            # https://github.com/dlt-hub/dlt/pull/2434 is merged
            response = rest_client.get(str(person.profile_picture.url))
            if not response.ok:
                logging.error(
                    f"Failed to download profile picture for person {person.id}"
                )
            else:
                yield dlt.mark.with_hints(
                    item={"person_id": person.id, "profile_picture": response.content},
                    hints=dlt.mark.make_hints(
                        table_name=Table.PERSONS_PROFILE_PICTURES.value,
                        primary_key="person_id",
                        merge_key="person_id",
                        write_disposition="merge",
                    ),
                    # needs to be a variant due to https://github.com/dlt-hub/dlt/pull/2109
                    create_table_variant=True,
                )

        yield dlt.mark.with_hints(
            item={"person_id": person.id}
            | {cas.root.id: cas.root.value for cas in person.custom_attributes},
            hints=dlt.mark.make_hints(
                table_name=Table.CUSTOM_ATTRIBUTES.value,
                primary_key="person_id",
                merge_key="person_id",
                write_disposition="merge",
            ),
            # needs to be a variant due to https://github.com/dlt-hub/dlt/pull/2109
            create_table_variant=True,
        )


@dlt.source(name="personio")
def source(limit=-1) -> Sequence[DltResource]:
    rest_client, auth = get_rest_client()
    try:
        person_list = persons(rest_client)
        if limit > 0:
            person_list = person_list.add_limit(limit)

        return person_list | person_details(rest_client=rest_client)
    finally:
        if auth:
            auth.revoke_token()


__all__ = ["source"]
