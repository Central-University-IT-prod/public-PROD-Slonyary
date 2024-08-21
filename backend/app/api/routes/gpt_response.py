import traceback

import anthropic
from fastapi import APIRouter
from httpx import Proxy

from app.api.deps import CurrentUserDep
from shared.core.config import Settings

router = APIRouter(prefix="/gpt_response", tags=["gpt"])


settings = Settings()

async_client = anthropic.AsyncClient(
    api_key=settings.GPT_KEY,
    proxies=Proxy(url="http://196.17.168.135:8000", auth=("uj0t2K", "EV6Cwa")),
)

SYSTEM_PROMPT = """
Улучши следующий текст для публикации, используя HTML-разметку для придания тексту выразительности и улучшения читабельности. Добавь подходящие эмодзи, создай заголовок с жирным шрифтом, выдели ключевые моменты и сделай текст привлекательным для аудитории (если нужно):
Указания:
- <b></b> для выделения важных слов и заголовков.
- <i></i> для выражения акцентов или курсива, где это уместно.
- <code></code> или <pre></pre> для выделения кода или технических указаний.
- Если есть ссылки, преобразуй их в <a href=""></a> для создания гиперссылок.
- По возможности, сократи и упрости текст для лучшей читабельности, но сохрани всю важную информацию.
- Где это уместно, добавь <s></s> для перечеркивания старой информации или ошибок.
- Используй <u></u> для подчеркивания информации, требующей особого внимания.
- Если необходимо включи эмодзи для добавления эмоционального оттенка и привлечения внимания к посту.
"""


async def gpt_response(prompt: str) -> str:
    try:
        response = await async_client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=4000,
            temperature=0.3,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": [{"type": "text", "text": prompt}]}],
        )

        text = response.content[0].text

        if text:
            return text
        else:
            return ""
    except Exception:
        print(traceback.format_exc())
        return ""


@router.get("", status_code=200)
async def get_gpt_response(prompt: str, user: CurrentUserDep) -> str:
    return await gpt_response(prompt)
