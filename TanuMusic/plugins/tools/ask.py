from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction
import requests
import urllib.parse
import asyncio
from TanuMusic import app 

def ask_query(query, model=None):
    default_model = 'mistralai/Mixtral-8x7B-Instruct-v0.1'
    system_prompt = """You are ResponseByAi, a Telegram bot managed by 𝐓ʜᴇ 𝐂ᴀᴘᴛᴀɪɴ's </> (@itzAsuraa)."""

    model = model or default_model

    if model == default_model:
        query = f"{system_prompt}\n\nUser: {query}"

    encoded_query = urllib.parse.quote(query)
    url = f"https://darkness.ashlynn.workers.dev/chat/?prompt={encoded_query}&model={model}"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json().get("response", "😕 Sorry, no response found.")
    else:
        return f"⚠️ Error fetching response from API. Status code: {response.status_code}"


@app.on_message(filters.command("ask"))
async def ask_handler(client: Client, message: Message):
    # Get the query from the message
    query = message.text.split(" ", 1)
    if len(query) > 1:
        user_query = query[1]

        # Send typing action to simulate a response delay
        await send_typing_action(client, message.chat.id)

        # Call the ask_query function to process the user query
        reply = ask_query(user_query)
        user_mention = message.from_user.mention
        await message.reply_text(f"{user_mention}, {reply} 🚀")
    else:
        await message.reply_text("📝 Please provide a query to ask ResponseByAi! Don't be shy, let's chat! 🤖💬.")


@app.on_message(filters.mentioned & filters.group)
async def mentioned_handler(client: Client, message: Message):
    # Extract text to process if there's text in the reply message or after the mention
    user_text = (
        message.reply_to_message.text.strip()
        if message.reply_to_message and message.reply_to_message.text
        else message.text.split(" ", 1)[1].strip()
        if len(message.text.split(" ", 1)) > 1
        else None
    )

    if user_text:
        # Send typing action to simulate a response delay
        await send_typing_action(client, message.chat.id)

        # Call the ask_query function to process the user query
        reply = ask_query(user_text)
        user_mention = message.from_user.mention
        await message.reply_text(f"{user_mention}, {reply} 🚀")
    else:
        await message.reply_text("👋 Please ask a question after mentioning me! I’m here to help! 😊")


# Simulate Typing Action
async def send_typing_action(client: Client, chat_id, duration=1):
    await client.send_chat_action(chat_id, ChatAction.TYPING)
    await asyncio.sleep(duration)