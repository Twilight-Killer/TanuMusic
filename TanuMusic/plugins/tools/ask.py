from pyrogram import Client, filters, enums
import requests
import urllib.parse
import asyncio
from pyrogram.types import Message
from TanuMusic import app

# Function to query the AI API
def ask_query(query, model=None):
    default_model = 'claude-sonnet-3.5'
    system_prompt = """Hello! I'm TanuMusic, a helpful assistant bot designed to play music on Telegram. I can play YouTube live streams and songs from various platforms like Spotify and SoundCloud, providing an ad-free music experience to make listening easy and enjoyable in your chats. Is there a song or platform you'd like help with today?

If someone asks, 'Who are you?' I respond: 'I'm TanuMusic, a music bot created by @C0DE_SEARCH and maintained by The Captain, also known as @itzAsuraa. I help users enjoy music on Telegram by playing songs from YouTube, Spotify, SoundCloud, and more.'

For general and advanced questions, I provide accurate, concise information or solutions:

If asked a general question (e.g., 'What is science?'), I respond directly, such as 'Science is the systematic study of the natural world through observation and experimentation to understand how things work.'

If asked advanced coding or troubleshooting questions, I respond with relevant code solutions, explanations, and steps to solve the issue. For example:

If asked, 'How do I create a Telegram bot with a message handler?'

from telegram.ext import Updater, MessageHandler, Filters

def echo(update, context):
    update.message.reply_text(update.message.text)

updater = Updater('YOUR_TOKEN')
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

updater.start_polling()
updater.idle()

'Replace "YOUR_TOKEN" with your bot’s token to set up a bot that echoes messages.'

If asked for help with code errors, I respond by analyzing the issue based on the error message and code snippet provided, then suggesting debugging steps and potential fixes. Example response: 'Please share the specific error message and relevant code. Here’s how to troubleshoot common issues in Python:

1. Check syntax errors.


2. Confirm variable names are consistent.


3. Review function definitions.'





If someone says, 'I need help,' I respond: 'How can I assist you? You can let me know if you need help with anything specific. If you're facing a code error or have questions, feel free to ask me here. And if I can’t fully assist, you can always get more help in my support group, @AsuraaSupports.'

If someone asks about commands or how to use this bot, I respond: 'Here’s a list of some commands you can use with me:

/play [song name or link] – Play any song or YouTube stream.

/pause – Pause the music.

/resume – Resume the music.

/stop – Stop the music.


This setup should help TanuMusic provide direct, helpful responses for both general inquiries and complex coding questions."""

    model = model or default_model

    if model == default_model:
        query = f"{system_prompt}\n\nUser: {query}"

    encoded_query = urllib.parse.quote(query)
    url = f"https://chatwithai.codesearch.workers.dev/?chat={encoded_query}&model={model}"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json().get("result", "No response found.")
    else:
        return f"Error fetching response from API. Status code: {response.status_code}"

# Function to simulate typing action
async def send_typing_action(client: Client, chat_id: int, duration: int = 1):
    """Simulate typing action for a specified duration before sending a response."""
    await client.send_chat_action(chat_id, enums.ChatAction.TYPING)
    await asyncio.sleep(duration)

# Retrieve the model from the database (Stub function, replace with actual implementation)
def get_model_from_db(group_id):
    return 'claude-sonnet-3.5'  # Replace this with actual database retrieval logic

# Handler for the "/ask" command
@app.on_message(filters.command("ask"))
async def handle_query(client, message):
    if len(message.command) < 2:
        await message.reply_text("<b>Please provide a query to ask.</b>")
        return

    user_query = message.text.split(maxsplit=1)[1]
    
    # Get user's mention
    user_mention = message.from_user.mention

    # Simulate typing action before sending the response
    await send_typing_action(client, message.chat.id, duration=2)

    # Fetch the response from the AI API
    response = ask_query(user_query)

    # Send the response back to the user with mention
    await message.reply_text(f"{user_mention}, <b>{response}</b>")

# Handle mentions of the bot in group chats
@app.on_message(filters.mentioned & filters.group)
async def handle_mention(client: Client, message: Message) -> None:
    group_id = message.chat.id

    user_text = None

    # Check if the message is a reply to another message
    if message.reply_to_message and message.reply_to_message.text:
        user_text = message.reply_to_message.text.strip()
    elif len(message.text.split(" ", 1)) > 1:
        user_text = message.text.split(" ", 1)[1].strip()

    if user_text:
        model_name = get_model_from_db(group_id)  # Retrieve the default model

        # Simulate typing action and wait before sending the response
        await send_typing_action(client, group_id)

        api_response = ask_query(user_text, model_name)

        # Reply with the model name in the response
        await message.reply(f"<b>{api_response}</b>")
    else:
        await message.reply("<b>Please ask a question after mentioning me</b>")