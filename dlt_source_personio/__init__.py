"""A source loading entities and lists from personio  (personio.com)"""

from enum import StrEnum
from typing import Any, Iterable, Sequence
import dlt
from dlt.common.typing import TDataItem
from dlt.sources import DltResource
import jmespath
from pydantic import AnyUrl

from dlt.common import json
from dlt.common.json import JsonSerializable

from .model.v2.person import Person

from .settings import V2_PERSONS
from pydantic import BaseModel
from .rest_client import get_rest_client, V2_MAX_PAGE_LIMIT, hooks
from .type_adapters import persons_adapter, employments_adapter


# logging.basicConfig(level=logging.DEBUG)


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
    CUSTOM_ATTRIBUTES = "custom_attributes"
    EMPLOYMENTS = "employments"


def use_id(entity: Person, **kwargs) -> dict:
    return pydantic_model_dump(entity, **kwargs) | {"_dlt_id": __get_id(entity)}


@dlt.resource(
    selected=True,
    parallelized=True,
    primary_key="id",
)
def persons() -> Iterable[TDataItem]:

    rest_client, auth = get_rest_client()
    try:
        for persons_raw in rest_client.paginate(
            V2_PERSONS, params={"limit": V2_MAX_PAGE_LIMIT}, hooks=hooks
        ):
            persons = persons_adapter.validate_python(persons_raw)
            yield [
                use_id(
                    person, exclude=["field_meta", "custom_attributes", "employments"]
                )
                for person in persons
            ]
            for person in persons:
                href = jmespath.search("links.employments.href", person.field_meta)
                if not href:
                    continue
                for employments_raw in rest_client.paginate(
                    href, params={"limit": V2_MAX_PAGE_LIMIT}, hooks=hooks
                ):
                    employments = employments_adapter.validate_python(employments_raw)
                    for employment in employments:
                        yield dlt.mark.with_hints(
                            item=use_id(
                                employment, exclude=["field_meta", "org_units"]
                            ),
                            hints=dlt.mark.make_hints(
                                table_name=Table.EMPLOYMENTS.value,
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
    finally:
        if auth:
            auth.revoke_token()


# TODO: Workaround for the fact that when `add_limit` is used, the yielded entities
# become dicts instead of first-class entities
def __get_id(obj):
    if isinstance(obj, dict):
        return obj.get("id")
    return getattr(obj, "id", None)


@dlt.source(name="personio")
def source(limit=-1) -> Sequence[DltResource]:

    person_list = persons()
    if limit > 0:
        person_list = person_list.add_limit(limit)

    return person_list


__all__ = ["source"]
