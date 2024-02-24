import os

from dotenv import load_dotenv
from pydantic import BaseModel


class RedisConfig(BaseModel):
    host: str
    port: int


class TelegramBot(BaseModel):
    token: str
    admin_ids: list[int]
    write_logs: bool


class Miscellaneous(BaseModel):
    service_api_token: str


class Config(BaseModel):
    bot: TelegramBot
    redis: RedisConfig
    misc: Miscellaneous


def load_config(path: str = None):
    load_dotenv(dotenv_path=path)

    return Config(
        bot=TelegramBot(
            token=os.getenv('BOT_TOKEN'),
            admin_ids=os.getenv('ADMINS', '').split(','),
            write_logs=os.getenv('WRITE_LOGS', 'False'),
        ),
        redis=RedisConfig(
            host=os.getenv('REDIS_HOST', '127.0.0.1'),
            port=os.getenv('REDIS_PORT', 6379)
        ),
        misc=Miscellaneous(
            service_api_token=os.getenv('SERVICE_API_TOKEN')
        )
    )
