import asyncio
from io import BytesIO
from pathlib import Path

import httpx

from shared.vk.bot import VkBot

GROUP_ID = 123123
KEY = "vk1.a."


async def main() -> None:
    async with httpx.AsyncClient() as client:
        bot = VkBot(GROUP_ID, KEY, client)
        upload_server = await bot.get_wall_upload_server()
        print(upload_server)

        with open(Path(__file__).parent.resolve() / "example.jpg", "rb") as f:
            photo_bytes = BytesIO(f.read())
            photo_bytes.seek(0)
        photo = await bot.upload_photo(photo_bytes, upload_server)
        print(photo)

        saved_photos = await bot.save_photo(photo)
        print(saved_photos)

        post = await bot.create_post("message", saved_photos)
        print(post)


if __name__ == "__main__":
    asyncio.run(main())
