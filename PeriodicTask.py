import asyncio
from datetime import datetime
from typing import Sequence

import schedule
from croniter import croniter
from telethon.tl.types import MessageMediaPoll, PollResults

from ClientHolder import client
from MessagesUtil import create_batches_game_list, get_poll
from Store import Info, select_all


def run_periodic_task():
    schedule.every().hour.do(lambda: asyncio.create_task(ask_about_game()))

    asyncio.create_task(run_scheduler())


async def run_scheduler():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


async def ask_about_game():
    infos: Sequence[Info] = await select_all()

    for info in infos:
        if croniter.match(info.cron_question_about_game, datetime.now()):
            for batch in create_batches_game_list(info):
                await client.send_message(
                    info.chat_id,
                    file=MessageMediaPoll(get_poll(batch, info), PollResults()),
                    reply_to=info.forum_id
                )
