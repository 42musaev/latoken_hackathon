import asyncio
import logging

from aiogram import Bot, Dispatcher
from handlers import router as router_handler
from quiz_handler import router as quiz_handler


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token="7439664834:AAHexCdBuE4YEc0xb-FqAL15U_FAulJwt_k")
    dp = Dispatcher()
    dp.include_router(quiz_handler)
    dp.include_router(router_handler)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
