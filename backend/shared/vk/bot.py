from io import BytesIO

import httpx

from shared.vk.entities.create_post import CreatePostInput, CreatePostOutput
from shared.vk.entities.get_wall_upload_server import (
    GetWallUploadServerInput,
    GetWallUploadServerOutput,
)
from shared.vk.entities.media import Media
from shared.vk.entities.photo import Photo
from shared.vk.entities.save_wall_photo import SaveWallPhotoInput
from shared.vk.entities.upload import UploadPhotoInput, UploadPhotoOutput
from shared.vk.methods.create_post import VkCreatePost
from shared.vk.methods.get_wall_upload_server import GetWallUploadServer
from shared.vk.methods.save_wall_photo import SaveWallPhoto
from shared.vk.methods.upload import UploadPhoto


class VkBot:
    def __init__(
        self,
        group_id: int,
        key: str,
        client: httpx.AsyncClient,
    ) -> None:
        self.group_id = abs(group_id)
        self.key = key
        self.client = client

    async def get_wall_upload_server(self) -> GetWallUploadServerOutput:
        get_wall_server = GetWallUploadServer(self.client, self.key)
        params = GetWallUploadServerInput(group_id=self.group_id)
        result = await get_wall_server(params)
        return result.response

    async def upload_photo(
        self,
        photo: BytesIO,
        filename: str,
        upload_server: GetWallUploadServerOutput,
    ) -> UploadPhotoOutput:
        upload_photo_method = UploadPhoto(self.client, self.key)
        params = UploadPhotoInput(
            upload_url=upload_server.upload_url,
            filename=filename,
            photo=photo,
        )
        result = await upload_photo_method(params)
        return result.response

    async def save_photo(self, photo: UploadPhotoOutput) -> list[Photo]:
        save_wall_photo = SaveWallPhoto(self.client, self.key)
        params = SaveWallPhotoInput(
            group_id=self.group_id,
            photo=photo.photo,
            server=photo.server,
            hash=photo.hash,
        )
        result = await save_wall_photo(params)
        return result.response

    async def create_post(
        self,
        message: str,
        photos: list[Photo] | None = None,
    ) -> CreatePostOutput:
        post_create = VkCreatePost(self.client, self.key)

        attachments = (
            ",".join(
                (
                    str(Media(type="photo", owner_id=photo.owner_id, media_id=photo.id))
                    for photo in photos
                )
            )
            if photos
            else None
        )

        params = CreatePostInput(
            owner_id=-self.group_id,
            from_group=1,
            message=message,
            attachments=attachments,
            mark_as_ads=0,
            close_comments=0,
            mute_notifications=0,
            copyright=None,
        )
        result = await post_create(params)
        return result.response
