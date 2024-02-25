import asyncio
from time import time
from typing import Sequence

import click
from click import Group
from litestar import Litestar
from litestar.plugins import CLIPluginProtocol

from lib.database import db_config, async_sessionmaker
from models.user import User, UserService


async def get_users(db_engine) -> Sequence[User]:
    async with async_sessionmaker(bind=db_engine) as session:
        user_service = UserService(session)
        users = await user_service.list()
    return users


class DemoCLIPlugin(CLIPluginProtocol):
    def on_cli_init(self, cli: Group) -> None:
        @cli.command()
        def debug(app: Litestar) -> None:
            start = time()
            db_engine = db_config.get_engine()
            users = asyncio.run(get_users(db_engine))
            for user in users:
                message = f"{user.email}, {user.first_name}, {user.last_name}"
                click.echo(click.style(message, fg=(200, 150, 100)))
            end = time()
            print("The time of execution of above program is:",
                  (end - start) * 10 ** 3, "ms")
