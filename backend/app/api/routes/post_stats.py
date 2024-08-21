from fastapi import APIRouter

router = APIRouter(prefix="/post_stats")

@router.get("/{channel_id}/{message_id}", status_code=200)
async def get_post_stats(channel_id: int, message_id: int):
    # Через pyrogram получение сообщения в канале по айди, затем возврат количества реакций, просмотров и репостов
    return 'ok'
