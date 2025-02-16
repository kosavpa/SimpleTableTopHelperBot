import asyncio

from ClientHolder import start_up_client
from PeriodicTask import run_periodic_task
from Store import create_table
from MessageHandler import init_info
from MessageHandler import game_list
from MessageHandler import create_poll

async def main():
    await create_table()

    run_periodic_task()

    await start_up_client()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
