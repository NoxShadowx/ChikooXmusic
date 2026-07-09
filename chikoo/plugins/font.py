from pyrogram import filters, types
from chikoo import app

from pyrogram.enums import ButtonStyle

SMALL_CAPS = str.maketrans(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ"
)

BOLD_AESTHETIC = str.maketrans(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
    "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙αʙᴄᴅєғɢʜιᴊᴋʟмησᴘǫʀsᴛυνωxʏᴢ"
)

@app.on_message(filters.command(["font"]) & ~app.bl_users)
async def font_command(_, message: types.Message):
    if not message.reply_to_message or not message.reply_to_message.text:
        return await message.reply_text("Please reply to a text message to convert its font!")
        
    btn_smallcaps = "Small Caps".translate(SMALL_CAPS)
    btn_aesthetic = "Aesthetic".translate(BOLD_AESTHETIC)

    buttons = [
        [
            types.InlineKeyboardButton(btn_smallcaps, callback_data="font_smallcaps", style=ButtonStyle.PRIMARY),
            types.InlineKeyboardButton(btn_aesthetic, callback_data="font_aesthetic", style=ButtonStyle.SUCCESS)
        ],
        [
            types.InlineKeyboardButton("⌯ 𝐂ʟσsє ⌯", callback_data="help close", style=ButtonStyle.DANGER)
        ]
    ]
    
    await message.reply_to_message.reply_text(
        "<b>Select a font style below:</b>",
        reply_markup=types.InlineKeyboardMarkup(buttons)
    )

@app.on_callback_query(filters.regex(r"^font_(smallcaps|aesthetic)$"))
async def font_callback(_, query: types.CallbackQuery):
    if not query.message.reply_to_message or not query.message.reply_to_message.text:
        return await query.answer("Original text not found!", show_alert=True)
        
    text = query.message.reply_to_message.text
    style = query.matches[0].group(1)
    
    if style == "smallcaps":
        converted = text.translate(SMALL_CAPS)
        font_name = "Small Caps"
    else:
        converted = text.translate(BOLD_AESTHETIC)
        font_name = "Aesthetic"
        
    btn_smallcaps = "Small Caps".translate(SMALL_CAPS)
    btn_aesthetic = "Aesthetic".translate(BOLD_AESTHETIC)

    buttons = [
        [
            types.InlineKeyboardButton(btn_smallcaps, callback_data="font_smallcaps", style=ButtonStyle.PRIMARY),
            types.InlineKeyboardButton(btn_aesthetic, callback_data="font_aesthetic", style=ButtonStyle.SUCCESS)
        ],
        [
            types.InlineKeyboardButton("⌯ 𝐂ʟσsє ⌯", callback_data="help close", style=ButtonStyle.DANGER)
        ]
    ]
    
    await query.message.edit_text(
        f"<b>{font_name}:</b>\n\n<code>{converted}</code>",
        reply_markup=types.InlineKeyboardMarkup(buttons)
    )
