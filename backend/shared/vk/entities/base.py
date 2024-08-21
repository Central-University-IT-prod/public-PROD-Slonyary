from abc import ABC

from pydantic import BaseModel, ConfigDict

API_VERSION = "5.199"
LANG = "ru"


class VkObject(BaseModel, ABC):
    model_config = ConfigDict(
        use_enum_values=True,
        extra="allow",
        validate_assignment=True,
        frozen=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        defer_build=True,
    )


class MutableVkObject(VkObject):
    model_config = ConfigDict(
        frozen=False,
    )


class VkMethodInputParams(VkObject, ABC):
    v: str = API_VERSION
    lang: str = LANG


class VkMethodOutputParams(VkObject, ABC):
    pass
