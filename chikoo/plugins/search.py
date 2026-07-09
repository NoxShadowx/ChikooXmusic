import aiohttp
from pyrogram import filters, types
from chikoo import app, lang
from chikoo.helpers import utils

search_cache = {}

@app.on_message(filters.command(["search"]))
@lang.language()
async def search_command(_, message: types.Message):
    if len(message.command) < 2:
        return await message.reply_text("Please provide a query to search. Example: `/search shape of you`")
    
    query = " ".join(message.command[1:])
    sent = await message.reply_text("🔍 Searching for music...")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.airbeats.xyz/api/search/songs",
                params={"query": query, "limit": 5}
            ) as response:
                if response.status != 200:
                    return await sent.edit_text("❌ Failed to fetch results from the API.")
                
                data = await response.json()
                
        if not data.get("success") or not data.get("data") or not data["data"].get("results"):
            return await sent.edit_text("❌ No results found.")
            
        results = data["data"]["results"]
        user_id = message.from_user.id
        search_cache[user_id] = results
        
        buttons = []
        text = f"**Search results for '{query}':**\n\n"
        for idx, song in enumerate(results):
            name = song.get("name", "Unknown")
            artists = "Unknown"
            if "artists" in song and "primary" in song["artists"] and song["artists"]["primary"]:
                artists = ", ".join([a.get("name", "") for a in song["artists"]["primary"]])
            
            text += f"{idx + 1}. {name} - {artists}\n"
            buttons.append([types.InlineKeyboardButton(f"{idx + 1}. {name}", callback_data=f"srch_dl_{idx}_{user_id}")])
            
        buttons.append([types.InlineKeyboardButton("❌ Close", callback_data="help close")])
        
        await sent.edit_text(
            text=text,
            reply_markup=types.InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        await sent.edit_text(f"❌ An error occurred: {str(e)}")

@app.on_callback_query(filters.regex(r"^srch_dl_"))
async def search_download_cb(_, query: types.CallbackQuery):
    data = query.data.split("_")
    idx = int(data[2])
    user_id = int(data[3])
    
    if query.from_user.id != user_id:
        return await query.answer("This search result is not for you!", show_alert=True)
        
    if user_id not in search_cache or len(search_cache[user_id]) <= idx:
        return await query.answer("Search session expired. Please search again.", show_alert=True)
        
    song = search_cache[user_id][idx]
    download_urls = song.get("downloadUrl", [])
    
    if not download_urls:
        return await query.answer("No download URL found for this song.", show_alert=True)
        
    # Get highest quality (320kbps usually last)
    best_url = download_urls[-1].get("url")
    name = song.get("name", "Audio")
    artists = "Unknown"
    if "artists" in song and "primary" in song["artists"] and song["artists"]["primary"]:
        artists = ", ".join([a.get("name", "") for a in song["artists"]["primary"]])
    
    await query.answer("Downloading and sending audio... Please wait.")
    
    try:
        await query.message.reply_audio(
            audio=best_url,
            title=name,
            performer=artists,
            caption=f"🎵 **{name}** - {artists}\n\nDownloaded via Airbeats API",
            quote=False
        )
    except Exception as e:
        await query.message.reply_text(f"❌ Failed to send audio: {str(e)}")
