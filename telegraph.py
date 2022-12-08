import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from telegraph import upload_file

@Client.on_message(filters.command("telegraph"))
async def telegraph_upload(Client, message):
    replied = message.reply_to_message
    if not replied:
        await message.reply_text("Reply To A Photo Or Video Under 5MB")
        return
    text = await message.reply_text(text="Downloading", disable_web_page_preview=True)   
    media = await message.reply_to_message.download()   
    await text.edit_text(text="Uploading", disable_web_page_preview=True)                                            
    try:
        response = upload_file(media)
    except Exception as error:
        print(error)
        await text.edit_text(text=f"Error:- {error}", disable_web_page_preview=True)       
        return    
    try:
        os.remove(media)
    except Exception as error:
        print(error)
        return    
    await text.edit_text(
        text=f"<b>Link :-</b>\n\n<code>https://graph.org{response[0]}</code>",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton(text="Open Link", url=f"https://graph.org{response[0]}"),
            InlineKeyboardButton(text="Share Link", url=f"https://telegram.me/share/url?url=https://graph.org{response[0]}")
            ]]
        )
    )

