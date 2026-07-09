from pyrogram import filters, types
from chikoo import app

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
        
    text = message.reply_to_message.text
    
    font1 = text.translate(SMALL_CAPS)
    font2 = text.translate(BOLD_AESTHETIC)
    
    response = f"**Font 1:**\n`{font1}`\n\n**Font 2:**\n`{font2}`"
    
    await message.reply_text(response)
