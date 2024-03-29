import asyncio
import datetime
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from tgbot.config import load_config
from tgbot import handlers
from tgbot import middlewares

logger = logging.getLogger(__name__)


def register_all_middlewares(dp):
    ...


async def main():
    config = load_config('.env')
    logging_handlers = [logging.StreamHandler()]
    if config.bot.write_logs:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        log_file = rf'logs/{datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")}.log'
        logging_handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
        handlers=logging_handlers
    )

    bot = Bot(token=config.bot.token, parse_mode='HTML')


    redis = Redis(host=config.redis.host, port=config.redis.port)
    storage = RedisStorage(redis)
    dp = Dispatcher(
        storage=storage,
        config=config,
        redis=redis
    )

    register_all_middlewares(dp)

    dp.include_routers(*handlers.routers)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
