from pyrogram import Client, filters, enums
import requests
import urllib.parse
import asyncio
from pyrogram.types import Message
from TanuMusic import app

# Function to query the AI API
def ask_query(query, model=None):
    default_model = 'gpt-4o'
    system_prompt = """Hey! I'm TanuMusic."""

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