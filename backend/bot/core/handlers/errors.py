import logging
import traceback

from aiogram.types import ErrorEvent

from core.handlers.logger import TgLogger

tg_log = TgLogger()
logger = logging.getLogger(__name__)


async def error_handler(event: ErrorEvent) -> None:
    """
    Обработчик ошибок для пользователя
    """

    logger.error(msg=traceback.format_exc())
    await tg_log.error(traceback.format_exc())
