from aiogram import Bot, Dispatcher
from config_reader import config
import asyncio
from callbacks import user_collbacks
from handlers import *
db = []


async def main():
    bot = Bot(config.bot_token.get_secret_value())

    dp = Dispatcher()
    dp.include_routers(
        user_commands.router,
        newClient_handlers.router,
        oldClient_handlers.router,
        user_collbacks.router
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
