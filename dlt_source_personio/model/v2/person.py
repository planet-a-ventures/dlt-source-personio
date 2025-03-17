# generated by datamodel-codegen:
#   filename:  person.yaml

from __future__ import annotations

from enum import Enum
from typing import Annotated, Any, Dict, List, Literal

from pendulum import Date, DateTime
from pydantic import AnyUrl, Field, RootModel
from pydantic_extra_types.pendulum_dt import Date, DateTime

from ..v2 import MyPersonBaseModel


class Gender(str, Enum):
    UNSPECIFIED = "UNSPECIFIED"
    MALE = "MALE"
    FEMALE = "FEMALE"
    DIVERSE = "DIVERSE"


class ProfilePicture(MyPersonBaseModel):
    url: AnyUrl | None = None
    """
    The URL to the profile picture.
    """


class Status(str, Enum):
    UNSPECIFIED = "UNSPECIFIED"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class Type(str, Enum):
    UNSPECIFIED = "unspecified"
    STRING = "string"
    INT = "int"
    DOUBLE = "double"
    DATE = "date"
    BOOLEAN = "boolean"
    STRING_LIST = "string_list"


class CustomAttributeValueString(MyPersonBaseModel):
    id: str
    """
    The unique identifier for this custom attribute.
    """
    global_id: str
    """
    The global identifier for this attribute.
    """
    label: str | None = None
    """
    The label defined for this attribute.
    """
    type: Literal["string"]
    value: str


class CustomAttributeUnspecified(MyPersonBaseModel):
    id: str
    """
    The unique identifier for this custom attribute.
    """
    global_id: str
    """
    The global identifier for this attribute.
    """
    label: str | None = None
    """
    The label defined for this attribute.
    """
    type: Literal["unspecified"]
    value: Dict[str, Any]


class CustomAttributeValueInt(MyPersonBaseModel):
    id: str
    """
    The unique identifier for this custom attribute.
    """
    global_id: str
    """
    The global identifier for this attribute.
    """
    label: str | None = None
    """
    The label defined for this attribute.
    """
    type: Literal["int"]
    value: float


class CustomAttributeValueDouble(MyPersonBaseModel):
    id: str
    """
    The unique identifier for this custom attribute.
    """
    global_id: str
    """
    The global identifier for this attribute.
    """
    label: str | None = None
    """
    The label defined for this attribute.
    """
    type: Literal["double"]
    value: float


class CustomAttributeValueDate(MyPersonBaseModel):
    id: str
    """
    The unique identifier for this custom attribute.
    """
    global_id: str
    """
    The global identifier for this attribute.
    """
    label: str | None = None
    """
    The label defined for this attribute.
    """
    type: Literal["date"]
    value: Date


class CustomAttributeValueBoolean(MyPersonBaseModel):
    id: str
    """
    The unique identifier for this custom attribute.
    """
    global_id: str
    """
    The global identifier for this attribute.
    """
    label: str | None = None
    """
    The label defined for this attribute.
    """
    type: Literal["boolean"]
    value: bool


class CustomAttributeValueStringList(MyPersonBaseModel):
    id: str
    """
    The unique identifier for this custom attribute.
    """
    global_id: str
    """
    The global identifier for this attribute.
    """
    label: str | None = None
    """
    The label defined for this attribute.
    """
    type: Literal["string_list"]
    value: List[str]


class FieldMeta(MyPersonBaseModel):
    links: Dict[str, Any] | None = None
    """
    Additional metadata links.
    """


class Employment(MyPersonBaseModel):
    id: str
    """
    The employment id.
    """
    field_meta: Annotated[FieldMeta | None, Field(alias="_meta")] = None
    """
    This object represents the metadata information for the employment. It is a set of arbitrary key/value attributes.

    """


class CustomAttributes(
    RootModel[
        CustomAttributeValueString
        | CustomAttributeValueInt
        | CustomAttributeValueDouble
        | CustomAttributeValueDate
        | CustomAttributeValueBoolean
        | CustomAttributeValueStringList
        | CustomAttributeUnspecified
    ]
):
    root: Annotated[
        CustomAttributeValueString
        | CustomAttributeValueInt
        | CustomAttributeValueDouble
        | CustomAttributeValueDate
        | CustomAttributeValueBoolean
        | CustomAttributeValueStringList
        | CustomAttributeUnspecified,
        Field(discriminator="type"),
    ]


class Person(MyPersonBaseModel):
    id: str
    """
    The unique identifier for the Person.
    """
    field_meta: Annotated[Dict[str, Any], Field(alias="_meta")]
    """
    Has additional fields.
    """
    email: str
    """
    The email address this Person is connected with. The email is unique per Person, and the same Person can hold different Employments sharing the same email.

    """
    created_at: DateTime
    """
    The timestamp of when the person was created in UTC.
    """
    updated_at: DateTime
    """
    The timestamp of when the person was updated in UTC.
    """
    first_name: str
    """
    The first name of the person.
    """
    last_name: str
    """
    The last name of the person.
    """
    preferred_name: str | None = None
    """
    The preferred name of the person.
    """
    gender: Gender
    """
    The gender of the person.
    """
    profile_picture: ProfilePicture
    """
    The person's profile picture.
    """
    status: Status
    """
    The status of the person
    """
    custom_attributes: List[CustomAttributes]
    """
    A list of custom attributes.
    """
    employments: List[Employment]
    """
    A list of employments.
    """


class CustomAttribute(MyPersonBaseModel):
    type: Type
    """
    The type of the custom attribute.
    """
    value: Annotated[
        CustomAttributeValueString
        | CustomAttributeValueInt
        | CustomAttributeValueDouble
        | CustomAttributeValueDate
        | CustomAttributeValueBoolean
        | CustomAttributeValueStringList
        | CustomAttributeUnspecified
        | None,
        Field(discriminator="type"),
    ] = None
    """
    The value of the custom attribute.
    """
