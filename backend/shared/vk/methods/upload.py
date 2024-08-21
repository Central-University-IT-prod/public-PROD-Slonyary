from shared.vk.entities.upload import UploadPhotoInput, UploadPhotoOutput
from shared.vk.methods.base import VkApiResponse, VkBaseMethod


class UploadPhoto(VkBaseMethod[UploadPhotoInput, UploadPhotoOutput]):
    __input__ = UploadPhotoInput
    __output__ = UploadPhotoOutput
    __method__ = None

    async def __call__(
        self,
        params: UploadPhotoInput,
    ) -> VkApiResponse[UploadPhotoOutput]:
        files = {"file": (params.filename, params.photo)}
        resp = await self.client.post(params.upload_url, files=files)
        return await self.check_response({"response": resp.json()})
