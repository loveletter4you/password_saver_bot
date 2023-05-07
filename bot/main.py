import asyncio
from aiogram import Bot, Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from settings_env import TG_TOKEN, DB_URL
from bot.handlers import commands
from bot.middlewares.db import DbSessionMiddleware
from bot.models.base import init_models


async def main():
    engine = create_async_engine(url=DB_URL)
    await init_models(engine)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    bot = Bot(token=TG_TOKEN)
    dp = Dispatcher()
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    # Automatically reply to all callbacks
    dp.callback_query.middleware(CallbackAnswerMiddleware())
    dp.include_router(commands.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
