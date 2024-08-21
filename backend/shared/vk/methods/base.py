from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, ClassVar, Generic, TypeVar

from httpx import AsyncClient
from pydantic import BaseModel

from shared.vk.entities.base import VkMethodInputParams, VkMethodOutputParams
from shared.vk.exceptions import VkApiError

VK_API = "https://api.vk.com/method/{method}"

InputParams = TypeVar("InputParams")
OutputParams = TypeVar("OutputParams")


class VkApiResponse(BaseModel, Generic[OutputParams]):
    response: OutputParams


class VkBaseMethod(Generic[InputParams, OutputParams], ABC):
    if TYPE_CHECKING:
        __method__: ClassVar[str]
        __input__: ClassVar[type[VkMethodInputParams]]
        __output__: ClassVar[type[VkMethodOutputParams]]
    else:

        @property
        @abstractmethod
        def __method__(self) -> str:
            pass

        @property
        @abstractmethod
        def __input__(self) -> type[VkMethodInputParams]:
            pass

        @property
        @abstractmethod
        def __output__(self) -> type[VkMethodOutputParams]:
            pass

    @property
    def url(self) -> str:
        return VK_API.format(method=self.__method__)

    def __init__(self, client: AsyncClient, access_token: str) -> None:
        self.client = client
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "multipart/form-data",
        }

    async def __call__(
        self,
        params: InputParams,
    ) -> VkApiResponse[OutputParams]:
        params = params.model_dump()
        resp = await self.client.post(
            self.url,
            params=params,
            data=params,
            headers=self.headers,
        )
        return await self.check_response(resp.json())

    async def check_response(
        self,
        data: dict[str, Any],
    ) -> VkApiResponse[OutputParams]:
        response_type = VkApiResponse[self.__output__]
        if "error" in data:
            raise VkApiError(f"{data}")
        return response_type.model_validate(data)
