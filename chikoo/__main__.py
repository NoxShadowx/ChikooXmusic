# Copyright (c) 2025 marine
# Licensed under the MIT License.
# This file is part of chikooMusic


import asyncio
import importlib

from pyrogram import idle
import os
from aiohttp import web

from chikoo import (anon, app, config, db,
                   logger, stop, userbot, yt)
from chikoo.plugins import all_modules

async def handle(request):
    return web.Response(text="Bot is running on Render")

async def web_server():
    webapp = web.Application()
    webapp.add_routes([web.get('/', handle)])
    runner = web.AppRunner(webapp)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logger.info(f"Web server started on port {port}")


async def main():
    await db.connect()
    asyncio.create_task(web_server())
    await app.boot()
    await userbot.boot()
    await anon.boot()

    for module in all_modules:
        importlib.import_module(f"chikoo.plugins.{module}")
    logger.info(f"Loaded {len(all_modules)} modules.")

    if config.COOKIES_URL:
        await yt.save_cookies(config.COOKIES_URL)

    sudoers = await db.get_sudoers()
    app.sudoers.update(sudoers)
    app.bl_users.update(await db.get_blacklisted())
    logger.info(f"Loaded {len(app.sudoers)} sudo users.")

    await idle()
    await stop()


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        pass
