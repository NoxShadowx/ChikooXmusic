# Copyright (c) 2025 marine 
# Licensed under the MIT License.
# This file is part of chikooMusic


import pyrogram

from chikoo import config, logger


class Bot(pyrogram.Client):
    def __init__(self):
        super().__init__(
            name="chikoo",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            parse_mode=pyrogram.enums.ParseMode.HTML,
            max_concurrent_transmissions=7,
            link_preview_options=pyrogram.types.LinkPreviewOptions(is_disabled=True),
        )
        self.owner = config.OWNER_ID
        self.logger = config.LOGGER_ID
        self.bl_users = pyrogram.filters.user()
        self.sudoers = pyrogram.filters.user(self.owner)

    async def boot(self):
        """
        Starts the bot and performs initial setup.

        Raises:
            SystemExit: If the bot fails to access the log group or is not an administrator in the logger group.
        """
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name
        self.username = self.me.username
        self.mention = self.me.mention

        try:
            from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
            bot_started_text = f"""
🎵 <b>Bot Started Successfully</b>

<b>Name:</b> {self.name}
<b>Username:</b> @{self.username}
<b>ID:</b> <code>{self.id}</code>

<i>Bot is now online and ready to serve!</i>
"""
            key = InlineKeyboardMarkup([[InlineKeyboardButton("Add Me To Your Group", url=f"https://t.me/{self.username}?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users")]])
            pic = config.RANDOM_PIC
            if str(pic).endswith((".mp4", ".gif", ".webm", ".mkv")):
                await self.send_video(self.logger, video=pic, caption=bot_started_text, reply_markup=key)
            else:
                await self.send_photo(self.logger, photo=pic, caption=bot_started_text, reply_markup=key)
            get = await self.get_chat_member(self.logger, self.id)
            
            # Set bot commands
            from pyrogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeAllChatAdministrators, BotCommandScopeChat
            
            # Commands for everyone
            await self.set_bot_commands(
                [
                    BotCommand("play", "Play music in voice chat"),
                    BotCommand("vplay", "Play video in voice chat"),
                    BotCommand("search", "Search for a track on YouTube"),
                    BotCommand("queue", "Check the queued tracks"),
                    BotCommand("stats", "Check bot statistics"),
                    BotCommand("ping", "Check bot status"),
                    BotCommand("lang", "Change bot language"),
                    BotCommand("help", "Show help menu"),
                    BotCommand("settings", "Show playmode settings"),
                    BotCommand("autoplay", "Toggle Auto Play Moods")
                ],
                scope=BotCommandScopeDefault()
            )
            
            # Commands for Group Admins
            await self.set_bot_commands(
                [
                    BotCommand("play", "Play music in voice chat"),
                    BotCommand("vplay", "Play video in voice chat"),
                    BotCommand("search", "Search for a track on YouTube"),
                    BotCommand("queue", "Check the queued tracks"),
                    BotCommand("stats", "Check bot statistics"),
                    BotCommand("ping", "Check bot status"),
                    BotCommand("lang", "Change bot language"),
                    BotCommand("help", "Show help menu"),
                    BotCommand("settings", "Show playmode settings"),
                    BotCommand("autoplay", "Toggle Auto Play Moods"),
                    BotCommand("pause", "Pause playback"),
                    BotCommand("resume", "Resume playback"),
                    BotCommand("skip", "Skip current track"),
                    BotCommand("stop", "Stop playback"),
                    BotCommand("seek", "Seek current track"),
                    BotCommand("auth", "Add authorized users"),
                    BotCommand("unauth", "Remove authorized users"),
                    BotCommand("authusers", "List authorized users"),
                    BotCommand("tagall", "Tag all members in the group"),
                    BotCommand("cancel", "Stop tagging members")
                ],
                scope=BotCommandScopeAllChatAdministrators()
            )
            
            # Commands for Owner
            await self.set_bot_commands(
                [
                    BotCommand("play", "Play music in voice chat"),
                    BotCommand("vplay", "Play video in voice chat"),
                    BotCommand("search", "Search for a track on YouTube"),
                    BotCommand("queue", "Check the queued tracks"),
                    BotCommand("stats", "Check bot statistics"),
                    BotCommand("ping", "Check bot status"),
                    BotCommand("lang", "Change bot language"),
                    BotCommand("help", "Show help menu"),
                    BotCommand("settings", "Show playmode settings"),
                    BotCommand("autoplay", "Toggle Auto Play Moods"),
                    BotCommand("pause", "Pause playback"),
                    BotCommand("resume", "Resume playback"),
                    BotCommand("skip", "Skip current track"),
                    BotCommand("stop", "Stop playback"),
                    BotCommand("seek", "Seek current track"),
                    BotCommand("auth", "Add authorized users"),
                    BotCommand("unauth", "Remove authorized users"),
                    BotCommand("tagall", "Tag all members in the group"),
                    BotCommand("cancel", "Stop tagging members"),
                    BotCommand("owner", "Show owner menu"),
                    BotCommand("broadcast", "Broadcast a message"),
                    BotCommand("save_broadcast", "Save a broadcast message"),
                    BotCommand("saved_broadcasts", "List saved broadcasts"),
                    BotCommand("del_broadcast", "Delete a saved broadcast"),
                    BotCommand("load_broadcast", "Load a saved broadcast"),
                    BotCommand("schedule_broadcast", "Schedule a broadcast"),
                    BotCommand("stop_broadcast", "Stop a running broadcast"),
                    BotCommand("blacklist", "Blacklist a user"),
                    BotCommand("unblacklist", "Unblacklist a user"),
                    BotCommand("whitelist", "Whitelist a user"),
                    BotCommand("addsudo", "Add a sudo user"),
                    BotCommand("delsudo", "Remove a sudo user"),
                    BotCommand("listsudo", "List sudo users"),
                    BotCommand("logger", "Toggle bot logging"),
                    BotCommand("logs", "Get bot logs"),
                    BotCommand("restart", "Restart the bot"),
                    BotCommand("logger", "Enable/disable the logger"),
                    BotCommand("addsudo", "Add a user to sudo list"),
                    BotCommand("rmsudo", "Remove a user from sudo list"),
                    BotCommand("sudolist", "List all sudo users"),
                    BotCommand("search", "Search and download mp3 music")
                ],
                scope=BotCommandScopeChat(chat_id=self.owner)
            )
            
        except Exception as ex:
            raise SystemExit(f"Bot has failed to access the log group: {self.logger}\nReason: {ex}")

        if get.status != pyrogram.enums.ChatMemberStatus.ADMINISTRATOR:
            raise SystemExit("Please promote the bot as an admin in logger group.")
        
        try:
            from pyrogram.types import BotCommand
            commands = [
                BotCommand("play", "Play a song"),
                BotCommand("vplay", "Play a video"),
                BotCommand("pause", "Pause the playback"),
                BotCommand("resume", "Resume the playback"),
                BotCommand("skip", "Skip to the next track"),
                BotCommand("stop", "Stop playback and clear queue"),
                BotCommand("seek", "Seek the current track"),
                BotCommand("queue", "Check the playback queue"),
                BotCommand("lang", "Change bot language"),
                BotCommand("ping", "Check bot status and latency"),
                BotCommand("stats", "Check bot stats")
            ]
            await self.set_bot_commands(commands)
        except Exception as e:
            logger.warning(f"Failed to set bot commands: {e}")

        try:
            import asyncio
            from chikoo.plugins.saved_broadcasts import scheduler_loop
            asyncio.create_task(scheduler_loop(self))
            logger.info("Started Scheduled Broadcast Loop")
        except Exception as e:
            logger.warning(f"Failed to start scheduler loop: {e}")

        logger.info(f"Bot started as @{self.username}")

    async def exit(self):
        """
        Asynchronously stops the bot.
        """
        await super().stop()
        logger.info("Bot stopped.")
