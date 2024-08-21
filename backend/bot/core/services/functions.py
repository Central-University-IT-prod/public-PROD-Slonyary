import base64
import traceback
from typing import Optional

import aiofiles


async def image_to_base64(path_to_file: str) -> Optional[str]:
    try:
        async with aiofiles.open(path_to_file, "rb") as img:
            return base64.b64encode(await img.read()).decode("utf-8")
    except FileNotFoundError:
        print(traceback.format_exc())
        return None
    except IOError:
        print(traceback.format_exc())
        return None
