# Copyright (c) 2025 marine
# Licensed under the MIT License.
# This file is part of chikooMusic
#CHIKOO-CODER

import re

from pyrogram import enums, types

from chikoo import app


class Utilities:
    def __init__(self):
        pass

    def format_eta(self, seconds: int) -> str:
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            return f"{seconds // 60}:{seconds % 60:02d} min"
        else:
            h = seconds // 3600
            m = (seconds % 3600) // 60
            s = seconds % 60
            return f"{h}:{m:02d}:{s:02d} h"

    def format_size(self, bytes: int) -> str:
        if bytes >= 1024**3:
            return f"{bytes / 1024 ** 3:.2f} GB"
        elif bytes >= 1024**2:
            return f"{bytes / 1024 ** 2:.2f} MB"
        else:
            return f"{bytes / 1024:.2f} KB"

    def to_seconds(self, time: str) -> int:
        parts = [int(p) for p in time.strip().split(":")]
        return sum(value * 60**i for i, value in enumerate(reversed(parts)))


    def get_url(self, message_1: types.Message) -> str | None:
        link = None
        messages = [message_1]
        entities = [enums.MessageEntityType.URL, enums.MessageEntityType.TEXT_LINK]

        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)

        for message in messages:
            if message.entities:
                for entity in message.entities:
                    if entity.type in entities:
                        link = entity.url
                        break

            if message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type in entities:
                        link = entity.url
                        break

        if link:
            return link.split("&si")[0].split("?si")[0]
        return None


    async def extract_user(self, msg: types.Message) -> types.User | None:
        if msg.reply_to_message:
            return msg.reply_to_message.from_user

        if msg.entities:
            for e in msg.entities:
                if e.type == enums.MessageEntityType.TEXT_MENTION:
                    return e.user

        if msg.text:
            try:
                if m := re.search(r"@(\w{5,32})", msg.text):
                    return await app.get_users(m.group(0))
                if m := re.search(r"\b\d{6,15}\b", msg.text):
                    return await app.get_users(int(m.group(0)))
            except:
                pass

        return None


    async def play_log(
        self,
        m: types.Message,
        title: str,
        duration: str,
    ) -> None:
        if m.chat.id == app.logger:
            return
        _text = m.lang["play_log"].format(
            app.name,
            m.chat.id,
            m.chat.title,
            m.from_user.id,
            m.from_user.mention,
            m.link,
            title,
            duration,
        )
        await app.send_message(chat_id=app.logger, text=_text)

    async def send_log(self, m: types.Message, chat: bool = False) -> None:
        from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        from chikoo import config
        
        if chat:
            user = m.from_user
            chat_obj = m.chat
            try:
                members = await app.get_chat_members_count(chat_obj.id)
            except Exception:
                members = "Unknown"
            
            try:
                invite_link = await app.export_chat_invite_link(chat_obj.id)
            except Exception:
                invite_link = f"https://t.me/{chat_obj.username}" if chat_obj.username else "Private (No Link)"
            
            chat_username = f"@{chat_obj.username}" if chat_obj.username else "Private Group"
            
            text = (
                f"<b>{app.name} Added In A New Group</b>\n\n"
                f"<b>Chat Name:</b> {chat_obj.title}\n"
                f"<b>Chat ID:</b> <code>{chat_obj.id}</code>\n"
                f"<b>Chat Username:</b> {chat_username}\n"
                f"<b>Chat Link:</b> {invite_link}\n"
                f"<b>Group Members:</b> {members}\n"
                f"<b>Added By:</b> {user.mention if user else 'Anonymous'}"
            )
            key = InlineKeyboardMarkup([[InlineKeyboardButton("Added By", user_id=user.id if user else app.id)]])
            
            pic = config.RANDOM_PIC
            if str(pic).endswith((".mp4", ".gif", ".webm", ".mkv")):
                await app.send_video(
                    chat_id=app.logger,
                    video=pic,
                    caption=text,
                    reply_markup=key
                )
            else:
                await app.send_photo(
                    chat_id=app.logger,
                    photo=pic,
                    caption=text,
                    reply_markup=key
                )
            return

        user = m.from_user
        text = (
            f"<b>{user.mention} JUST STARTED THE BOT.</b>\n\n"
            f"<b>USER ID:</b> <code>{user.id}</code>\n"
            f"<b>USERNAME:</b> @{user.username if user.username else 'None'}\n\n"
            f"<b>Developer:</b> nox_shadowx"
        )
        
        user_key = InlineKeyboardMarkup([
            [InlineKeyboardButton("User Profile", url=f"tg://openmessage?user_id={user.id}")]
        ])
        
        await app.send_message(
            chat_id=app.logger,
            text=text,
            reply_markup=user_key,
        )
